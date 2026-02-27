import bpy
import math
import os

# =====================================================
# STELLATED ICO-DOD COMPOUND — DODECAHEDRAL LATTICE
# 1 center + 12 surrounding = 13 total
# Equal circumsphere: all 32 tips at R=3.840881
# Satellites arranged at icosahedral vertex positions
# (= dodecahedral face centers = touching-sphere lattice)
# Each sphere touches its neighbors exactly at one point
# =====================================================

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=True)

phi = (1 + math.sqrt(5)) / 2
DOD_TIP_SCALE = 3.840881 / 2.731550  # equal circumsphere correction

# ===== BASE GEOMETRY =====
verts_raw = [
    (-0.8090169944, -0.8090169944, -0.8090169944),
    (-0.8090169944, -0.8090169944,  0.8090169944),
    (-0.8090169944,  0.8090169944, -0.8090169944),
    (-0.8090169944,  0.8090169944,  0.8090169944),
    ( 0.8090169944, -0.8090169944, -0.8090169944),
    ( 0.8090169944, -0.8090169944,  0.8090169944),
    ( 0.8090169944,  0.8090169944, -0.8090169944),
    ( 0.8090169944,  0.8090169944,  0.8090169944),
    ( 0.0,          -1.3090169944, -0.5         ),
    (-0.5,           0.0,          -1.3090169944),
    (-1.3090169944, -0.5,           0.0         ),
    ( 0.0,          -1.3090169944,  0.5         ),
    ( 0.5,           0.0,          -1.3090169944),
    (-1.3090169944,  0.5,           0.0         ),
    ( 0.0,           1.3090169944, -0.5         ),
    (-0.5,           0.0,           1.3090169944),
    ( 1.3090169944, -0.5,           0.0         ),
    ( 0.0,           1.3090169944,  0.5         ),
    ( 0.5,           0.0,           1.3090169944),
    ( 1.3090169944,  0.5,           0.0         ),
    ( 0.0,           1.4360610050,  2.3235955160),
    ( 2.3235955160,  0.0,           1.4360610050),
    ( 1.4360610050,  2.3235955160,  0.0         ),
    ( 0.0,          -1.4360610050,  2.3235955160),
    ( 2.3235955160,  0.0,          -1.4360610050),
    (-2.3235955160,  0.0,           1.4360610050),
    (-2.3235955160,  0.0,          -1.4360610050),
    ( 0.0,          -1.4360610050, -2.3235955160),
    (-1.4360610050, -2.3235955160,  0.0         ),
    ( 0.0,           1.4360610050, -2.3235955160),
    (-1.4360610050,  2.3235955160,  0.0         ),
    ( 1.4360610050, -2.3235955160,  0.0         ),
    ( 0.0,          -0.8090169944, -1.3090169944),
    (-1.3090169944,  0.0,          -0.8090169944),
    (-0.8090169944, -1.3090169944,  0.0         ),
    ( 0.0,          -0.8090169944,  1.3090169944),
    ( 1.3090169944,  0.0,          -0.8090169944),
    (-0.8090169944,  1.3090169944,  0.0         ),
    ( 0.0,           0.8090169944, -1.3090169944),
    (-1.3090169944,  0.0,           0.8090169944),
    ( 0.8090169944, -1.3090169944,  0.0         ),
    ( 0.0,           0.8090169944,  1.3090169944),
    ( 1.3090169944,  0.0,           0.8090169944),
    ( 0.8090169944,  1.3090169944,  0.0         ),
    ( 2.2175339577, -2.2175339577, -2.2175339577),
    ( 1.3705113571,  0.0,           3.5880453148),
    (-3.5880453148,  1.3705113571,  0.0         ),
    ( 3.5880453148,  1.3705113571,  0.0         ),
    ( 0.0,           3.5880453148, -1.3705113571),
    (-1.3705113571,  0.0,          -3.5880453148),
    (-1.3705113571,  0.0,           3.5880453148),
    (-2.2175339577,  2.2175339577,  2.2175339577),
    ( 2.2175339577, -2.2175339577,  2.2175339577),
    (-2.2175339577,  2.2175339577, -2.2175339577),
    ( 3.5880453148, -1.3705113571,  0.0         ),
    (-2.2175339577, -2.2175339577, -2.2175339577),
    (-3.5880453148, -1.3705113571,  0.0         ),
    ( 0.0,          -3.5880453148,  1.3705113571),
    ( 2.2175339577,  2.2175339577,  2.2175339577),
    ( 1.3705113571,  0.0,          -3.5880453148),
    ( 0.0,           3.5880453148,  1.3705113571),
    ( 2.2175339577,  2.2175339577, -2.2175339577),
    (-2.2175339577, -2.2175339577,  2.2175339577),
    ( 0.0,          -3.5880453148, -1.3705113571),
]

verts = []
for i, v in enumerate(verts_raw):
    if 20 <= i <= 31:
        verts.append((v[0]*DOD_TIP_SCALE, v[1]*DOD_TIP_SCALE, v[2]*DOD_TIP_SCALE))
    else:
        verts.append(v)

faces = [
    (3,15,20),(15,18,20),(18,7,20),(7,17,20),(17,3,20),
    (5,16,21),(16,19,21),(19,7,21),(7,18,21),(18,5,21),
    (6,14,22),(14,17,22),(17,7,22),(7,19,22),(19,6,22),
    (1,11,23),(11,5,23),(5,18,23),(18,15,23),(15,1,23),
    (4,12,24),(12,6,24),(6,19,24),(19,16,24),(16,4,24),
    (1,25,10),(10,25,13),(13,25,3),(3,25,15),(15,25,1),
    (0,26,9),(9,26,2),(2,26,13),(13,26,10),(10,26,0),
    (0,27,8),(8,27,4),(4,27,12),(12,27,9),(9,27,0),
    (0,8,28),(8,11,28),(11,1,28),(1,10,28),(10,0,28),
    (2,29,9),(9,29,12),(12,29,6),(6,29,14),(14,29,2),
    (2,13,30),(13,3,30),(3,17,30),(17,14,30),(14,2,30),
    (4,31,8),(8,31,11),(11,31,5),(5,31,16),(16,31,4),
    (32,36,44),(36,40,44),(40,32,44),
    (35,45,41),(41,45,42),(42,45,35),
    (33,46,37),(37,46,39),(39,46,33),
    (36,47,42),(42,47,43),(43,47,36),
    (37,48,38),(38,48,43),(43,48,37),
    (32,33,49),(33,38,49),(38,32,49),
    (35,50,39),(39,50,41),(41,50,35),
    (37,39,51),(39,41,51),(41,37,51),
    (35,40,52),(40,42,52),(42,35,52),
    (33,37,53),(37,38,53),(38,33,53),
    (36,54,40),(40,54,42),(42,54,36),
    (32,55,33),(33,55,34),(34,55,32),
    (33,34,56),(34,39,56),(39,33,56),
    (34,57,35),(35,57,40),(40,57,34),
    (41,42,58),(42,43,58),(43,41,58),
    (32,59,36),(36,59,38),(38,59,32),
    (37,41,60),(41,43,60),(43,37,60),
    (36,38,61),(38,43,61),(43,36,61),
    (34,35,62),(35,39,62),(39,34,62),
    (32,63,34),(34,63,40),(40,63,32),
]

def make_material(name, r, g, b, metallic=0.4, roughness=0.2):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (r, g, b, 1.0)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    return mat

mat_dod_center = make_material("DOD_Gold_Center", 1.0, 0.84, 0.0)
mat_ico_center = make_material("ICO_Blue_Center", 0.2, 0.5, 1.0)
mat_dod_sat    = make_material("DOD_Gold_Sat",    1.0, 0.75, 0.1, metallic=0.6)
mat_ico_sat    = make_material("ICO_Violet_Sat",  0.6, 0.2,  1.0, metallic=0.6)

R = 3.840881
lattice_dist = 2.0 * R

ico_raw = [
    (0, 1, phi), (0, -1, phi), (0, 1, -phi), (0, -1, -phi),
    (1, phi, 0), (-1, phi, 0), (1, -phi, 0), (-1, -phi, 0),
    (phi, 0, 1), (phi, 0, -1), (-phi, 0, 1), (-phi, 0, -1),
]
satellite_centers = []
for v in ico_raw:
    r = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    satellite_centers.append(tuple(c / r * lattice_dist for c in v))

def build_stelly(name, offset, mat_dod, mat_ico):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = offset
    obj.data.materials.append(mat_dod)
    obj.data.materials.append(mat_ico)
    for i, poly in enumerate(obj.data.polygons):
        poly.material_index = 0 if i < 60 else 1
    return obj

build_stelly("Stelly_Center", (0, 0, 0), mat_dod_center, mat_ico_center)
for i, center in enumerate(satellite_centers):
    build_stelly(f"Stelly_Sat_{i+1:02d}", center, mat_dod_sat, mat_ico_sat)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.shade_flat()
bpy.ops.object.select_all(action='DESELECT')

bpy.ops.object.select_all(action='SELECT')
stl_path = os.path.expanduser('~/Desktop/stelly_dodecahedral_lattice_13.stl')
try:
    bpy.ops.wm.stl_export(filepath=stl_path, export_selected_objects=True)
except:
    bpy.ops.export_mesh.stl(filepath=stl_path, use_selection=True)
bpy.ops.object.select_all(action='DESELECT')

print(f'STL exported: {stl_path}')
print('=== DODECAHEDRAL LATTICE COMPLETE ===')
print(f'1 center + 12 satellites = 13 stellated compounds')
print(f'Each circumsphere R = {R:.4f} units')
print(f'Satellite spacing = {lattice_dist:.4f} units (touching spheres)')
print(f'Equal circumsphere: all 32 tips at R = {R:.4f}')
