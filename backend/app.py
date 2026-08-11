from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import traceback
from feature import extract_features, is_safelisted_domain
app = Flask(__name__)
CORS(app)
try:
    model = joblib.load("rf_model.pkl")
    print("Random Forest berhasil dimuat")
except Exception as e:
    print("Gagal memuat rf_model.pkl")
    print(e)
    model = None
try:
    selected_features = joblib.load("selected_features.pkl")
    print(f"Selected Features berhasil dimuat ({len(selected_features)} fitur)")
except Exception as e:
    print("Gagal memuat selected_features.pkl")
    print(e)
    selected_features = None
@app.route("/")
def home():
    return jsonify({
        "message": "Backend Sistem Deteksi URL Phishing Berjalan"
    })
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request tidak valid."}), 400
        url = data.get("url", "").strip()
        if url == "":
            return jsonify({"error": "URL tidak boleh kosong."}), 400
        if is_safelisted_domain(url):
            features = extract_features(url)
            df = pd.DataFrame([features])
            if selected_features is not None:
                df = df[selected_features]
            model_proba = model.predict_proba(df)[0].tolist() if model is not None else None
            return jsonify({
                "result": "Website Aman",
                "catatan": (
                    "Domain terverifikasi resmi (.ac.id) melalui safelist "
                    "rule-based, bukan hasil murni model Random Forest."
                ),
                "model_probability_raw": model_proba
            })
        features = extract_features(url)
        df = pd.DataFrame([features])
        if selected_features is not None:
            missing = []
            for f in selected_features:
                if f not in df.columns:
                    missing.append(f)
            if len(missing) > 0:
                return jsonify({
                    "error": "Fitur berikut tidak ditemukan.",
                    "missing": missing
                }), 500
            df = df[selected_features]
        prediction = model.predict(df)[0]
        proba = model.predict_proba(df)[0]

        if prediction == 0:
            result = "Website Aman"
        else:
            result = "Website Phishing"
        return jsonify({"result": result})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)