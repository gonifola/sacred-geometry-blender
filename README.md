# 🕈 Sacred Geometry — Blender Scripts & 3D-Printable STLs

**φ-derived polyhedra, Kepler-Poinsot star compounds, stellated solids, and sacred form generators.**  
Paste into Blender's Text Editor → Run Script → Export STL → Print.

---

## 🔹 v0.3.0 — Agentic API + 4 New Geometries

**The `/design` API is live.** Agents and humans can now submit a geometry spec and receive a manufacturable Blender script + STL instructions for **$0.10/call**.

```bash
# Example: agent requests a Merkaba
curl -X POST https://your-railway-url/design \
  -H "Content-Type: application/json" \
  -d '{"geometry": "merkaba", "material": "crystal", "budget": 0.10}'
```

---

## Models

### ⬟ Stellated Icosahedron-Dodecahedron Compound
The dual compound of two Platonic solids, stellated so every face becomes a spike — 60 gold dodecahedral pyramids interpenetrating 60 violet icosahedral pyramids, sharing a common midsphere.

| Script | Colors | Faces |
|--------|--------|-------|
| `stellated_dual_compound.py` | Gold + Blue | 120 |
| `stellated_compound_violet_gold.py` | Gold + Violet | 120 |
| `stellated_compound_inverted.py` | Inverted color mapping | 120 |
| `stellated_compound_short_spikes.py` | Short spike variant | 120 |
| `stellated_compound_cool_shape.py` | Poke-stellated (visual) | variable |

### 🕇 Star Mother (3-Shell)
Dan Winter's recursive nested icosahedron-dodecahedron structure — three concentric shells scaled by φ (golden ratio). Each shell is a dual compound; together they form the Star Mother geometry central to implosion physics.

| Script | Description |
|--------|-------------|
| `star_mother_3shell.py` | 3 nested ico-dodec shells, φ-scaled |

### 🔵 Sacred Form Suite (v0.3.0)

| Script | Description | Materials |
|--------|-------------|----------|
| `sri_yantra.py` | 9 interlocking triangles around bindu — Shiva/Shakti duality | Gold + Crimson + Crystal |
| `merkaba.py` | Star Tetrahedron — two interlocked tetrahedra + energy field tori | Gold + Crystal |
| `fibonacci_spiral.py` | 3D Fibonacci growth spiral, 144 nodes, phi-scaled | Obsidian→Crystal→Gold gradient |
| `torus_knot.py` | Parametric (p,q) torus knot — change `KNOT_P`/`KNOT_Q` for any knot type | Gold / Crystal / Obsidian |

### 🔷 Platonic Solid Compounds
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

## /design API (v0.3.0)

Agents and developers can call the `/design` endpoint to receive a geometry script URL for any supported form.

```bash
# List supported geometries
curl https://your-railway-url/geometries

# Request a design
curl -X POST https://your-railway-url/design \
  -H "Content-Type: application/json" \
  -d '{
    "geometry": "sri_yantra",
    "material": "gold",
    "params": {},
    "budget": 0.10
  }'
```

**Supported geometries:** `sri_yantra`, `merkaba`, `fibonacci_spiral`, `torus_knot`, `star_mother`, `stellated_dual`, `nested_platonic`, `cube_octahedron`

**Materials:** `gold` · `crystal` · `obsidian` · `violet` · `crimson`

**Price:** $0.10/call

### Deploy to Railway
```bash
cd design_api
railway up
```

---

## The Math

Every vertex is derived from the golden ratio φ = (1+√5)/2 ≈ 1.618.

- **Dodecahedron vertices**: permutations of (±1, ±1, ±1) and (0, ±1/φ, ±φ)
- **Icosahedron vertices**: permutations of (0, ±1, ±φ)
- **Stellated tips**: face centroids extended by φ² along face normals
- **Star Mother shells**: each successive shell scaled by φ from the previous
- **Fibonacci spiral**: golden angle (≈137.5°) step, phi-scaled radius growth

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
