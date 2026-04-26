from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from rapidfuzz import process

app = Flask(__name__)
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
    try:
        data = request.json or {}
        user_message = data.get("message", "").lower()

        # 🧠 mapping بسيط
        if "سباك" in user_message or "plumber" in user_message:
            matched = "plumber"
        elif "كهربائي" in user_message or "electrician" in user_message:
            matched = "electrician"
        else:
            return jsonify({
                "found": False,
                "message": "مفيش نتائج"
            })

        # 📦 dummy data (مؤقت لحد ما نوصل الداتا الحقيقية)
        workers = [
            {"name": "Ahmed", "rating": 4.8, "distance": 1.2},
            {"name": "Ali", "rating": 4.5, "distance": 2.0}
        ]

        return jsonify({
            "found": True,
            "matched": matched,
            "data": workers
        })

    except Exception as e:
        return jsonify({
            "found": False,
            "error": str(e)
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
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6000))
    app.run(host="0.0.0.0", port=port)
