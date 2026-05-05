# 📝 Panduan Anotasi Dataset Biji Kopi untuk YOLO

Panduan lengkap untuk membuat dataset training YOLO dari foto biji kopi Anda.

---

## 🎯 Tujuan

Membuat dataset dengan 2 class:
- **bagus** - Biji kopi berkualitas baik
- **cacat** - Biji kopi cacat (pecah, hitam, berlubang, dll)

---

## 📊 Rekomendasi Jumlah Data

| Kategori | Minimum | Ideal | Excellent |
|----------|---------|-------|-----------|
| Training | 100 gambar | 300 gambar | 500+ gambar |
| Validation | 20 gambar | 50 gambar | 100+ gambar |
| Per Class | 50/50 split | Balanced | Balanced |

**Tips:**
- Lebih banyak data = model lebih akurat
- Pastikan jumlah class seimbang (50% bagus, 50% cacat)
- Foto dari berbagai angle, lighting, background

---

## 🌐 METODE 1: Roboflow (Recommended - Mudah & Cepat)

### Kelebihan:
✅ Berbasis web (tidak perlu install)  
✅ Auto-split train/val/test  
✅ Augmentasi otomatis  
✅ Export langsung ke format YOLO  
✅ Kolaborasi tim  

### Langkah-langkah:

#### 1. Setup Akun
1. Buka [https://roboflow.com](https://roboflow.com)
2. Sign up gratis (bisa pakai Google account)
3. Klik **"Create New Project"**

#### 2. Konfigurasi Project
```
Project Name: Kopi Sorting Dataset
Project Type: Object Detection
Annotation Group: kopi-quality
```

#### 3. Upload Gambar
1. Klik **"Upload"** → Pilih semua foto biji kopi Anda
2. Tunggu upload selesai
3. Roboflow akan auto-detect duplikat

**Tips Upload:**
- Format: JPG, PNG (max 10MB per file)
- Batch upload: bisa drag & drop folder
- Nama file: gunakan nama deskriptif (contoh: `bagus_001.jpg`, `cacat_001.jpg`)

#### 4. Anotasi (Labeling)

**Cara Anotasi:**
1. Klik gambar pertama
2. Pilih tool **"Bounding Box"** (kotak)
3. Klik & drag untuk membuat kotak di sekitar biji kopi
4. Pilih class: **bagus** atau **cacat**
5. Tekan **Enter** atau klik **"Save"**
6. Lanjut ke gambar berikutnya (tombol panah kanan)

**Shortcut Keyboard:**
- `B` - Bounding Box tool
- `Enter` - Save annotation
- `→` - Next image
- `←` - Previous image
- `Delete` - Hapus box yang dipilih

**Best Practices:**
- ✅ Kotak pas mengelilingi biji (tidak terlalu besar/kecil)
- ✅ Jika ada multiple biji dalam 1 foto, buat box untuk setiap biji
- ✅ Jangan include background terlalu banyak
- ❌ Jangan skip biji yang kecil/blur

**Contoh Anotasi:**
```
┌─────────────────────────────────┐
│                                 │
│    ┌──────┐                     │
│    │BAGUS │  ← Biji bagus       │
│    └──────┘                     │
│                                 │
│              ┌──────┐           │
│              │CACAT │  ← Cacat  │
│              └──────┘           │
└─────────────────────────────────┘
```

#### 5. Generate Dataset

Setelah semua gambar dianotasi:

1. Klik **"Generate"** (pojok kanan atas)
2. **Preprocessing:**
   ```
   ✅ Auto-Orient
   ✅ Resize: 640x640 (Stretch)
   ❌ Grayscale (biarkan color)
   ```

3. **Augmentation** (opsional, untuk perbanyak data):
   ```
   ✅ Flip: Horizontal
   ✅ Rotation: ±15°
   ✅ Brightness: ±15%
   ✅ Blur: Up to 1px
   ❌ Cutout (tidak perlu untuk biji kopi)
   ```
   
   **Multiplier:** 2x atau 3x (akan gandakan jumlah data)

4. **Train/Val/Test Split:**
   ```
   Train: 70%
   Valid: 20%
   Test: 10%
   ```

5. Klik **"Generate"**

#### 6. Export untuk YOLO

1. Klik **"Export"**
2. Format: **YOLOv8**
3. Pilih **"Download ZIP"**
4. Extract ZIP ke folder proyek Anda

**Struktur hasil download:**
```
kopi-dataset/
├── data.yaml          ← Config file (PENTING!)
├── train/
│   ├── images/
│   │   ├── img001.jpg
│   │   └── ...
│   └── labels/
│       ├── img001.txt
│       └── ...
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

#### 7. Verifikasi data.yaml

Buka `data.yaml`, pastikan isinya seperti ini:
```yaml
train: ../train/images
val: ../valid/images
test: ../test/images

nc: 2
names: ['bagus', 'cacat']
```

**Jika path tidak sesuai, edit manual:**
```yaml
# Gunakan absolute path
train: C:/Users/YourName/kopi-dataset/train/images
val: C:/Users/YourName/kopi-dataset/valid/images

nc: 2
names: ['bagus', 'cacat']
```

---

## 💻 METODE 2: LabelImg (Offline - Full Control)

### Kelebihan:
✅ Offline (tidak perlu internet)  
✅ Lebih cepat untuk dataset besar  
✅ Full control atas anotasi  
✅ Gratis & open source  

### Langkah-langkah:

#### 1. Install LabelImg

**Windows:**
```bash
# Install via pip
pip install labelImg

# Atau download executable:
# https://github.com/heartexlabs/labelImg/releases
```

**Verifikasi instalasi:**
```bash
labelImg
# Harus muncul GUI window
```

#### 2. Persiapan Folder

Buat struktur folder:
```
kopi-dataset/
├── images/           ← Taruh semua foto di sini
├── labels/           ← Hasil anotasi akan disimpan di sini
└── classes.txt       ← File class names
```

**Buat file `classes.txt`:**
```bash
# Windows PowerShell
echo "bagus`ncacat" > kopi-dataset/classes.txt

# Atau buat manual dengan Notepad:
# Isi:
# bagus
# cacat
```

#### 3. Jalankan LabelImg

```bash
labelImg kopi-dataset/images kopi-dataset/classes.txt
```

**Atau via GUI:**
1. Jalankan `labelImg`
2. **Open Dir** → Pilih folder `images`
3. **Change Save Dir** → Pilih folder `labels`
4. **View** → **Auto Save mode** (centang)
5. **PascalVOC** → Klik untuk ganti ke **YOLO**

#### 4. Anotasi

**Workflow:**
1. Klik **"Create RectBox"** (atau tekan `W`)
2. Klik & drag untuk buat kotak di sekitar biji
3. Pilih class: **bagus** atau **cacat**
4. Tekan `Ctrl+S` untuk save (atau auto-save)
5. Tekan `D` untuk next image

**Shortcut Keyboard:**
- `W` - Create bounding box
- `D` - Next image
- `A` - Previous image
- `Del` - Delete selected box
- `Ctrl+S` - Save
- `Ctrl+D` - Duplicate box
- `Ctrl++` - Zoom in
- `Ctrl+-` - Zoom out

**Tips:**
- Gunakan zoom untuk biji kecil
- Duplicate box (`Ctrl+D`) untuk biji dengan ukuran sama
- Verifikasi setiap anotasi sebelum next

#### 5. Verifikasi Hasil

Setelah anotasi selesai, cek folder `labels`:
```
labels/
├── img001.txt
├── img002.txt
└── ...
```

**Format file `.txt` (YOLO format):**
```
0 0.5 0.5 0.2 0.3
│ │   │   │   └─ height (normalized)
│ │   │   └───── width (normalized)
│ │   └───────── center_y (normalized)
│ └───────────── center_x (normalized)
└─────────────── class_id (0=bagus, 1=cacat)
```

**Contoh `img001.txt`:**
```
0 0.456 0.523 0.123 0.145
1 0.678 0.234 0.098 0.112
```
Artinya: 1 biji bagus + 1 biji cacat dalam gambar

#### 6. Split Dataset (Train/Val/Test)

Buat script Python untuk split otomatis:

**Buat file `split_dataset.py`:**
```python
import os
import shutil
import random
from pathlib import Path

# Konfigurasi
DATASET_DIR = "kopi-dataset"
TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
TEST_RATIO = 0.1

# Buat folder output
output_dirs = ['train', 'valid', 'test']
for split in output_dirs:
    os.makedirs(f"{DATASET_DIR}/{split}/images", exist_ok=True)
    os.makedirs(f"{DATASET_DIR}/{split}/labels", exist_ok=True)

# Ambil semua file gambar
images = list(Path(f"{DATASET_DIR}/images").glob("*.jpg")) + \
         list(Path(f"{DATASET_DIR}/images").glob("*.png"))

# Shuffle
random.seed(42)
random.shuffle(images)

# Split
total = len(images)
train_end = int(total * TRAIN_RATIO)
val_end = train_end + int(total * VAL_RATIO)

splits = {
    'train': images[:train_end],
    'valid': images[train_end:val_end],
    'test': images[val_end:]
}

# Copy files
for split_name, img_list in splits.items():
    print(f"\n{split_name.upper()}: {len(img_list)} images")
    for img_path in img_list:
        # Copy image
        shutil.copy(img_path, f"{DATASET_DIR}/{split_name}/images/")
        
        # Copy label
        label_path = Path(f"{DATASET_DIR}/labels/{img_path.stem}.txt")
        if label_path.exists():
            shutil.copy(label_path, f"{DATASET_DIR}/{split_name}/labels/")
        else:
            print(f"⚠️  Warning: Label not found for {img_path.name}")

print("\n✅ Dataset split completed!")
print(f"Train: {len(splits['train'])}")
print(f"Valid: {len(splits['valid'])}")
print(f"Test: {len(splits['test'])}")
```

**Jalankan:**
```bash
python split_dataset.py
```

#### 7. Buat data.yaml

**Buat file `kopi-dataset/data.yaml`:**
```yaml
# Dataset paths (gunakan absolute path)
train: C:/path/to/kopi-dataset/train/images
val: C:/path/to/kopi-dataset/valid/images
test: C:/path/to/kopi-dataset/test/images

# Number of classes
nc: 2

# Class names
names: ['bagus', 'cacat']
```

**Ganti path sesuai lokasi Anda!**

---

## ✅ Verifikasi Dataset

Sebelum training, pastikan dataset valid:

### 1. Cek Struktur Folder
```
kopi-dataset/
├── data.yaml
├── train/
│   ├── images/ (70% data)
│   └── labels/ (70% data)
├── valid/
│   ├── images/ (20% data)
│   └── labels/ (20% data)
└── test/
    ├── images/ (10% data)
    └── labels/ (10% data)
```

### 2. Cek Jumlah File

**Buat script `check_dataset.py`:**
```python
import os
from pathlib import Path

DATASET_DIR = "kopi-dataset"

for split in ['train', 'valid', 'test']:
    img_dir = Path(f"{DATASET_DIR}/{split}/images")
    lbl_dir = Path(f"{DATASET_DIR}/{split}/labels")
    
    images = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png"))
    labels = list(lbl_dir.glob("*.txt"))
    
    print(f"\n{split.upper()}:")
    print(f"  Images: {len(images)}")
    print(f"  Labels: {len(labels)}")
    
    if len(images) != len(labels):
        print(f"  ⚠️  WARNING: Mismatch! {len(images) - len(labels)} files missing")
    else:
        print(f"  ✅ OK")

# Cek class distribution
print("\n" + "="*50)
print("CLASS DISTRIBUTION:")
print("="*50)

class_counts = {'bagus': 0, 'cacat': 0}

for split in ['train', 'valid', 'test']:
    lbl_dir = Path(f"{DATASET_DIR}/{split}/labels")
    
    for label_file in lbl_dir.glob("*.txt"):
        with open(label_file, 'r') as f:
            for line in f:
                class_id = int(line.split()[0])
                if class_id == 0:
                    class_counts['bagus'] += 1
                elif class_id == 1:
                    class_counts['cacat'] += 1

print(f"Bagus: {class_counts['bagus']} instances")
print(f"Cacat: {class_counts['cacat']} instances")

total = sum(class_counts.values())
print(f"\nBalance:")
print(f"  Bagus: {class_counts['bagus']/total*100:.1f}%")
print(f"  Cacat: {class_counts['cacat']/total*100:.1f}%")

if abs(class_counts['bagus'] - class_counts['cacat']) / total > 0.3:
    print("⚠️  WARNING: Dataset imbalanced! Consider adding more data.")
else:
    print("✅ Dataset balanced!")
```

**Jalankan:**
```bash
python check_dataset.py
```

**Output yang diharapkan:**
```
TRAIN:
  Images: 210
  Labels: 210
  ✅ OK

VALID:
  Images: 60
  Labels: 60
  ✅ OK

TEST:
  Images: 30
  Labels: 30
  ✅ OK

==================================================
CLASS DISTRIBUTION:
==================================================
Bagus: 450 instances
Cacat: 430 instances

Balance:
  Bagus: 51.1%
  Cacat: 48.9%
✅ Dataset balanced!
```

### 3. Visualisasi Dataset (Opsional)

**Buat script `visualize_dataset.py`:**
```python
import cv2
import random
from pathlib import Path

DATASET_DIR = "kopi-dataset"
CLASS_NAMES = ['bagus', 'cacat']
COLORS = [(0, 255, 0), (0, 0, 255)]  # Green, Red

# Ambil random image dari train
img_dir = Path(f"{DATASET_DIR}/train/images")
images = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png"))
sample = random.choice(images)

# Load image
img = cv2.imread(str(sample))
h, w = img.shape[:2]

# Load label
label_path = Path(f"{DATASET_DIR}/train/labels/{sample.stem}.txt")

if label_path.exists():
    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center = float(parts[1]) * w
            y_center = float(parts[2]) * h
            width = float(parts[3]) * w
            height = float(parts[4]) * h
            
            # Convert to corner coordinates
            x1 = int(x_center - width/2)
            y1 = int(y_center - height/2)
            x2 = int(x_center + width/2)
            y2 = int(y_center + height/2)
            
            # Draw box
            color = COLORS[class_id]
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, CLASS_NAMES[class_id], (x1, y1-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

cv2.imshow("Sample Annotation", img)
print("Press any key to close...")
cv2.waitKey(0)
cv2.destroyAllWindows()
```

**Jalankan:**
```bash
python visualize_dataset.py
```

---

## 🎯 Tips Anotasi Berkualitas

### DO ✅
- Anotasi konsisten (semua biji, tidak skip)
- Bounding box pas (tidak terlalu besar/kecil)
- Foto dari berbagai angle & lighting
- Include biji di edge frame (partial visible)
- Foto dengan multiple biji per frame (lebih realistis)

### DON'T ❌
- Jangan anotasi biji yang blur/tidak jelas
- Jangan include terlalu banyak background
- Jangan skip biji kecil
- Jangan anotasi biji yang terpotong >50%
- Jangan foto dengan lighting ekstrem (terlalu gelap/terang)

### Best Practices
1. **Consistency:** Gunakan kriteria yang sama untuk semua anotasi
2. **Quality over Quantity:** 100 anotasi bagus > 500 anotasi asal-asalan
3. **Diverse Data:** Variasi background, lighting, angle
4. **Edge Cases:** Include biji yang sulit diklasifikasi (borderline)

---

## 📊 Checklist Sebelum Training

- [ ] Minimal 100 gambar (lebih banyak lebih baik)
- [ ] Semua gambar sudah dianotasi
- [ ] Dataset split (70/20/10)
- [ ] File `data.yaml` sudah benar
- [ ] Path di `data.yaml` absolute & valid
- [ ] Class distribution balanced (±50/50)
- [ ] Verifikasi dengan `check_dataset.py`
- [ ] Visualisasi sample dengan `visualize_dataset.py`

---

## 🚀 Next Steps

Setelah dataset siap:

1. **Training Model:**
   ```bash
   python train_model.py
   ```
   (Script training akan dibuat setelah dataset ready)

2. **Evaluasi Model:**
   - Cek metrics (mAP, precision, recall)
   - Test dengan gambar baru

3. **Integrasi ke Sistem:**
   - Update `config.py`
   - Test real-time detection

---

## 📞 Troubleshooting

### Roboflow: "Upload failed"
- Cek ukuran file (<10MB)
- Cek format (JPG/PNG)
- Coba upload batch lebih kecil

### LabelImg: "Cannot save"
- Pastikan folder `labels` exist
- Cek permission folder
- Pastikan format YOLO (bukan PascalVOC)

### Dataset: "Mismatch images/labels"
- Cek nama file (harus sama: `img001.jpg` → `img001.txt`)
- Cek apakah ada gambar yang belum dianotasi
- Jalankan `check_dataset.py` untuk detail

---

**🎉 Selamat! Dataset Anda siap untuk training!**

Lanjut ke **PANDUAN_TRAINING.md** untuk mulai training model YOLO custom.
