"""Sri Yantra — 9 interlocking triangles around a central bindu point.
Blender script: paste into Text Editor → Run Script → STL auto-exports.
Phi-derived coordinates. Zero runtime dependencies beyond Blender."""
import bpy, math, bmesh
from mathutils import Vector

GOLD = (1.0, 0.843, 0.0, 1.0)
CRIMSON = (0.698, 0.133, 0.133, 1.0)
CRYSTAL = (0.85, 0.95, 1.0, 0.3)
OBSIDIAN = (0.05, 0.05, 0.08, 1.0)

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)

def make_material(name, color, metallic=0.0, roughness=0.4, alpha=1.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    if alpha < 1.0:
        bsdf.inputs['Alpha'].default_value = alpha
        mat.blend_method = 'BLEND'
    return mat

def triangle_verts(cx, cy, cz, radius, angle_offset=0.0, z_scale=1.0):
    """Return 3 vertices of an equilateral triangle centered at (cx,cy,cz)."""
    verts = []
    for i in range(3):
        angle = math.radians(120 * i + angle_offset)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        z = cz
        verts.append(Vector((x, y, z)))
    return verts

def create_triangle_mesh(name, verts, mat, thickness=0.015):
    """Create a thin triangular prism from 3 base verts."""
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    # Bottom face
    bv = [bm.verts.new(v) for v in verts]
    # Top face
    tv = [bm.verts.new(Vector((v.x, v.y, v.z + thickness))) for v in verts]
    bm.faces.new(bv)
    bm.faces.new(tv[::-1])
    for i in range(3):
        bm.faces.new([bv[i], bv[(i+1)%3], tv[(i+1)%3], tv[i]])
    bm.to_mesh(mesh)
    bm.free()
    mesh.validate()
    obj.data.materials.append(mat)
    return obj

def build_sri_yantra():
    """9 triangles: 5 downward (Shakti) + 4 upward (Shiva), nested around bindu."""
    # Radii for 9 rings — phi-scaled
    phi = (1 + math.sqrt(5)) / 2
    base_r = 0.5
    radii = [base_r * (phi ** (i * 0.38)) for i in range(9)]

    gold_mat = make_material('SriGold', GOLD, metallic=0.9, roughness=0.15)
    crimson_mat = make_material('SriCrimson', CRIMSON, metallic=0.1, roughness=0.5)
    crystal_mat = make_material('SriCrystal', CRYSTAL, metallic=0.0, roughness=0.05, alpha=0.4)
    obsidian_mat = make_material('SriObsidian', OBSIDIAN, metallic=0.8, roughness=0.1)

    objs = []
    for i in range(9):
        r = radii[i]
        z = i * 0.012  # slight z-layering so triangles don't z-fight
        # Alternate upward (Shiva, gold) and downward (Shakti, crimson)
        if i % 2 == 0:
            mat = gold_mat
            angle_off = 90.0  # apex up
        else:
            mat = crimson_mat
            angle_off = 270.0  # apex down
        verts = triangle_verts(0, 0, z, r, angle_offset=angle_off)
        obj = create_triangle_mesh(f'Triangle_{i:02d}', verts, mat)
        objs.append(obj)

    # Central bindu (point) — small gold sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.015, location=(0, 0, 0.12))
    bindu = bpy.context.active_object
    bindu.name = 'Bindu'
    bindu.data.materials.append(gold_mat)

    # Outer lotus circle (torus)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=radii[-1] * 1.18,
        minor_radius=0.012,
        location=(0, 0, 0)
    )
    outer = bpy.context.active_object
    outer.name = 'OuterLotus'
    outer.data.materials.append(crystal_mat)

    # Second lotus ring
    bpy.ops.mesh.primitive_torus_add(
        major_radius=radii[-1] * 1.08,
        minor_radius=0.008,
        location=(0, 0, 0.005)
    )
    inner_lotus = bpy.context.active_object
    inner_lotus.name = 'InnerLotus'
    inner_lotus.data.materials.append(obsidian_mat)

    return objs

# --- MAIN ---
clear_scene()
build_sri_yantra()

# Export STL
import os
export_path = os.path.expanduser('~/Desktop/sri_yantra.stl')
bpy.ops.export_mesh.stl(filepath=export_path, use_mesh_modifiers=True)
print(f'STL exported → {export_path}')
