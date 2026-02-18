# Stellated Icosahedron-Dodecahedron Compound (the "cool shape")
# Paste into Blender Text Editor > Run Script (▶ or Alt+P)
# Note: This is the poke-stellated version — visually cool but
# not the mathematically exact Kepler-Poinsot dual compound.
# Exports STL to ~/Desktop/cool_stellated_compound.stl
import bpy, bmesh, math, os
from mathutils import Vector

PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI
SC = 1.5

# --- Clear scene ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.meshes):
    bpy.data.meshes.remove(m)
for m in list(bpy.data.materials):
    bpy.data.materials.remove(m)

# === ICOSAHEDRON (12 verts, 20 tri faces) ===
ico_v = []
for s1 in (1,-1):
    for s2 in (1,-1):
        ico_v.append(Vector((0, s1, s2*PHI)))
        ico_v.append(Vector((s1*PHI, 0, s2)))
        ico_v.append(Vector((s1, s2*PHI, 0)))

def find_tri_faces(verts, edge_len):
    tol = 0.05
    faces = []
    n = len(verts)
    for i in range(n):
        for j in range(i+1, n):
            if abs((verts[i]-verts[j]).length - edge_len) > tol:
                continue
            for k in range(j+1, n):
                if (abs((verts[i]-verts[k]).length - edge_len) < tol and
                    abs((verts[j]-verts[k]).length - edge_len) < tol):
                    faces.append((i,j,k))
    return faces

ico_f = find_tri_faces(ico_v, 2.0)

# === DODECAHEDRON (20 verts, 12 pent faces) ===
dod_v = []
for x in (1,-1):
    for y in (1,-1):
        for z in (1,-1):
            dod_v.append(Vector((x, y, z)))
for s1 in (1,-1):
    for s2 in (1,-1):
        dod_v.append(Vector((0, s1*PHI_INV, s2*PHI)))
        dod_v.append(Vector((s1*PHI, 0, s2*PHI_INV)))
        dod_v.append(Vector((s1*PHI_INV, s2*PHI, 0)))

def find_pent_faces(verts, edge_len):
    tol = 0.05
    n = len(verts)
    adj = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i+1, n):
            if abs((verts[i]-verts[j]).length - edge_len) < tol:
                adj[i].add(j)
                adj[j].add(i)
    faces = []
    seen = set()
    for a in range(n):
        for b in adj[a]:
            if b <= a: continue
            for c in adj[b]:
                if c == a: continue
                for d in adj[c]:
                    if d == a or d == b: continue
                    for e in adj[d]:
                        if e == a and e != b and e != c and a in adj[e]:
                            key = tuple(sorted([a,b,c,d,e]))
                            if key not in seen:
                                norm = (verts[b]-verts[a]).cross(verts[c]-verts[a]).normalized()
                                if all(abs(norm.dot(verts[x]-verts[a])) < tol for x in [d,e]):
                                    seen.add(key)
                                    faces.append((a,b,c,d,e))
    return faces

dod_edge = 2 * PHI_INV
dod_f = find_pent_faces(dod_v, dod_edge)

# === BUILD MESHES ===
def make_obj(name, verts, faces, color):
    m = bpy.data.meshes.new(name+'_m')
    o = bpy.data.objects.new(name, m)
    bpy.context.collection.objects.link(o)
    m.from_pydata([list(v*SC) for v in verts], [], list(faces))
    m.update()
    mat = bpy.data.materials.new(name+'_mat')
    mat.use_nodes = True
    bs = mat.node_tree.nodes.get('Principled BSDF')
    if bs:
        bs.inputs['Base Color'].default_value = color
        bs.inputs['Alpha'].default_value = 0.85
    try:
        mat.surface_render_method = 'BLENDED'
    except:
        try:
            mat.blend_method = 'BLEND'
        except:
            pass
    o.data.materials.append(mat)
    return o

def stellate(obj, factor):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    res = bmesh.ops.poke(bm, faces=bm.faces[:])
    for v in res['verts']:
        d = v.co.normalized()
        v.co = v.co + d * factor * SC
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    obj.select_set(False)

# Icosahedron - blue
ico_obj = make_obj('Stellated_Icosahedron', ico_v, ico_f, (0.15, 0.4, 1.0, 1.0))
stellate(ico_obj, PHI * 0.5)

# Dodecahedron - gold
dod_obj = make_obj('Stellated_Dodecahedron', dod_v, dod_f, (1.0, 0.75, 0.1, 1.0))
stellate(dod_obj, PHI * 0.618)

# Light
bpy.ops.object.light_add(type='SUN', location=(5,5,10))

# === EXPORT STL ===
bpy.ops.object.select_all(action='DESELECT')
ico_obj.select_set(True)
dod_obj.select_set(True)
bpy.context.view_layer.objects.active = ico_obj

out = os.path.expanduser("~/Desktop/cool_stellated_compound.stl")
try:
    bpy.ops.wm.stl_export(filepath=out, export_selected_objects=True)
except:
    bpy.ops.export_mesh.stl(filepath=out, use_selection=True)
print(f"\n✓ STL → {out}")

print('=== COMPOUND COMPLETE ===')
print(f'Icosahedron: {len(ico_f)} stellated faces')
print(f'Dodecahedron: {len(dod_f)} stellated faces')
print(f'All coords from phi = {PHI:.10f}')
