# 📘 Panduan Menggunakan config.py

File `config.py` adalah **pusat konfigurasi** untuk sistem sortir kopi. Semua parameter dapat disesuaikan di sini tanpa menyentuh kode utama `Yolo.py`.

---

## 🎯 Keuntungan Menggunakan config.py

✅ **Mudah disesuaikan** - Semua setting di satu tempat  
✅ **Tidak merusak kode** - Edit parameter tanpa risiko error  
✅ **Dokumentasi jelas** - Setiap parameter ada penjelasan  
✅ **Reusable** - Bisa buat multiple config untuk testing  
✅ **Team-friendly** - Mudah share setting antar developer  

---

## 📋 Struktur config.py

### 1. **SERIAL_CONFIG** - Komunikasi dengan ESP32

```python
SERIAL_CONFIG = {
    'port': 'COM3',          # Port ESP32
    'baudrate': 115200,      # Kecepatan komunikasi
    'timeout': 1             # Timeout (detik)
}
```

**Kapan diubah:**
- Ganti `port` jika ESP32 di port lain (cek Device Manager)
- Windows: `COM3`, `COM4`, dll
- Linux: `/dev/ttyUSB0`, `/dev/ttyACM0`

---

### 2. **CAMERA_CONFIG** - Setting Kamera

```python
CAMERA_CONFIG = {
    'index': 0,              # 0=default, 1/2=eksternal
    'width': 640,            # Resolusi lebar
    'height': 480,           # Resolusi tinggi
    'fps': 30                # Target FPS
}
```

**Kapan diubah:**
- `index`: Jika kamera tidak terdeteksi, coba 1 atau 2
- `width/height`: Sesuaikan dengan kemampuan kamera
  - 640x480 (VGA) - standar, cepat
  - 1280x720 (HD) - lebih detail, lebih lambat
  - 1920x1080 (Full HD) - detail maksimal, butuh GPU

---

### 3. **YOLO_CONFIG** - Model AI

```python
YOLO_CONFIG = {
    'model_path': 'yolov8n.pt',  # File model
    'confidence': 0.5,            # Threshold (0.0-1.0)
    'device': 'cpu',              # 'cpu' atau 'cuda'
    'verbose': False              # Show detail inference
}
```

**Kapan diubah:**
- `model_path`: Ganti dengan model custom Anda
  - `'yolov8n.pt'` - Nano (paling cepat, akurasi standar)
  - `'yolov8s.pt'` - Small (balance)
  - `'yolov8m.pt'` - Medium (lebih akurat, lebih lambat)
  - `'best.pt'` - Model custom hasil training
  
- `confidence`: Sesuaikan sensitivitas
  - `0.3` - Lebih sensitif (banyak deteksi, banyak false positive)
  - `0.5` - Standar (balance)
  - `0.7` - Lebih strict (sedikit deteksi, lebih akurat)
  
- `device`: 
  - `'cpu'` - Untuk komputer tanpa GPU NVIDIA
  - `'cuda'` - Jika punya GPU NVIDIA (10x lebih cepat!)

---

### 4. **ROI_CONFIG** - Area Deteksi

```python
ROI_CONFIG = {
    'x_start_percent': 0.3,  # 30% dari kiri
    'x_end_percent': 0.7,    # 70% dari kiri
    'y_start_percent': 0.3,  # 30% dari atas
    'y_end_percent': 0.7     # 70% dari atas
}
```

**Visualisasi:**
```
┌─────────────────────────────┐
│                             │ ← 0% (atas)
│     ┌───────────────┐       │
│ 30% │   ROI AREA    │ 70%   │ ← Area deteksi
│     │  (Tengah)     │       │
│     └───────────────┘       │
│                             │ ← 100% (bawah)
└─────────────────────────────┘
  30%                   70%
```

**Kapan diubah:**
- Jika kamera terlalu dekat/jauh dari konveyor
- Jika biji kopi lewat di pinggir frame

**Contoh penyesuaian:**
```python
# ROI lebih lebar (20%-80%)
'x_start_percent': 0.2,
'x_end_percent': 0.8,

# ROI lebih sempit (40%-60%)
'x_start_percent': 0.4,
'x_end_percent': 0.6,

# ROI di bagian bawah frame
'y_start_percent': 0.5,
'y_end_percent': 0.9,
```

---

### 5. **DETECTION_CONFIG** - Parameter Deteksi

```python
DETECTION_CONFIG = {
    'cooldown': 1.0,         # Detik antar deteksi
    'min_area': 100,         # Minimum area (pixels²)
    'max_area': 50000        # Maximum area (pixels²)
}
```

**Kapan diubah:**
- `cooldown`: Sesuaikan dengan kecepatan konveyor
  - Konveyor cepat: `0.5` detik
  - Konveyor lambat: `2.0` detik
  - Formula: `cooldown = jarak_kamera_ke_IR / kecepatan_konveyor`
  
- `min_area`: Filter objek terlalu kecil (noise)
  - Biji kopi kecil: `50`
  - Biji kopi besar: `200`
  
- `max_area`: Filter objek terlalu besar (tangan, dll)
  - Sesuaikan dengan ukuran biji kopi maksimal

---

### 6. **CLASSIFICATION_CONFIG** - Klasifikasi Kualitas

```python
CLASSIFICATION_CONFIG = {
    'mode': 'placeholder',   # 'placeholder' atau 'custom'
    'classes': {
        'bagus': ['bagus', 'good', 'grade_a'],
        'cacat': ['cacat', 'defect', 'bad']
    },
    'placeholder_threshold': 0.7
}
```

**Mode Placeholder (Default):**
- Menggunakan confidence threshold
- Confidence > 0.7 = BAGUS
- Confidence ≤ 0.7 = CACAT
- **Gunakan untuk testing tanpa model custom**

**Mode Custom (Setelah Training):**
```python
'mode': 'custom',  # ← Ubah ke 'custom'
'classes': {
    'bagus': ['bagus', 'good', 'kopi_bagus'],  # ← Sesuaikan dengan class name model Anda
    'cacat': ['cacat', 'defect', 'kopi_cacat']
}
```

---

### 7. **DISPLAY_CONFIG** - Tampilan Window

```python
DISPLAY_CONFIG = {
    'show_window': True,     # Tampilkan preview
    'show_fps': True,        # Tampilkan FPS
    'show_roi': True,        # Tampilkan ROI box
    'show_stats': True,      # Tampilkan statistik
    'window_name': 'Sistem Sortir Kopi - YOLO Detection'
}
```

**Kapan diubah:**
- `show_window`: Set `False` jika running di server tanpa display
- `show_fps`: Set `False` untuk performa lebih baik
- `show_roi`: Set `False` setelah kalibrasi selesai

---

### 8. **LOGGING_CONFIG** - Log File

```python
LOGGING_CONFIG = {
    'enabled': True,
    'level': 'INFO',         # DEBUG, INFO, WARNING, ERROR
    'file': 'sortir_kopi.log',
    'format': '%(asctime)s - %(levelname)s - %(message)s'
}
```

**Level logging:**
- `DEBUG` - Semua detail (untuk debugging)
- `INFO` - Informasi penting (default)
- `WARNING` - Hanya warning & error
- `ERROR` - Hanya error

**Kapan diubah:**
- Set `enabled: False` untuk disable logging
- Ubah `level` ke `DEBUG` saat troubleshooting
- Ubah `file` untuk custom log path

---

### 9. **COLORS** - Warna Visualisasi

```python
COLORS = {
    'roi': (0, 255, 255),        # Kuning
    'bagus': (0, 255, 0),        # Hijau
    'cacat': (0, 0, 255),        # Merah
    'cooldown': (128, 128, 128), # Abu-abu
    'outside_roi': (200, 200, 200),
    'text': (255, 255, 255)      # Putih
}
```

**Format:** BGR (Blue, Green, Red) untuk OpenCV

**Contoh warna:**
- Merah: `(0, 0, 255)`
- Hijau: `(0, 255, 0)`
- Biru: `(255, 0, 0)`
- Kuning: `(0, 255, 255)`
- Putih: `(255, 255, 255)`
- Hitam: `(0, 0, 0)`

---

## 🔧 Contoh Skenario Penyesuaian

### Skenario 1: Ganti COM Port

```python
# config.py
SERIAL_CONFIG = {
    'port': 'COM5',  # ← Ubah dari COM3 ke COM5
    'baudrate': 115200,
    'timeout': 1
}
```

### Skenario 2: Gunakan GPU untuk Performa Lebih Cepat

```python
# config.py
YOLO_CONFIG = {
    'model_path': 'yolov8n.pt',
    'confidence': 0.5,
    'device': 'cuda',  # ← Ubah dari 'cpu' ke 'cuda'
    'verbose': False
}
```

### Skenario 3: ROI Lebih Lebar (Kamera Jauh)

```python
# config.py
ROI_CONFIG = {
    'x_start_percent': 0.2,  # ← Lebih lebar (20%-80%)
    'x_end_percent': 0.8,
    'y_start_percent': 0.2,
    'y_end_percent': 0.8
}
```

### Skenario 4: Konveyor Lebih Cepat

```python
# config.py
DETECTION_CONFIG = {
    'cooldown': 0.5,  # ← Kurangi cooldown jadi 0.5 detik
    'min_area': 100,
    'max_area': 50000
}
```

### Skenario 5: Gunakan Model Custom

```python
# config.py
YOLO_CONFIG = {
    'model_path': 'models/kopi_best.pt',  # ← Path ke model custom
    'confidence': 0.6,  # ← Sesuaikan threshold
    'device': 'cpu',
    'verbose': False
}

CLASSIFICATION_CONFIG = {
    'mode': 'custom',  # ← Ubah ke custom
    'classes': {
        'bagus': ['kopi_bagus', 'grade_a'],  # ← Sesuaikan class name
        'cacat': ['kopi_cacat', 'grade_c']
    }
}
```

### Skenario 6: Running di Server (Tanpa Display)

```python
# config.py
DISPLAY_CONFIG = {
    'show_window': False,  # ← Disable window
    'show_fps': False,
    'show_roi': False,
    'show_stats': False,
    'window_name': 'Sistem Sortir Kopi'
}
```

---

## 🚀 Cara Menggunakan

### 1. Edit config.py
```bash
# Buka dengan text editor
notepad config.py  # Windows
nano config.py     # Linux
```

### 2. Ubah parameter yang diinginkan
```python
# Contoh: Ganti COM port
SERIAL_CONFIG = {
    'port': 'COM5',  # ← Edit di sini
    ...
}
```

### 3. Simpan file

### 4. Jalankan sistem
```bash
python Yolo.py
```

### 5. Lihat konfigurasi yang digunakan
Saat program start, akan tampil:
```
============================================================
KONFIGURASI SISTEM (dari config.py)
============================================================
Serial Port      : COM5
Camera Index     : 0
Resolution       : 640x480
YOLO Model       : yolov8n.pt
Confidence       : 0.5
ROI Area         : 30%-70% (X), 30%-70% (Y)
Detection Cooldown: 1.0s
Classification   : placeholder
Logging          : Enabled
============================================================
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'config'"

**Penyebab:** File `config.py` tidak ada di folder yang sama dengan `Yolo.py`

**Solusi:**
```bash
# Pastikan struktur folder:
├── Yolo.py
├── config.py  ← Harus ada di sini
├── Sortir.cpp
└── ...
```

### Error: "NameError: name 'SERIAL_CONFIG' is not defined"

**Penyebab:** Syntax error di `config.py`

**Solusi:** Cek syntax Python (indentasi, tanda kurung, koma)

---

## 📝 Tips & Best Practices

1. **Backup config.py** sebelum edit besar
   ```bash
   cp config.py config.py.backup
   ```

2. **Buat multiple config** untuk testing
   ```python
   # config_testing.py
   # config_production.py
   
   # Import sesuai kebutuhan:
   from config_testing import *
   ```

3. **Dokumentasikan perubahan**
   ```python
   # config.py
   SERIAL_CONFIG = {
       'port': 'COM5',  # Diubah dari COM3 karena ESP32 pindah port
       ...
   }
   ```

4. **Test satu parameter per waktu**
   - Ubah satu setting
   - Test
   - Jika berhasil, lanjut ke setting berikutnya

5. **Gunakan version control** (Git)
   ```bash
   git add config.py
   git commit -m "Update ROI area untuk kamera baru"
   ```

---

## ✅ Checklist Konfigurasi Awal

Sebelum running pertama kali:

- [ ] Set `SERIAL_CONFIG['port']` sesuai ESP32 Anda
- [ ] Set `CAMERA_CONFIG['index']` sesuai kamera Anda
- [ ] Pastikan `YOLO_CONFIG['model_path']` ada (akan auto-download jika belum)
- [ ] Sesuaikan `ROI_CONFIG` dengan posisi kamera
- [ ] Set `DETECTION_CONFIG['cooldown']` sesuai kecepatan konveyor
- [ ] Pilih `CLASSIFICATION_CONFIG['mode']` (placeholder atau custom)
- [ ] Enable/disable `DISPLAY_CONFIG` sesuai kebutuhan
- [ ] Set `LOGGING_CONFIG['level']` untuk debugging

---

## 📞 Need Help?

Jika ada pertanyaan tentang parameter tertentu:
1. Baca komentar di `config.py`
2. Lihat contoh skenario di atas
3. Cek log file: `sortir_kopi.log`
4. Test dengan nilai default dulu

---

**Happy Configuring! 🎉**
