[4/26/2026 8:39 PM] Mariem Gamil: from flask import Flask, request, jsonify

app = Flask(name)

@app.route("/", methods=["GET"])
def home():
    return "Servigo API is running 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    return jsonify({
        "reply": f"Received: {message}"
    })

if name == "main":
    app.run(host="0.0.0.0", port=6000)
[4/26/2026 8:47 PM] Mariem Gamil: from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from rapidfuzz import process

app = Flask(name)
CORS(app)

# ================= IMPORT YOUR MODULES =================
try:
    from ai_matching import match_worker
    from payment_ai import verify_receipt
except ImportError:
    def match_worker(lat, lng, cat, worker_list=[]):
        return [{"name": "Test Worker", "distance": 1.2, "rating": 4.8}]
    
    def verify_receipt(p):
        return {"status": "success", "message": "Test Mode Active"}

# ================= CHAT / AI MATCHING =================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    return jsonify({
        "reply": f"Received: {message}"
    })

# ================= MATCH =================
@app.route("/match", methods=["POST"])
def match():
    data = request.json

    result = match_worker(
        float(data.get("lat", 0)),
        float(data.get("lng", 0)),
        data.get("category", ""),
        data.get("worker_list", [])
    )

    return jsonify(result)

# ================= VERIFY PAYMENT =================
@app.route("/verify_payment", methods=["POST"])
def verify_payment():
    if "image" not in request.files:
        return jsonify({"error": "No image"}), 400

    file = request.files["image"]
    path = "receipt.jpg"
    file.save(path)

    result = verify_receipt(path)

    if os.path.exists(path):
        os.remove(path)

    return jsonify(result)

# ================= RUN =================
if name == "main":
    port = int(os.environ.get("PORT", 6000))
    app.run(host="0.0.0.0", port=port)
