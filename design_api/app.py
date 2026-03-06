"""OmniCAD /design API — v0.3.0
Agents and humans submit a design spec; receive a Blender Python script
that generates the requested sacred geometry STL.

POST /design
  body: { "geometry": str, "material": str, "params": dict, "budget": float }
  returns: { "script_url": str, "geometry": str, "material": str, "price_usd": float }

Revenue model: $0.10 per /design call (agents pay tolls to get a physical form).
Deploy to Railway: https://railway.app
"""
from flask import Flask, request, jsonify, abort
import os, json, base64, hashlib, time

app = Flask(__name__)

# --- Supported geometries ---
SUPPORTED_GEOMETRIES = {
    "sri_yantra":       "sri_yantra.py",
    "merkaba":          "merkaba.py",
    "fibonacci_spiral": "fibonacci_spiral.py",
    "torus_knot":       "torus_knot.py",
    "star_mother":      "star_mother_3shell.py",
    "stellated_dual":   "stellated_dual_compound.py",
    "nested_platonic":  "nested_5_platonic_solids.py",
    "cube_octahedron":  "cube_octahedron_compound.py",
}

SUPPORTED_MATERIALS = ["gold", "crystal", "obsidian", "violet", "crimson"]

PRICE_USD = 0.10  # per call
REPO_RAW_BASE = "https://raw.githubusercontent.com/gonifola/sacred-geometry-blender/main"
AUTH_TOKEN = os.environ.get("OMNICAD_AUTH_TOKEN", "")  # optional bearer auth


def _check_auth():
    """Optional bearer token auth. Skip if AUTH_TOKEN env not set."""
    if not AUTH_TOKEN:
        return
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer ") or auth_header[7:] != AUTH_TOKEN:
        abort(401, description="Invalid or missing auth token")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": "0.3.0"})


@app.route("/geometries", methods=["GET"])
def list_geometries():
    """List supported geometry types and materials."""
    return jsonify({
        "geometries": list(SUPPORTED_GEOMETRIES.keys()),
        "materials": SUPPORTED_MATERIALS,
        "price_usd_per_call": PRICE_USD,
    })


@app.route("/design", methods=["POST"])
def design():
    """
    Submit a design request. Returns script URL + metadata.
    Body (JSON):
      geometry  (str, required): one of SUPPORTED_GEOMETRIES
      material  (str, optional): gold | crystal | obsidian | violet | crimson
      params    (dict, optional): geometry-specific overrides
      budget    (float, optional): caller's budget in USD
    """
    _check_auth()

    body = request.get_json(silent=True) or {}
    geometry = body.get("geometry", "").lower().strip()
    material  = body.get("material", "gold").lower().strip()
    params    = body.get("params", {})
    budget    = float(body.get("budget", PRICE_USD))

    # Validate geometry
    if geometry not in SUPPORTED_GEOMETRIES:
        return jsonify({
            "error": f"Unknown geometry '{geometry}'. Supported: {list(SUPPORTED_GEOMETRIES.keys())}"
        }), 400

    # Validate material
    if material not in SUPPORTED_MATERIALS:
        material = "gold"  # safe default

    # Budget check
    if budget < PRICE_USD:
        return jsonify({
            "error": f"Insufficient budget. Minimum: ${PRICE_USD:.2f}",
            "required_usd": PRICE_USD,
        }), 402

    script_file = SUPPORTED_GEOMETRIES[geometry]
    script_url = f"{REPO_RAW_BASE}/{script_file}"

    # Log (simple stdout for Railway logs)
    call_id = hashlib.sha256(f"{geometry}{material}{time.time()}".encode()).hexdigest()[:12]
    print(f"[design] call_id={call_id} geometry={geometry} material={material} params={params}")

    response = {
        "call_id":      call_id,
        "geometry":     geometry,
        "material":     material,
        "script_url":   script_url,
        "params_applied": params,
        "price_usd":    PRICE_USD,
        "instructions": (
            "1. Open Blender. "
            "2. Switch to Scripting workspace. "
            f"3. Fetch {script_url} and paste into Text Editor. "
            "4. Click ▶ Run Script. "
            "5. STL exports to ~/Desktop/."
        ),
    }
    return jsonify(response), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
