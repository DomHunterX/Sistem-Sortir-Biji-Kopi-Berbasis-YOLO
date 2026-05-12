"""
SISTEM DETEKSI BIJI KOPI MENGGUNAKAN YOLO
Titik Inspeksi - Mendeteksi kualitas biji kopi secara real-time
"""

import cv2
import serial
import time
import numpy as np
import logging
from ultralytics import YOLO

# Import konfigurasi dari config.py
from config import (
    SERIAL_CONFIG,
    CAMERA_CONFIG,
    YOLO_CONFIG,
    ROI_CONFIG,
    DETECTION_CONFIG,
    CLASSIFICATION_CONFIG,
    DISPLAY_CONFIG,
    LOGGING_CONFIG,
    COLORS
)

# ==================== SETUP LOGGING ====================
if LOGGING_CONFIG['enabled']:
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG['level']),
        format=LOGGING_CONFIG['format'],
        handlers=[
            logging.FileHandler(LOGGING_CONFIG['file']),
            logging.StreamHandler()
        ]
    )
else:
    logging.basicConfig(level=logging.CRITICAL)

logger = logging.getLogger(__name__)

# =====================================================

class KopiSortingSystem:
    def __init__(self):
        """Inisialisasi sistem deteksi dan komunikasi"""
        print("Memulai Sistem Sortir Kopi Otomatis...")
        logger.info("Sistem dimulai")
        
        # Hitung ROI berdasarkan persentase dari config
        self.frame_width = CAMERA_CONFIG['width']
        self.frame_height = CAMERA_CONFIG['height']
        self.roi_x_start = int(self.frame_width * ROI_CONFIG['x_start_percent'])
        self.roi_x_end = int(self.frame_width * ROI_CONFIG['x_end_percent'])
        self.roi_y_start = int(self.frame_height * ROI_CONFIG['y_start_percent'])
        self.roi_y_end = int(self.frame_height * ROI_CONFIG['y_end_percent'])
        
        # Inisialisasi Serial Communication
        try:
            self.esp32 = serial.Serial(
                SERIAL_CONFIG['port'],
                SERIAL_CONFIG['baudrate'],
                timeout=SERIAL_CONFIG['timeout']
            )
            time.sleep(2)  # Tunggu ESP32 siap
            print(f"Koneksi Serial berhasil di {SERIAL_CONFIG['port']}")
            logger.info(f"Serial connected: {SERIAL_CONFIG['port']}")
        except Exception as e:
            print(f"Error koneksi serial: {e}")
            print("Pastikan ESP32 terhubung dan COM port benar!")
            logger.error(f"Serial connection failed: {e}")
            exit(1)
        
        # Inisialisasi YOLO Model
        try:
            self.model = YOLO(YOLO_CONFIG['model_path'])
            print(f"Model YOLO berhasil dimuat: {YOLO_CONFIG['model_path']}")
            print("CATATAN: Saat ini menggunakan model 'person' sebagai placeholder")
            print("Ganti dengan model custom Anda untuk deteksi biji kopi!")
            logger.info(f"YOLO model loaded: {YOLO_CONFIG['model_path']}")
        except Exception as e:
            print(f"Error loading model: {e}")
            logger.error(f"Model loading failed: {e}")
            exit(1)
        
        # Inisialisasi Camera
        self.cap = cv2.VideoCapture(CAMERA_CONFIG['index'])
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        
        if not self.cap.isOpened():
            print("Error: Tidak dapat membuka kamera!")
            logger.error("Camera open failed")
            exit(1)
        
        print(f"Kamera berhasil diinisialisasi (Index: {CAMERA_CONFIG['index']})")
        logger.info(f"Camera initialized: {CAMERA_CONFIG['index']}")
        
        # Variabel tracking
        self.last_detection_time = 0
        self.total_detections = 0
        self.bagus_count = 0
        self.cacat_count = 0
        self.fps = 0
        self.fps_start_time = time.time()
    
    def is_in_roi(self, x1, y1, x2, y2):
        """Cek apakah bounding box berada di ROI (tengah frame)"""
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        # Cek area bounding box
        area = (x2 - x1) * (y2 - y1)
        if area < DETECTION_CONFIG['min_area'] or area > DETECTION_CONFIG['max_area']:
            return False
        
        return (self.roi_x_start <= center_x <= self.roi_x_end and 
                self.roi_y_start <= center_y <= self.roi_y_end)
    
    def classify_quality(self, detection):
        """
        Klasifikasi kualitas biji kopi
        Mode: placeholder atau custom (sesuai config.py)
        """
        confidence = float(detection.conf.item())   # Fix: konversi ke float
        class_id = int(detection.cls.item())         # Fix: konversi ke int
        class_name = self.model.names[class_id].lower()

        if CLASSIFICATION_CONFIG['mode'] == 'custom':
            if class_name in CLASSIFICATION_CONFIG['classes']['bagus']:
                return "BAGUS"
            elif class_name in CLASSIFICATION_CONFIG['classes']['cacat']:
                return "CACAT"
            else:
                logger.warning(f"Unknown class: {class_name}")
                return "CACAT"
        else:
            import random
            if random.random() < 0.7:
                logger.info(f"Placeholder mode: Simulated as BAGUS (confidence: {confidence:.2f})")
                return "BAGUS"
            else:
                logger.info(f"Placeholder mode: Simulated as CACAT (confidence: {confidence:.2f})")
                return "CACAT"
    
    def send_flag_to_esp32(self, grade):
        """Kirim flag ke ESP32 via Serial"""
        try:
            if grade == "CACAT":
                self.esp32.write(b'C')
                self.cacat_count += 1
                print(f"Kirim flag: CACAT (Total Cacat: {self.cacat_count})")
                logger.info(f"Flag sent: CACAT (Total: {self.cacat_count})")
            elif grade == "BAGUS":
                self.esp32.write(b'B')
                self.bagus_count += 1
                print(f"Kirim flag: BAGUS (Total Bagus: {self.bagus_count})")
                logger.info(f"Flag sent: BAGUS (Total: {self.bagus_count})")
            
            self.total_detections += 1
        except Exception as e:
            print(f"Error mengirim data: {e}")
            logger.error(f"Serial send failed: {e}")
    
    def draw_roi(self, frame):
        """Gambar ROI di frame untuk visualisasi"""
        if DISPLAY_CONFIG['show_roi']:
            cv2.rectangle(frame, 
                         (self.roi_x_start, self.roi_y_start), 
                         (self.roi_x_end, self.roi_y_end), 
                         COLORS['roi'], 2)
            cv2.putText(frame, "ROI - Area Deteksi", 
                       (self.roi_x_start, self.roi_y_start - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS['roi'], 2)
    
    def draw_info(self, frame):
        """Tampilkan informasi statistik di frame"""
        if not DISPLAY_CONFIG['show_stats']:
            return
        
        info_y = 30
        cv2.putText(frame, f"Total: {self.total_detections}", 
                   (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLORS['text'], 2)
        cv2.putText(frame, f"Bagus: {self.bagus_count}", 
                   (10, info_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLORS['bagus'], 2)
        cv2.putText(frame, f"Cacat: {self.cacat_count}", 
                   (10, info_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLORS['cacat'], 2)
        
        # Tampilkan FPS jika diaktifkan
        if DISPLAY_CONFIG['show_fps']:
            cv2.putText(frame, f"FPS: {self.fps:.1f}", 
                       (10, info_y + 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLORS['text'], 2)
    
    def run(self):
        """Main loop - Deteksi real-time"""
        print("\n🎥 Sistem berjalan! Tekan 'q' untuk keluar\n")
        logger.info("Detection loop started")
        
        frame_count = 0
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error membaca frame dari kamera")
                logger.error("Frame read failed")
                break
            
            # Hitung FPS
            frame_count += 1
            if frame_count % 30 == 0:  # Update FPS setiap 30 frame
                elapsed = time.time() - self.fps_start_time
                self.fps = 30 / elapsed if elapsed > 0 else 0
                self.fps_start_time = time.time()
            
            # Jalankan YOLO inference
            results = self.model(
                frame,
                conf=YOLO_CONFIG['confidence'],
                device=YOLO_CONFIG['device'],
                verbose=YOLO_CONFIG['verbose']
            )
            
            # Gambar ROI
            self.draw_roi(frame)
            
            # Process detections
            current_time = time.time()
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Ambil koordinat bounding box
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = self.model.names[class_id]
                    
                    # Cek apakah deteksi di dalam ROI
                    if self.is_in_roi(x1, y1, x2, y2):
                        # Cooldown check - hindari spam deteksi
                        cooldown = DETECTION_CONFIG['cooldown']
                        if current_time - self.last_detection_time >= cooldown:
                            # Klasifikasi kualitas
                            grade = self.classify_quality(box)
                            
                            # Kirim flag ke ESP32
                            self.send_flag_to_esp32(grade)
                            
                            # Update timestamp
                            self.last_detection_time = current_time
                            
                            # Gambar bounding box dengan warna sesuai grade
                            color = COLORS['bagus'] if grade == "BAGUS" else COLORS['cacat']
                            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)
                            
                            # Label
                            label = f"{grade} ({class_name}) {confidence:.2f}"
                            cv2.putText(frame, label, (int(x1), int(y1) - 10),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                        else:
                            # Masih dalam cooldown, gambar box abu-abu
                            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), 
                                        COLORS['cooldown'], 2)
                    else:
                        # Deteksi di luar ROI, gambar box tipis
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), 
                                    COLORS['outside_roi'], 1)
            
            # Tampilkan statistik
            self.draw_info(frame)
            
            # Tampilkan frame (jika diaktifkan)
            if DISPLAY_CONFIG['show_window']:
                cv2.imshow(DISPLAY_CONFIG['window_name'], frame)
                
                # Exit dengan tombol 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\nMenghentikan sistem...")
                    logger.info("System stopped by user")
                    break
            else:
                # Jika window tidak ditampilkan, cek keyboard interrupt
                time.sleep(0.01)
        
        # Cleanup
        self.cleanup()
    
    def cleanup(self):
        """Bersihkan resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        self.esp32.close()
        print("Sistem dihentikan dengan aman")
        print(f"\nSTATISTIK AKHIR:")
        print(f"   Total Deteksi: {self.total_detections}")
        print(f"   Biji Bagus: {self.bagus_count}")
        print(f"   Biji Cacat: {self.cacat_count}")
        
        logger.info("System cleanup completed")
        logger.info(f"Final stats - Total: {self.total_detections}, Bagus: {self.bagus_count}, Cacat: {self.cacat_count}")

# ==================== MAIN PROGRAM ====================
if __name__ == "__main__":
    try:
        # Tampilkan konfigurasi yang digunakan
        print("\n" + "="*60)
        print("KONFIGURASI SISTEM (dari config.py)")
        print("="*60)
        print(f"Serial Port      : {SERIAL_CONFIG['port']}")
        print(f"Camera Index     : {CAMERA_CONFIG['index']}")
        print(f"Resolution       : {CAMERA_CONFIG['width']}x{CAMERA_CONFIG['height']}")
        print(f"YOLO Model       : {YOLO_CONFIG['model_path']}")
        print(f"Confidence       : {YOLO_CONFIG['confidence']}")
        print(f"ROI Area         : {ROI_CONFIG['x_start_percent']*100:.0f}%-{ROI_CONFIG['x_end_percent']*100:.0f}% (X), {ROI_CONFIG['y_start_percent']*100:.0f}%-{ROI_CONFIG['y_end_percent']*100:.0f}% (Y)")
        print(f"Detection Cooldown: {DETECTION_CONFIG['cooldown']}s")
        print(f"Classification   : {CLASSIFICATION_CONFIG['mode']}")
        print(f"Logging          : {'Enabled' if LOGGING_CONFIG['enabled'] else 'Disabled'}")
        print("="*60 + "\n")
        
        system = KopiSortingSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n⚠️  Program dihentikan oleh user (Ctrl+C)")
        logger.info("Program interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()