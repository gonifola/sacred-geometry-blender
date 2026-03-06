import bpy
import math

# =====================================================
# KLEIN BOTTLE - immersion in R3
# Parametric surface, u/v in [0, 2pi]
# Non-orientable: the surface passes through itself
# =====================================================

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=True)

U_STEPS = 80
V_STEPS = 60

def klein(u, v):
    if u < math.pi:
        x = 3*math.cos(u)*(1 + math.sin(u)) + (2*(1 - math.cos(u)/2))*math.cos(u)*math.cos(v)
        y = 8*math.sin(u) + (2*(1 - math.cos(u)/2))*math.sin(u)*math.cos(v)
        z = (2*(1 - math.cos(u)/2))*math.sin(v)
    else:
        x = 3*math.cos(u)*(1 + math.sin(u)) + (2*(1 - math.cos(u)/2))*math.cos(v + math.pi)
        y = 8*math.sin(u)
        z = (2*(1 - math.cos(u)/2))*math.sin(v)
    return x, y, z

pts = [[klein(2*math.pi*i/U_STEPS, 2*math.pi*j/V_STEPS)
        for j in range(V_STEPS)] for i in range(U_STEPS)]

all_p = [pts[i][j] for i in range(U_STEPS) for j in range(V_STEPS)]
cx = sum(p[0] for p in all_p)/len(all_p)
cy = sum(p[1] for p in all_p)/len(all_p)
cz = sum(p[2] for p in all_p)/len(all_p)
ext = max(
    max(p[0] for p in all_p)-min(p[0] for p in all_p),
    max(p[1] for p in all_p)-min(p[1] for p in all_p),
    max(p[2] for p in all_p)-min(p[2] for p in all_p)
)
sc = 50.0/ext

verts = [((pts[i][j][0]-cx)*sc, (pts[i][j][1]-cy)*sc, (pts[i][j][2]-cz)*sc)
         for i in range(U_STEPS) for j in range(V_STEPS)]

def vidx(i, j):
    return (i % U_STEPS)*V_STEPS + (j % V_STEPS)

faces = []
for i in range(U_STEPS):
    for j in range(V_STEPS):
        a, b = vidx(i,j), vidx(i+1,j)
        c, d = vidx(i,j+1), vidx(i+1,j+1)
        faces.append((a, b, d, c))

mesh = bpy.data.meshes.new('KleinBottle')
mesh.from_pydata(verts, [], faces)
mesh.update()
obj = bpy.data.objects.new('KleinBottle', mesh)
bpy.context.collection.objects.link(obj)

mat = bpy.data.materials.new('KleinMat')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.1, 0.6, 0.9, 1.0)
bsdf.inputs['Metallic'].default_value = 0.8
bsdf.inputs['Roughness'].default_value = 0.05
bsdf.inputs['Alpha'].default_value = 0.85
mat.blend_method = 'BLEND'
obj.data.materials.append(mat)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.shade_smooth()
bpy.ops.object.select_all(action='DESELECT')

print(f'Klein bottle: {len(verts)} verts, {len(faces)} quads, 100mm diameter')
