import bpy
import math

# =====================================================
# SRI YANTRA - 9 interlocking triangles
# 4 upward (Shiva) + 5 downward (Shakti)
# + Bindu (center point), 8-petal + 16-petal lotus
# Extruded to 3D for printing/rendering
# =====================================================

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=True)

SCALE = 50.0
DEPTH = 5.0
half_d = DEPTH / 2.0

triangles_2d = {
    'S1': [(0.0, 0.95),  (-0.82, -0.47), ( 0.82, -0.47)],
    'S2': [(0.0, 0.62),  (-0.78, -0.58), ( 0.78, -0.58)],
    'S3': [(0.0, 0.35),  (-0.60, -0.55), ( 0.60, -0.55)],
    'S4': [(0.0, 0.15),  (-0.32, -0.22), ( 0.32, -0.22)],
    'K1': [(0.0, -0.88), (-0.78,  0.42), ( 0.78,  0.42)],
    'K2': [(0.0, -0.60), (-0.68,  0.32), ( 0.68,  0.32)],
    'K3': [(0.0, -0.40), (-0.52,  0.22), ( 0.52,  0.22)],
    'K4': [(0.0, -0.22), (-0.35,  0.15), ( 0.35,  0.15)],
    'K5': [(0.0, -0.10), (-0.18,  0.08), ( 0.18,  0.08)],
}

mat_shiva = bpy.data.materials.new('Shiva')
mat_shiva.use_nodes = True
mat_shiva.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.4, 0.7, 1.0, 1.0)
mat_shiva.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 0.6
mat_shiva.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.1

mat_shakti = bpy.data.materials.new('Shakti')
mat_shakti.use_nodes = True
mat_shakti.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (1.0, 0.3, 0.1, 1.0)
mat_shakti.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 0.7
mat_shakti.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.1

def make_triangle_prism(name, pts_2d, scale, z_bot, z_top, mat):
    verts = []
    for x, y in pts_2d:
        verts.append((x*scale, y*scale, z_bot))
    for x, y in pts_2d:
        verts.append((x*scale, y*scale, z_top))
    faces = [
        (0, 2, 1), (3, 4, 5),
        (0, 1, 4), (0, 4, 3),
        (1, 2, 5), (1, 5, 4),
        (2, 0, 3), (2, 3, 5),
    ]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj

for name, pts in triangles_2d.items():
    mat = mat_shiva if name.startswith('S') else mat_shakti
    idx = int(name[1])
    dz = DEPTH * (1.0 - 0.07 * idx)
    make_triangle_prism(name, pts, SCALE, -dz/2, dz/2, mat)

mat_bindu = bpy.data.materials.new('Bindu')
mat_bindu.use_nodes = True
mat_bindu.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (1.0, 0.9, 0.1, 1.0)
mat_bindu.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 1.0
mat_bindu.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.05
bpy.ops.mesh.primitive_uv_sphere_add(radius=2.0, location=(0,0,0), segments=32, ring_count=16)
bpy.context.active_object.name = 'Bindu'
bpy.context.active_object.data.materials.append(mat_bindu)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.shade_flat()
bpy.ops.object.select_all(action='DESELECT')

print('Sri Yantra complete: 4 Shiva (blue) + 5 Shakti (red) + gold Bindu')
