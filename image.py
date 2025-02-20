import cv2
import pandas as pd
from datetime import datetime
from deepface import DeepFace
from tkinter import Tk, filedialog
import numpy as np

# Gerekli kütüphaneleri yüklediğinizden emin olun
# pip install opencv-python pandas deepface

# 📂 CSV dosyasının adı
csv_file = "duygu_gunlugu.csv"

# 📝 Eğer CSV dosyası yoksa başlıkları ekleyerek oluştur
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Tarih", "Duygu"])
    df.to_csv(csv_file, index=False)

# 📸 Kullanıcıdan görsel seçmesini iste
Tk().withdraw()  # Tkinter penceresini gizle
image_path = filedialog.askopenfilename(title="Bir fotoğraf seçin", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

if not image_path:
    print("Görsel seçilmedi! Lütfen bir görsel seçin.")
else:
    # 📸 Görüntüyü yükle
    image = cv2.imread(image_path)
    if image is None:
        print("Görsel yüklenemedi! Lütfen doğru dosya yolunu kontrol edin.")
    else:
        # 🔍 Görüntüyü gri tonlamaya çevir ve yüz tespiti yap
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(50, 50))

        if len(faces) == 0:
            print("Yüz algılanamadı! Lütfen yüzün net olduğu bir fotoğraf seçin.")
        else:
            for (x, y, w, h) in faces:
                face = image[y:y + h, x:x + w]  # Yüz bölgesini al

                try:
                    # 🎭 Duygu analizi yap
                    analysis = DeepFace.analyze(face, actions=['emotion'], enforce_detection=True)
                    dominant_emotion = analysis[0]['dominant_emotion']

                    # 📝 Yeni veriyi CSV'ye ekle
                    new_data = pd.DataFrame([[datetime.now(), dominant_emotion]], columns=["Tarih", "Duygu"])
                    new_data.to_csv(csv_file, mode='a', header=False, index=False)

                    # 🎭 Sonucu ekrana yazdır
                    print(f"Tespit Edilen Duygu: {dominant_emotion}")
                except Exception as e:
                    print(f"Hata: {e}")
