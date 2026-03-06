"""Merkaba — Star Tetrahedron (two interlocked tetrahedra).
Blender script: paste into Text Editor → Run Script → STL auto-exports.
Gold upward tetrahedron (Shiva/masculine), crystal downward (Shakti/feminine).
Phi-derived scale. Zero runtime dependencies beyond Blender."""
import bpy, math, bmesh
from mathutils import Vector, Matrix

GOLD = (1.0, 0.843, 0.0, 1.0)
CRYSTAL = (0.7, 0.9, 1.0, 0.55)
OBSIDIAN = (0.04, 0.04, 0.07, 1.0)
VIOLET = (0.5, 0.0, 0.9, 1.0)

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

def tetrahedron_verts(scale=1.0, invert=False):
    """Unit tetrahedron vertices, optionally inverted (apex down)."""
    s = scale
    if not invert:
        verts = [
            Vector((0, 0, s)),
            Vector((math.sqrt(8/9)*s, 0, -s/3)),
            Vector((-math.sqrt(2/9)*s, math.sqrt(2/3)*s, -s/3)),
            Vector((-math.sqrt(2/9)*s, -math.sqrt(2/3)*s, -s/3)),
        ]
    else:
        verts = [
            Vector((0, 0, -s)),
            Vector((math.sqrt(8/9)*s, 0, s/3)),
            Vector((-math.sqrt(2/9)*s, math.sqrt(2/3)*s, s/3)),
            Vector((-math.sqrt(2/9)*s, -math.sqrt(2/3)*s, s/3)),
        ]
    return verts

def create_tetra_mesh(name, verts, mat):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bv = [bm.verts.new(v) for v in verts]
    bm.faces.new([bv[0], bv[1], bv[2]])
    bm.faces.new([bv[0], bv[2], bv[3]])
    bm.faces.new([bv[0], bv[3], bv[1]])
    bm.faces.new([bv[1], bv[3], bv[2]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.validate()
    obj.data.materials.append(mat)
    return obj

def build_merkaba():
    phi = (1 + math.sqrt(5)) / 2
    scale = 1.0

    gold_mat = make_material('MerkGold', GOLD, metallic=0.95, roughness=0.1)
    crystal_mat = make_material('MerkCrystal', CRYSTAL, metallic=0.0, roughness=0.05, alpha=0.55)
    violet_mat = make_material('MerkViolet', VIOLET, metallic=0.6, roughness=0.2)
    obsidian_mat = make_material('MerkObsidian', OBSIDIAN, metallic=0.85, roughness=0.08)

    # Upward tetrahedron — gold (masculine / Shiva)
    up_verts = tetrahedron_verts(scale=scale, invert=False)
    up_tetra = create_tetra_mesh('Tetra_Up_Gold', up_verts, gold_mat)

    # Downward tetrahedron — crystal (feminine / Shakti)
    down_verts = tetrahedron_verts(scale=scale, invert=True)
    down_tetra = create_tetra_mesh('Tetra_Down_Crystal', down_verts, crystal_mat)

    # Outer energy field torus (phi-scaled)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=scale * phi * 0.88,
        minor_radius=scale * 0.03,
        location=(0, 0, 0)
    )
    torus_h = bpy.context.active_object
    torus_h.name = 'EnergyField_H'
    torus_h.data.materials.append(violet_mat)

    # Vertical torus (perpendicular)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=scale * phi * 0.88,
        minor_radius=scale * 0.03,
        location=(0, 0, 0)
    )
    torus_v = bpy.context.active_object
    torus_v.name = 'EnergyField_V'
    torus_v.rotation_euler = (math.radians(90), 0, 0)
    torus_v.data.materials.append(obsidian_mat)

    # Central sphere (soul)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=scale * 0.04, location=(0, 0, 0))
    soul = bpy.context.active_object
    soul.name = 'SoulSphere'
    soul.data.materials.append(gold_mat)

def build():
    clear_scene()
    build_merkaba()
    import os
    path = os.path.expanduser('~/Desktop/merkaba.stl')
    bpy.ops.export_mesh.stl(filepath=path, use_mesh_modifiers=True)
    print(f'STL exported → {path}')

build()
