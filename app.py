from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from rapidfuzz import process

app = Flask(__name__)
CORS(app)

# ================= IMPORT =================
try:
    from ai_matching import match_worker
    from payment_ai import verify_receipt
except ImportError:
    def match_worker(lat, lng, cat, worker_list=[]):
        return [{"name": "Test Worker", "distance": 1.2, "rating": 4.8}]
    
    def verify_receipt(path):
        return {"status": "success"}

# ================= TEST MODE =================
TEST_MODE = True

fake_db = {
    "workers": [
        {"name": "Ahmed", "category": "plumber"},
        {"name": "Sara", "category": "electrician"},
        {"name": "Mohamed", "category": "plumber"}
    ],
    "categories": ["plumber", "electrician", "carpenter"],
    "services": []
}

DATA_API = "https://servigo-ai-api-production.up.railway.app/api/all-data"

CATEGORY_MAP = {
    "سباك": "plumber",
    "كهربائي": "electrician",
    "نجار": "carpenter"
}

# ================= CHAT =================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}
        user_message = data.get("message", "").lower().strip()

        if not user_message:
            return jsonify({"found": False})

        # عربي → إنجليزي
        for ar, en in CATEGORY_MAP.items():
            if ar in user_message:
                user_message = en
                break

        # مصدر الداتا
        if TEST_MODE:
            db = fake_db
        else:
            backend = requests.get(DATA_API)
            db = backend.json()

        workers = db.get("workers", [])
        categories = db.get("categories", [])

        # 🔍 matching
        best_cat = process.extractOne(user_message, categories) if categories else None

        # ✅ FIX: شيلنا شرط الـ score القاتل
        if not best_cat:
            return jsonify({"found": False})

        matched = best_cat[0]

        # 🔥 FIX: matching أقوى ومرن
        results = []
        for w in workers:
            cat = str(w.get("category", "")).lower().strip()

            if matched.lower() in cat or cat in matched.lower():
                results.append(w)

        return jsonify({
            "found": len(results) > 0,
            "matched": matched,
            "data": results
        })

    except Exception as e:
        print("CHAT ERROR:", e)
        return jsonify({"found": False})

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

        # لو مفيش عامل مناسب
        if not result:
            return jsonify({
                "success": False,
                "message": "No suitable worker found"
            })

        # رجوع أفضل عامل فقط
        return jsonify({
            "success": True,
            "best_worker": result
        })

    except Exception as e:
        print("MATCH ERROR:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
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
# ================= HOME =================
@app.route("/")
def home():
    return "API is running 🚀"

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6000))
    app.run(host="0.0.0.0", port=port)