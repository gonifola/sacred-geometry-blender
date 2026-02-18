# 🔯 Sacred Geometry — Blender Scripts & 3D-Printable STLs

**φ-derived polyhedra, Kepler-Poinsot star compounds, and stellated solids.**
Paste into Blender's Text Editor → Run Script → Export STL → Print.

---

## Models

### ⭐ Stellated Icosahedron-Dodecahedron Compound
The dual compound of two Platonic solids, stellated so every face becomes a spike — 60 gold dodecahedral pyramids interpenetrating 60 violet icosahedral pyramids, sharing a common midsphere.

| Script | Colors | Faces |
|--------|--------|-------|
| `stellated_dual_compound.py` | Gold + Blue | 120 |
| `stellated_compound_violet_gold.py` | Gold + Violet | 120 |
| `stellated_compound_inverted.py` | Inverted color mapping | 120 |
| `stellated_compound_short_spikes.py` | Short spike variant | 120 |
| `stellated_compound_cool_shape.py` | Poke-stellated (visual) | variable |

### 🔷 Star Mother (3-Shell)
Dan Winter's recursive nested icosahedron-dodecahedron structure — three concentric shells scaled by φ (golden ratio). Each shell is a dual compound; together they form the Star Mother geometry central to implosion physics.

| Script | Description |
|--------|-------------|
| `star_mother_3shell.py` | 3 nested ico-dodec shells, φ-scaled |

### 🧊 Platonic Solid Compounds
| Script | Description |
|--------|-------------|
| `nested_5_platonic_solids.py` | All 5 Platonic solids nested concentrically |
| `cube_octahedron_compound.py` | Cube-octahedron dual compound |

---

## Quick Start

```bash
# 1. Open Blender
# 2. Switch to Scripting workspace
# 3. Open or paste any .py file
# 4. Click ▶ Run Script (or Alt+P)
# 5. STL auto-exports to ~/Desktop/
```

All scripts clear the scene, build geometry from pre-computed φ-coordinates, assign materials, and export STL — zero dependencies beyond Blender.

---

## The Math

Every vertex is derived from the golden ratio φ = (1+√5)/2 ≈ 1.618.

- **Dodecahedron vertices**: permutations of (±1, ±1, ±1) and (0, ±1/φ, ±φ)
- **Icosahedron vertices**: permutations of (0, ±1, ±φ)
- **Stellated tips**: face centroids extended by φ² along face normals
- **Star Mother shells**: each successive shell scaled by φ from the previous

No runtime face-finding algorithms — all geometry is pre-computed offline with NumPy for speed and correctness.

---

## Print Settings

These models print well with:
- **Layer height**: 0.15–0.2mm
- **Infill**: 15–20%
- **Supports**: Yes (star compounds need them for overhanging spikes)
- **Scale**: Default exports are ~100mm diameter — scale as needed in your slicer

---

## License

MIT — use however you want. Credit appreciated but not required.

Made with φ and Python. 🐍
