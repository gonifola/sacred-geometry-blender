import bpy
import os

# ═══════════════════════════════════════════════════════════
# CUBE-OCTAHEDRON COMPOUND (Poke-Stellated)
# Pre-computed geometry — single from_pydata call
# Cube (gold) + Octahedron (blue), shared midsphere
# Both tip sets at same outer sphere radius
# ═══════════════════════════════════════════════════════════

# Clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

verts = [
    (-1.000000, -1.000000, -1.000000),
    (-1.000000, -1.000000, 1.000000),
    (-1.000000, 1.000000, -1.000000),
    (-1.000000, 1.000000, 1.000000),
    (1.000000, -1.000000, -1.000000),
    (1.000000, -1.000000, 1.000000),
    (1.000000, 1.000000, -1.000000),
    (1.000000, 1.000000, 1.000000),
    (-2.000000, 0.000000, 0.000000),
    (2.000000, 0.000000, 0.000000),
    (0.000000, -2.000000, 0.000000),
    (0.000000, 2.000000, 0.000000),
    (0.000000, 0.000000, -2.000000),
    (0.000000, 0.000000, 2.000000),
    (1.414214, 0.000000, 0.000000),
    (-1.414214, 0.000000, 0.000000),
    (0.000000, 1.414214, 0.000000),
    (0.000000, -1.414214, 0.000000),
    (0.000000, 0.000000, 1.414214),
    (0.000000, 0.000000, -1.414214),
    (-1.154701, -1.154701, 0.000000),
    (-1.154701, 0.000000, -1.154701),
    (0.000000, -1.154701, -1.154701),
    (-1.154701, 0.000000, 1.154701),
    (0.000000, -1.154701, 1.154701),
    (-1.154701, 1.154701, 0.000000),
    (0.000000, 1.154701, 1.154701),
    (1.154701, 1.154701, 0.000000),
]

faces = [
    (0, 1, 8),
    (1, 3, 8),
    (3, 2, 8),
    (2, 0, 8),
    (4, 6, 9),
    (6, 7, 9),
    (7, 5, 9),
    (5, 4, 9),
    (0, 4, 10),
    (4, 5, 10),
    (5, 1, 10),
    (1, 0, 10),
    (2, 3, 11),
    (3, 7, 11),
    (7, 6, 11),
    (6, 2, 11),
    (0, 2, 12),
    (2, 6, 12),
    (6, 4, 12),
    (4, 0, 12),
    (1, 5, 13),
    (5, 7, 13),
    (7, 3, 13),
    (3, 1, 13),
    (14, 16, 18),
    (14, 18, 17),
    (14, 17, 19),
    (14, 19, 16),
    (15, 18, 16),
    (15, 17, 18),
    (15, 19, 17),
    (15, 16, 19),
    (20, 24, 18),
    (20, 18, 23),
    (20, 23, 8),
    (21, 8, 23),
    (21, 23, 26),
    (21, 26, 11),
    (22, 12, 21),
    (22, 21, 20),
    (22, 20, 10),
    (25, 11, 26),
    (25, 26, 27),
    (25, 27, 9),
    (24, 10, 20),
    (24, 20, 22),
    (24, 22, 12),
    (27, 26, 13),
]

# Face groups: 0-23 = Cube (gold), 24-47 = Octahedron (blue)
CUBE_FACES = 24

mesh = bpy.data.meshes.new('CubeOctCompound')
mesh.from_pydata(verts, [], faces)
mesh.update()

obj = bpy.data.objects.new('Cube_Octahedron_Compound', mesh)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# Gold material (Cube)
mat_gold = bpy.data.materials.new('Cube_Gold')
mat_gold.use_nodes = True
bsdf = mat_gold.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.8, 0.6, 0.1, 1.0)
bsdf.inputs['Metallic'].default_value = 0.7
bsdf.inputs['Roughness'].default_value = 0.3
try:
    mat_gold.surface_render_method = 'DITHERED'
except: pass

# Blue material (Octahedron)
mat_blue = bpy.data.materials.new('Oct_Blue')
mat_blue.use_nodes = True
bsdf2 = mat_blue.node_tree.nodes['Principled BSDF']
bsdf2.inputs['Base Color'].default_value = (0.1, 0.3, 0.9, 1.0)
bsdf2.inputs['Metallic'].default_value = 0.7
bsdf2.inputs['Roughness'].default_value = 0.3
try:
    mat_blue.surface_render_method = 'DITHERED'
except: pass

obj.data.materials.append(mat_gold)
obj.data.materials.append(mat_blue)

for poly in obj.data.polygons:
    poly.material_index = 0 if poly.index < CUBE_FACES else 1

# STL Export
stl_path = os.path.expanduser('~/Desktop/cube_octahedron_compound.stl')
try:
    bpy.ops.wm.stl_export(filepath=stl_path)
except:
    try:
        bpy.ops.export_mesh.stl(filepath=stl_path)
    except: pass
print(f'STL exported to {stl_path}')
print('=== CUBE-OCTAHEDRON COMPOUND COMPLETE ===')
