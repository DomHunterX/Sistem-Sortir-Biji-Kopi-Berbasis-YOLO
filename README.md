# 🤖 Sistem Sortir Biji Kopi Otomatis dengan YOLO & IoT

Sistem pemilah biji kopi otomatis menggunakan AI (YOLO) untuk deteksi kualitas dan ESP32 untuk kontrol mekanik dengan monitoring real-time via Blynk IoT Dashboard.

---

## 📋 Komponen Sistem

### Hardware:
- **ESP32** - Mikrokontroler utama
- **USB Webcam** - Kamera untuk deteksi YOLO
- **Sensor IR** - Deteksi fisik biji kopi di gerbang sortir
- **Servo SG90** - Aktuator gate pemilah
- **Motor DC + Driver L298N** - Konveyor belt
- **LCD I2C 16x2** - Display lokal
- **Power Supply 7.4** - Untuk motor dan driver

### Software:
- **Python 3.8+** - YOLO detection system
- **Arduino IDE / PlatformIO** - ESP32 programming
- **YOLOv8** - AI model untuk deteksi
- **Blynk IoT** - Dashboard monitoring

---

## 🔧 Instalasi

### 1. Setup Python Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Download model YOLO (otomatis saat pertama run)
# Model default: yolov8n.pt (nano - ringan & cepat)
```

### 2. Setup ESP32

**Library yang dibutuhkan (Arduino IDE):**
- `ESP32Servo` by Kevin Harrington
- `LiquidCrystal_I2C` by Frank de Brabander
- `Blynk` by Volodymyr Shymanskyy

**Cara install:**
1. Buka Arduino IDE
2. Tools → Manage Libraries
3. Cari dan install library di atas

### 3. Konfigurasi Blynk

1. **Buat akun di [Blynk.io](https://blynk.io)**
2. **Buat Template baru:**
   - Name: `Kopi Sorting`
   - Hardware: `ESP32`
3. **Tambahkan Datastreams:**
   - `V0` - Total (Integer, 0-9999)
   - `V1` - Bagus (Integer, 0-9999)
   - `V2` - Cacat (Integer, 0-9999)
   - `V3` - Status (String)
   - `V4` - Reset Button (Integer, 0-1)
4. **Buat Dashboard:**
   - Tambahkan 3 Label widgets untuk V0, V1, V2
   - Tambahkan 1 Label widget untuk V3 (status)
   - Tambahkan 1 Button widget untuk V4 (reset counter)
5. **Copy Auth Token** dari Device Info

### 4. Konfigurasi Kode

**Edit `Sortir.cpp`:**
```cpp
#define BLYNK_TEMPLATE_ID "TMPL_XXXXXXXX"  // Dari Blynk Console
#define BLYNK_AUTH_TOKEN "YOUR_TOKEN_HERE"  // Auth Token Anda

const char* ssid = "YOUR_WIFI_SSID";        // Nama WiFi
const char* password = "YOUR_WIFI_PASSWORD"; // Password WiFi
```

**Edit `Yolo.py` (jika perlu):**
```python
COM_PORT = 'COM3'  # Sesuaikan dengan port ESP32 Anda
CAMERA_INDEX = 0   # 0 = default, 1/2 = eksternal
```

---

## 🚀 Cara Menjalankan

### 1. Upload kode ke ESP32
```bash
# Via Arduino IDE:
# 1. Buka Sortir.cpp
# 2. Pilih Board: ESP32 Dev Module
# 3. Pilih Port yang sesuai
# 4. Upload
```

### 2. Jalankan sistem YOLO
```bash
python Yolo.py
```

### 3. Monitor via Blynk
- Buka aplikasi Blynk di smartphone/web
- Lihat real-time data: Total, Bagus, Cacat
- Gunakan tombol Reset untuk reset counter

---

## 📊 Alur Kerja Sistem

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEM SORTIR KOPI                        │
└─────────────────────────────────────────────────────────────┘

1. TITIK INSPEKSI (Kamera + YOLO)
   ├─ Kamera menangkap biji kopi di tengah konveyor
   ├─ YOLO mendeteksi & klasifikasi: BAGUS / CACAT
   └─ Python kirim flag ke ESP32 via Serial

2. PERJALANAN BIJI
   └─ Biji bergerak dari titik inspeksi → titik eksekusi

3. TITIK EKSEKUSI (IR Sensor + Servo)
   ├─ IR Sensor deteksi biji tiba di gerbang
   ├─ ESP32 cek flag terakhir dari YOLO:
   │  ├─ Flag CACAT → Servo buka gate → Buang
   │  └─ Flag BAGUS → Servo diam → Lewat
   └─ Update counter & kirim ke Blynk

4. MONITORING
   ├─ LCD: Tampil lokal (Total, Bagus, Cacat)
   └─ Blynk: Dashboard IoT real-time
```

---

## 🔌 Pin Mapping ESP32

| Komponen | Pin ESP32 | Keterangan |
|----------|-----------|------------|
| **Motor Driver L298N** |
| ENA | D14 | PWM speed control |
| IN1 | D26 | Direction 1 |
| IN2 | D27 | Direction 2 |
| **Sensor & Aktuator** |
| IR Sensor OUT | D30 | Deteksi biji di gerbang |
| Servo PWM | D13 | Kontrol gate |
| **LCD I2C** |
| SDA | D21 | Data line |
| SCL | D22 | Clock line |

---

## ⚙️ Konfigurasi & Tuning

### Kecepatan Konveyor
Edit di `Sortir.cpp`:
```cpp
analogWrite(ENA_PIN, 150); // 0-255, sesuaikan dengan mekanik
```

### Posisi Servo
```cpp
const int POSISI_NORMAL = 0;  // Gate tertutup (biji bagus lewat)
const int POSISI_BUANG = 90;  // Gate terbuka (biji cacat dibuang)
```

### ROI Detection (Area deteksi kamera)
Edit di `Yolo.py`:
```python
ROI_X_START = int(FRAME_WIDTH * 0.3)  # 30% dari kiri
ROI_X_END = int(FRAME_WIDTH * 0.7)    # 70% dari kiri
```

### Confidence Threshold
```python
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence (0.0 - 1.0)
```

### Detection Cooldown
```python
DETECTION_COOLDOWN = 1.0  # Detik antar pengiriman flag
```

---

## 🎯 Mengganti dengan Model Custom

**Saat ini sistem menggunakan model default YOLOv8 (person detection) sebagai placeholder.**

### Langkah Training Model Custom:

1. **Siapkan Dataset:**
   - Foto biji kopi bagus & cacat
   - Annotasi dengan [Roboflow](https://roboflow.com) atau [LabelImg](https://github.com/heartexlabs/labelImg)
   - Format: YOLO (txt files)

2. **Training:**
   ```python
   from ultralytics import YOLO
   
   # Load model
   model = YOLO('yolov8n.pt')
   
   # Train
   model.train(
       data='kopi_dataset.yaml',  # Path ke dataset config
       epochs=100,
       imgsz=640,
       batch=16
   )
   ```

3. **Export Model:**
   ```python
   model.export(format='onnx')  # atau 'torchscript', 'tflite'
   ```

4. **Update Kode:**
   Edit `Yolo.py`:
   ```python
   MODEL_PATH = 'path/to/your/best.pt'  # Model custom Anda
   ```

5. **Update Klasifikasi:**
   Edit fungsi `classify_quality()`:
   ```python
   def classify_quality(self, detection):
       class_name = self.model.names[int(detection.cls)]
       
       if class_name == "cacat":
           return "CACAT"
       elif class_name == "bagus":
           return "BAGUS"
       # Atau untuk 3 class:
       # elif class_name == "grade_a": return "GRADE_A"
       # elif class_name == "grade_b": return "GRADE_B"
       # elif class_name == "grade_c": return "GRADE_C"
   ```

---

## 🐛 Troubleshooting

### Python tidak bisa connect ke ESP32
```
❌ Error koneksi serial: [WinError 2] The system cannot find the file specified
```
**Solusi:**
- Cek COM port di Device Manager
- Update `COM_PORT` di `Yolo.py`
- Install driver CH340/CP2102 jika perlu

### Kamera tidak terdeteksi
```
❌ Error: Tidak dapat membuka kamera!
```
**Solusi:**
- Cek kamera terhubung (USB)
- Coba ubah `CAMERA_INDEX` (0, 1, atau 2)
- Test dengan aplikasi Camera Windows

### ESP32 tidak connect ke WiFi
**Solusi:**
- Pastikan SSID & password benar
- Cek jarak ke router (sinyal lemah)
- Gunakan WiFi 2.4GHz (bukan 5GHz)

### Blynk tidak connect
**Solusi:**
- Pastikan Auth Token benar
- Cek Template ID sudah sesuai
- Pastikan Datastream (V0-V4) sudah dibuat

### Servo tidak bergerak
**Solusi:**
- Cek koneksi pin D13
- Cek power supply servo (5V)
- Test manual: `servoGate.write(90);`

### IR Sensor tidak deteksi
**Solusi:**
- Cek koneksi pin D30
- Cek power sensor (3.3V/5V)
- Adjust sensitivitas sensor (potentiometer)
- Cek logika: active-low atau active-high

---

## 📈 Monitoring & Maintenance

### Via Serial Monitor (Debug)
```
=== SISTEM SORTIR KOPI OTOMATIS ===
WiFi Connected!
IP Address: 192.168.1.100
Blynk Connected!
=== SISTEM SIAP BEROPERASI ===

📥 Flag: CACAT Terdeteksi!
🔔 IR Sensor: Biji kopi terdeteksi di gerbang!
❌ Aksi: MEMBUANG biji cacat
📊 Total: 1 | Bagus: 0 | Cacat: 1
---
```

### Via LCD Display
```
┌────────────────┐
│ T:10 B:7       │
│ Cacat: 3       │
└────────────────┘
```

### Via Blynk Dashboard
- **Real-time counter** (Total, Bagus, Cacat)
- **Status sistem** (Deteksi: BAGUS/CACAT, Sistem Aktif)
- **Reset button** (Reset semua counter)

---

## 📝 Catatan Penting

1. **Timing Synchronization:**
   - Jarak kamera ke IR sensor harus konsisten
   - Kecepatan konveyor mempengaruhi akurasi
   - Sesuaikan `DETECTION_COOLDOWN` dengan kecepatan

2. **Lighting Condition:**
   - Pastikan pencahayaan stabil untuk deteksi YOLO
   - Hindari backlight atau shadow

3. **Mechanical Alignment:**
   - Pastikan servo gate align dengan jalur biji
   - Test timing servo (delay open/close)

4. **Power Management:**
   - Gunakan power supply terpisah untuk motor (12V)
   - ESP32 & sensor gunakan 5V/3.3V regulated

---

## 📞 Support

Jika ada pertanyaan atau issue:
1. Cek troubleshooting section di atas
2. Review serial monitor untuk error log
3. Test komponen satu per satu (isolasi masalah)

---

## 📄 License

Project ini untuk keperluan edukasi dan prototype.
Silakan modifikasi sesuai kebutuhan Anda.

---

**Dibuat dengan ❤️ untuk Sistem Sortir Kopi Otomatis**
