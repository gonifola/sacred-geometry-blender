"""Fibonacci Spiral — 3D growth spiral with phi-derived point distribution.
Blender script: paste into Text Editor → Run Script → STL auto-exports.
Sphere cluster along golden-angle spiral arm. Tube spine option included.
Zero runtime dependencies beyond Blender."""
import bpy, math, bmesh
from mathutils import Vector

GOLD = (1.0, 0.843, 0.0, 1.0)
CRYSTAL = (0.8, 0.95, 1.0, 0.5)
GREEN = (0.1, 0.8, 0.3, 1.0)
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

def fibonacci_spiral_points(n=233, c=0.12, rise_per_turn=0.08):
    """Generate 3D Fibonacci spiral using golden angle."""
    golden_angle = math.pi * (3 - math.sqrt(5))  # ~137.508 degrees
    points = []
    for i in range(n):
        r = c * math.sqrt(i)
        theta = i * golden_angle
        z = i * rise_per_turn / n
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        points.append(Vector((x, y, z)))
    return points

def build_fibonacci_spiral():
    phi = (1 + math.sqrt(5)) / 2

    gold_mat = make_material('FibGold', GOLD, metallic=0.9, roughness=0.12)
    crystal_mat = make_material('FibCrystal', CRYSTAL, metallic=0.0, roughness=0.05, alpha=0.5)
    green_mat = make_material('FibGreen', GREEN, metallic=0.1, roughness=0.6)
    obs_mat = make_material('FibObsidian', OBSIDIAN, metallic=0.85, roughness=0.08)

    n_points = 144  # Fibonacci number
    points = fibonacci_spiral_points(n=n_points, c=0.15, rise_per_turn=1.2)

    # Sphere at each Fibonacci point (size grows with phi)
    for i, pt in enumerate(points):
        r_sphere = 0.012 + (i / n_points) * 0.028
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=r_sphere,
            segments=8, ring_count=6,
            location=pt
        )
        sp = bpy.context.active_object
        sp.name = f'FibNode_{i:03d}'
        # Color gradient: obsidian→gold as spiral grows
        if i < n_points * 0.33:
            sp.data.materials.append(obs_mat)
        elif i < n_points * 0.66:
            sp.data.materials.append(crystal_mat)
        else:
            sp.data.materials.append(gold_mat)

    # Spine curve through all points
    curve_data = bpy.data.curves.new('FibSpine', type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = 0.006
    curve_data.bevel_resolution = 4
    spline = curve_data.splines.new('NURBS')
    spline.points.add(len(points) - 1)
    for i, pt in enumerate(points):
        spline.points[i].co = (pt.x, pt.y, pt.z, 1)
    curve_obj = bpy.data.objects.new('FibSpine', curve_data)
    bpy.context.collection.objects.link(curve_obj)
    curve_obj.data.materials.append(green_mat)

    # Center marker
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.025, location=(0, 0, 0))
    center = bpy.context.active_object
    center.name = 'FibCenter'
    center.data.materials.append(gold_mat)

clear_scene()
build_fibonacci_spiral()

import os
path = os.path.expanduser('~/Desktop/fibonacci_spiral.stl')
bpy.ops.export_mesh.stl(filepath=path, use_mesh_modifiers=True)
print(f'STL exported → {path}')
