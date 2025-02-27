from flask import Flask, render_template, request, jsonify
import cv2
import pandas as pd
from datetime import datetime
from deepface import DeepFace
from io import BytesIO
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 📂 CSV dosyasının adı
csv_file = "duygu_gunlugu.csv"

# 📝 Eğer CSV dosyası yoksa başlıkları ekleyerek oluştur
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Tarih", "Duygu"])
    df.to_csv(csv_file, index=False)

# Upload klasörü
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Dosya uzantısını kontrol et
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ana sayfa
@app.route('/')
def index():
    return render_template('mood_analysis.htm')

# Duygu analizi
@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form.get("text")
    image = request.files.get("image")
    
    # Metin analizi
    positiveWords = ['mutlu', 'harika', 'sevgi', 'teşekkür', 'güzel', 'neşeli', 'başarılı', 'umut']
    negativeWords = ['üzgün', 'kötü', 'nefret', 'sinirli', 'korku', 'yalnız', 'kaygı', 'pişman']

    positiveCount = 0
    negativeCount = 0

    if text:
        for word in text.split():
            if word.lower() in positiveWords:
                positiveCount += 1
            if word.lower() in negativeWords:
                negativeCount += 1

    mood = 'Nötr'
    if positiveCount > negativeCount:
        mood = 'Olumlu 😊'
    elif negativeCount > positiveCount:
        mood = 'Olumsuz 😢'

    # Fotoğraf analizi
    imageEmotion = "N/A"
    if image and allowed_file(image.filename):
        img = image.read()
        img_array = np.asarray(bytearray(img), dtype=np.uint8)
        image = cv2.imdecode(img_array, -1)
        # 🎭 Görüntü analizi
        try:
            print("Fotoğraf analizi başlıyor...")
            analysis = DeepFace.analyze(image, actions=['emotion'], enforce_detection=True)
            print("Fotoğraf analizi tamamlandı:", analysis)
            imageEmotion = analysis[0]['dominant_emotion']
        except Exception as e:
            print("Hata oluştu:", e)
            imageEmotion = f"Yüz analizi hatası: {e}"

    # Sonuçları döndür
    return jsonify({
        "mood": mood,
        "positiveCount": positiveCount,
        "negativeCount": negativeCount,
        "imageEmotion": imageEmotion
    })

if __name__ == '__main__':
    app.run(debug=True)
