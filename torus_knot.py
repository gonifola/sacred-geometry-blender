"""Torus Knot — (p,q) parametric knot wound around a torus.
Blender script: paste into Text Editor → Run Script → STL auto-exports.
Includes gold, crystal, and obsidian material presets.
Change KNOT_P and KNOT_Q for different knot types:
  (2,3) = Trefoil  (3,5) = Cinquefoil  (2,5) = Pentafoil
Zero runtime dependencies beyond Blender."""
import bpy, math, bmesh
from mathutils import Vector

# --- CONFIG ---
KNOT_P = 2       # wraps around torus axis
KNOT_Q = 3       # wraps through torus hole
MAJOR_R = 1.0    # torus major radius
MINOR_R = 0.35   # torus minor radius
TUBE_R  = 0.045  # knot tube radius
N_STEPS = 512    # resolution
MATERIAL = 'gold'  # 'gold' | 'crystal' | 'obsidian'

GOLD = (1.0, 0.843, 0.0, 1.0)
CRYSTAL = (0.75, 0.93, 1.0, 0.55)
OBSIDIAN = (0.04, 0.04, 0.07, 1.0)

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

def torus_knot_points(p, q, R, r, n):
    """Parametric (p,q) torus knot points."""
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        phi = t * p
        theta = t * q
        x = (R + r * math.cos(phi)) * math.cos(theta)
        y = (R + r * math.cos(phi)) * math.sin(theta)
        z = r * math.sin(phi)
        pts.append(Vector((x, y, z)))
    return pts

def build_torus_knot():
    if MATERIAL == 'gold':
        mat = make_material('TKGold', GOLD, metallic=0.95, roughness=0.1)
    elif MATERIAL == 'crystal':
        mat = make_material('TKCrystal', CRYSTAL, metallic=0.0, roughness=0.05, alpha=0.55)
    else:
        mat = make_material('TKObsidian', OBSIDIAN, metallic=0.9, roughness=0.08)

    points = torus_knot_points(KNOT_P, KNOT_Q, MAJOR_R, MINOR_R, N_STEPS)

    # Build curve
    curve_data = bpy.data.curves.new(f'TorusKnot_p{KNOT_P}q{KNOT_Q}', type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = TUBE_R
    curve_data.bevel_resolution = 8
    curve_data.use_fill_caps = True

    spline = curve_data.splines.new('NURBS')
    spline.points.add(len(points))  # +1 for closure
    for i, pt in enumerate(points):
        spline.points[i].co = (pt.x, pt.y, pt.z, 1)
    # Close the knot
    spline.points[-1].co = spline.points[0].co
    spline.use_cyclic_u = True

    curve_obj = bpy.data.objects.new(f'TorusKnot_p{KNOT_P}q{KNOT_Q}', curve_data)
    bpy.context.collection.objects.link(curve_obj)
    curve_obj.data.materials.append(mat)

    # Optional ghost torus for context
    ghost_mat = make_material('GhostTorus', (0.3, 0.3, 0.5, 1.0), metallic=0.0, roughness=0.8, alpha=0.18)
    ghost_mat.blend_method = 'BLEND'
    bpy.ops.mesh.primitive_torus_add(
        major_radius=MAJOR_R,
        minor_radius=MINOR_R,
        location=(0, 0, 0)
    )
    ghost = bpy.context.active_object
    ghost.name = 'GhostTorus'
    ghost.data.materials.append(ghost_mat)

clear_scene()
build_torus_knot()

import os
path = os.path.expanduser(f'~/Desktop/torus_knot_p{KNOT_P}q{KNOT_Q}.stl')
bpy.ops.export_mesh.stl(filepath=path, use_mesh_modifiers=True)
print(f'STL exported → {path}')
