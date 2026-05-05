"""
KONFIGURASI SISTEM SORTIR KOPI
File ini berisi semua parameter yang dapat disesuaikan
"""

# ==================== SERIAL COMMUNICATION ====================
SERIAL_CONFIG = {
    'port': 'COM3',          # Port ESP32 (Windows: COM3, Linux: /dev/ttyUSB0)
    'baudrate': 115200,
    'timeout': 1
}

# ==================== CAMERA SETTINGS ====================
CAMERA_CONFIG = {
    'index': 0,              # 0=default, 1/2=eksternal
    'width': 640,
    'height': 480,
    'fps': 30                # Target FPS (actual may vary)
}

# ==================== YOLO MODEL ====================
YOLO_CONFIG = {
    'model_path': 'yolov8n.pt',  # Model file (yolov8n/s/m/l/x)
    'confidence': 0.5,            # Minimum confidence (0.0-1.0)
    'device': 'cuda',              # 'cpu' or 'cuda' (GPU)
    'verbose': False              # Show inference details
}

# ==================== ROI (REGION OF INTEREST) ====================
# Area deteksi di tengah frame (dalam persentase)
ROI_CONFIG = {
    'x_start_percent': 0.3,  # 30% dari kiri
    'x_end_percent': 0.7,    # 70% dari kiri
    'y_start_percent': 0.3,  # 30% dari atas
    'y_end_percent': 0.7     # 70% dari atas
}

# ==================== DETECTION SETTINGS ====================
DETECTION_CONFIG = {
    'cooldown': 1.0,         # Detik antar pengiriman flag (hindari spam)
    'min_area': 100,         # Minimum area bounding box (pixels²)
    'max_area': 50000        # Maximum area bounding box (pixels²)
}

# ==================== CLASSIFICATION ====================
# Untuk model custom, sesuaikan dengan class names Anda
CLASSIFICATION_CONFIG = {
    'mode': 'placeholder',   # 'placeholder' atau 'custom'
    'classes': {
        'bagus': ['bagus', 'good', 'grade_a'],  # Class names untuk BAGUS
        'cacat': ['cacat', 'defect', 'bad']     # Class names untuk CACAT
    },
    # Placeholder mode: klasifikasi berdasarkan confidence
    'placeholder_threshold': 0.7  # confidence > 0.7 = BAGUS, else CACAT
}

# ==================== DISPLAY SETTINGS ====================
DISPLAY_CONFIG = {
    'show_window': True,     # Tampilkan window preview
    'show_fps': True,        # Tampilkan FPS counter
    'show_roi': True,        # Tampilkan ROI box
    'show_stats': True,      # Tampilkan statistik
    'window_name': 'Sistem Sortir Kopi - YOLO Detection'
}

# ==================== LOGGING ====================
LOGGING_CONFIG = {
    'enabled': True,
    'level': 'INFO',         # DEBUG, INFO, WARNING, ERROR
    'file': 'sortir_kopi.log',
    'format': '%(asctime)s - %(levelname)s - %(message)s'
}

# ==================== COLORS (BGR format for OpenCV) ====================
COLORS = {
    'roi': (0, 255, 255),        # Kuning
    'bagus': (0, 255, 0),        # Hijau
    'cacat': (0, 0, 255),        # Merah
    'cooldown': (128, 128, 128), # Abu-abu
    'outside_roi': (200, 200, 200), # Abu-abu terang
    'text': (255, 255, 255)      # Putih
}
