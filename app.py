from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ================= AI IMPORT =================
try:
    from ai_matching import match_worker
    from payment_ai import verify_receipt
except:
    def match_worker(lat, lng, cat, worker_list=[]):
        return [{"name": "Test Worker", "distance": 1.2, "rating": 4.8}]

    def verify_receipt(path):
        return {"status": "success", "message": "Test Mode"}

# ================= HOME =================
@app.route("/")
def home():
    return "API is running 🚀"

# ================= CHAT =================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    msg = data.get("message", "").lower()

    if "كهربائي" in msg:
        workers = [
            {"name": "Ali", "cat": "electrician", "rating": 4.9},
            {"name": "Sara", "cat": "electrician", "rating": 4.7}
        ]

        return jsonify({
            "found": True,
            "data": workers
        })

    elif "سباك" in msg:
        workers = [
            {"name": "Ahmed", "cat": "plumber", "rating": 4.8},
            {"name": "Mohamed", "cat": "plumber", "rating": 4.6}
        ]

        return jsonify({
            "found": True,
            "data": workers
        })

    else:
        return jsonify({
            "found": False,
            "data": []
        })

# ================= MATCH =================
@app.route("/match", methods=["POST"])
def match():
    try:
        data = request.get_json()

        result = match_worker(
            float(data.get("lat", 0)),
            float(data.get("lng", 0)),
            data.get("category"),
            data.get("worker_list", [])
        )

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================= VERIFY =================
@app.route("/verify_payment", methods=["POST"])
def verify_payment_api():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image"}), 400

        file = request.files["image"]
        path = "receipt.jpg"
        file.save(path)

        result = verify_receipt(path)

        if os.path.exists(path):
            os.remove(path)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6000))
    app.run(host="0.0.0.0", port=port)