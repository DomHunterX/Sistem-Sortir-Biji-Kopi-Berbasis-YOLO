import cv2

cap = cv2.VideoCapture(0)

# Memaksa resolusi HD (sesuaikan dengan spesifikasi maksimal kamera, misal 720p/1080p)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal mengambil frame.")
        break
    cv2.imshow('Stream Webcam Generik', frame)

    # Tekan 'q' untuk menghentikan stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()