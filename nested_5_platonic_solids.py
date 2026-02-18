# 5 Nested Platonic Solids — Star Mother Foundation
# Tetrahedron → Cube → Octahedron → Icosahedron → Dodecahedron
# All nested concentrically via phi-coordinate relationships
# All geometry pre-computed — single from_pydata call
import bpy, os

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=True)
for m in list(bpy.data.meshes): bpy.data.meshes.remove(m)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)

# 50 vertices, 80 faces
verts = [
    (2.0000000000, 2.0000000000, 2.0000000000),
    (2.0000000000, -2.0000000000, -2.0000000000),
    (-2.0000000000, 2.0000000000, -2.0000000000),
    (-2.0000000000, -2.0000000000, 2.0000000000),
    (2.0000000000, 0.0000000000, 0.0000000000),
    (-2.0000000000, 0.0000000000, 0.0000000000),
    (0.0000000000, 0.0000000000, 2.0000000000),
    (0.0000000000, 0.0000000000, -2.0000000000),
    (0.0000000000, 2.0000000000, 0.0000000000),
    (0.0000000000, -2.0000000000, 0.0000000000),
    (2.0000000000, 2.0000000000, 2.0000000000),
    (2.0000000000, 2.0000000000, -2.0000000000),
    (2.0000000000, -2.0000000000, 2.0000000000),
    (2.0000000000, -2.0000000000, -2.0000000000),
    (-2.0000000000, 2.0000000000, 2.0000000000),
    (-2.0000000000, 2.0000000000, -2.0000000000),
    (-2.0000000000, -2.0000000000, 2.0000000000),
    (-2.0000000000, -2.0000000000, -2.0000000000),
    (0.0000000000, 2.3416407865, 1.4472135955),
    (1.4472135955, 0.0000000000, 2.3416407865),
    (2.3416407865, 1.4472135955, 0.0000000000),
    (0.0000000000, 2.3416407865, -1.4472135955),
    (1.4472135955, 0.0000000000, -2.3416407865),
    (2.3416407865, -1.4472135955, 0.0000000000),
    (0.0000000000, -2.3416407865, 1.4472135955),
    (0.0000000000, -2.3416407865, -1.4472135955),
    (-1.4472135955, 0.0000000000, 2.3416407865),
    (-2.3416407865, 1.4472135955, 0.0000000000),
    (-1.4472135955, 0.0000000000, -2.3416407865),
    (-2.3416407865, -1.4472135955, 0.0000000000),
    (2.0000000000, 2.0000000000, 2.0000000000),
    (2.0000000000, 2.0000000000, -2.0000000000),
    (2.0000000000, -2.0000000000, 2.0000000000),
    (2.0000000000, -2.0000000000, -2.0000000000),
    (-2.0000000000, 2.0000000000, 2.0000000000),
    (-2.0000000000, 2.0000000000, -2.0000000000),
    (-2.0000000000, -2.0000000000, 2.0000000000),
    (-2.0000000000, -2.0000000000, -2.0000000000),
    (0.0000000000, 1.2360679775, 3.2360679775),
    (3.2360679775, 0.0000000000, 1.2360679775),
    (1.2360679775, 3.2360679775, 0.0000000000),
    (0.0000000000, 1.2360679775, -3.2360679775),
    (3.2360679775, 0.0000000000, -1.2360679775),
    (1.2360679775, -3.2360679775, 0.0000000000),
    (0.0000000000, -1.2360679775, 3.2360679775),
    (-3.2360679775, 0.0000000000, 1.2360679775),
    (-1.2360679775, 3.2360679775, 0.0000000000),
    (0.0000000000, -1.2360679775, -3.2360679775),
    (-3.2360679775, 0.0000000000, -1.2360679775),
    (-1.2360679775, -3.2360679775, 0.0000000000)
]

faces = [
    (0, 1, 2),
    (0, 3, 1),
    (0, 2, 3),
    (1, 3, 2),
    (4, 8, 6),
    (4, 6, 9),
    (4, 7, 8),
    (4, 9, 7),
    (5, 6, 8),
    (5, 9, 6),
    (5, 8, 7),
    (5, 7, 9),
    (10, 13, 11),
    (10, 12, 13),
    (14, 17, 16),
    (14, 15, 17),
    (10, 16, 12),
    (10, 14, 16),
    (11, 17, 15),
    (11, 13, 17),
    (10, 15, 14),
    (10, 11, 15),
    (12, 17, 13),
    (12, 16, 17),
    (18, 19, 20),
    (18, 26, 19),
    (18, 20, 21),
    (18, 21, 27),
    (18, 27, 26),
    (19, 23, 20),
    (19, 24, 23),
    (19, 26, 24),
    (20, 22, 21),
    (20, 23, 22),
    (21, 22, 28),
    (21, 28, 27),
    (22, 23, 25),
    (22, 25, 28),
    (23, 24, 25),
    (24, 29, 25),
    (24, 26, 29),
    (25, 29, 28),
    (26, 27, 29),
    (27, 28, 29),
    (30, 34, 38),
    (30, 46, 34),
    (30, 40, 46),
    (30, 38, 44),
    (30, 44, 32),
    (30, 32, 39),
    (30, 39, 42),
    (30, 42, 31),
    (30, 31, 40),
    (31, 46, 40),
    (31, 35, 46),
    (31, 41, 35),
    (31, 47, 41),
    (31, 33, 47),
    (31, 42, 33),
    (32, 42, 39),
    (32, 33, 42),
    (32, 43, 33),
    (32, 49, 43),
    (32, 36, 49),
    (32, 44, 36),
    (33, 37, 47),
    (33, 49, 37),
    (33, 43, 49),
    (34, 44, 38),
    (34, 36, 44),
    (34, 45, 36),
    (34, 46, 35),
    (34, 35, 48),
    (34, 48, 45),
    (35, 37, 48),
    (35, 47, 37),
    (35, 41, 47),
    (36, 37, 49),
    (36, 48, 37),
    (36, 45, 48)
]

face_mats = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

mesh = bpy.data.meshes.new('NestedPlatonics')
mesh.from_pydata(verts, [], faces)
mesh.update(calc_edges=True)
mesh.validate(verbose=True)

obj = bpy.data.objects.new('Nested_5_Platonic_Solids', mesh)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# 5 materials with transparency (inner solids visible through outer)
mat = bpy.data.materials.new('Tetrahedron')
mat.use_nodes = True
bs = mat.node_tree.nodes['Principled BSDF']
bs.inputs['Base Color'].default_value = (0.9, 0.15, 0.15, 1.0)
bs.inputs['Alpha'].default_value = 0.4
bs.inputs['Metallic'].default_value = 0.2
try:
    mat.surface_render_method = 'BLENDED'
except:
    try:
        mat.blend_method = 'BLEND'
    except: pass
obj.data.materials.append(mat)

mat = bpy.data.materials.new('Octahedron')
mat.use_nodes = True
bs = mat.node_tree.nodes['Principled BSDF']
bs.inputs['Base Color'].default_value = (1.0, 0.55, 0.0, 1.0)
bs.inputs['Alpha'].default_value = 0.4
bs.inputs['Metallic'].default_value = 0.2
try:
    mat.surface_render_method = 'BLENDED'
except:
    try:
        mat.blend_method = 'BLEND'
    except: pass
obj.data.materials.append(mat)

mat = bpy.data.materials.new('Cube')
mat.use_nodes = True
bs = mat.node_tree.nodes['Principled BSDF']
bs.inputs['Base Color'].default_value = (1.0, 0.9, 0.1, 1.0)
bs.inputs['Alpha'].default_value = 0.4
bs.inputs['Metallic'].default_value = 0.2
try:
    mat.surface_render_method = 'BLENDED'
except:
    try:
        mat.blend_method = 'BLEND'
    except: pass
obj.data.materials.append(mat)

mat = bpy.data.materials.new('Icosahedron')
mat.use_nodes = True
bs = mat.node_tree.nodes['Principled BSDF']
bs.inputs['Base Color'].default_value = (0.1, 0.7, 0.3, 1.0)
bs.inputs['Alpha'].default_value = 0.4
bs.inputs['Metallic'].default_value = 0.2
try:
    mat.surface_render_method = 'BLENDED'
except:
    try:
        mat.blend_method = 'BLEND'
    except: pass
obj.data.materials.append(mat)

mat = bpy.data.materials.new('Dodecahedron')
mat.use_nodes = True
bs = mat.node_tree.nodes['Principled BSDF']
bs.inputs['Base Color'].default_value = (0.2, 0.4, 1.0, 1.0)
bs.inputs['Alpha'].default_value = 0.4
bs.inputs['Metallic'].default_value = 0.2
try:
    mat.surface_render_method = 'BLENDED'
except:
    try:
        mat.blend_method = 'BLEND'
    except: pass
obj.data.materials.append(mat)

for i, poly in enumerate(obj.data.polygons):
    poly.material_index = face_mats[i]

bpy.ops.object.shade_flat()

bpy.ops.object.light_add(type='SUN', energy=3, location=(5, 5, 10))

stl_path = os.path.expanduser('~/Desktop/nested_5_platonic_solids.stl')
try:
    bpy.ops.wm.stl_export(filepath=stl_path)
except:
    try:
        bpy.ops.export_mesh.stl(filepath=stl_path)
    except:
        print('STL export skipped')

print('=== 5 NESTED PLATONIC SOLIDS ===')
print('Verts: 50, Faces: 80')
print('Red    = Tetrahedron   (innermost, 4 faces)')
print('Orange = Octahedron    (6 verts = cube face centers)')
print('Yellow = Cube          (8 verts = dodecahedron subset)')
print('Green  = Icosahedron   (12 verts = dodecahedron face centers)')
print('Blue   = Dodecahedron  (outermost, 20 verts)')
print('STL -> ~/Desktop/nested_5_platonic_solids.stl')