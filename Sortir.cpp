// ================= KONFIGURASI BLYNK & WIFI =================
#define BLYNK_TEMPLATE_ID "TMPL68Y7uKsnv"  // Dari Blynk Console
#define BLYNK_TEMPLATE_NAME "Kopi Sorting"
#define BLYNK_AUTH_TOKEN "x8tDHI-XqvG59uUCkCdAcKVPk58arpbS"  // Token dari Blynk

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ESP32Servo.h>
#include <WiFi.h>
#include <BlynkSimpleEsp32.h>


const char* ssid = "Kaum Mendang Mending";        // Nama WiFi Anda
const char* password = "zidan123"; // Password WiFi Anda

// Virtual Pins Blynk (untuk monitoring di dashboard)
#define VPIN_TOTAL    V0  // Total biji kopi
#define VPIN_BAGUS    V1  // Jumlah biji bagus
#define VPIN_CACAT    V2  // Jumlah biji cacat
#define VPIN_STATUS   V3  // Status sistem (text)
#define VPIN_RESET    V4  // Button untuk reset counter
// ============================================================

// ================= PIN MAPPING (Berdasarkan Diagram) =================
// Pin Motor Driver L298N (Konveyor)
const int ENA_PIN = 14; 
const int IN1_PIN = 26;
const int IN2_PIN = 27;

// Pin Sensor & Aktuator
const int IR_PIN = 32;  // GPIO 32 - IR Sensor (Active-HIGH)
const int SERVO_PIN = 18;

// Pin LCD I2C menggunakan default ESP32: SDA = 21, SCL = 22
// =====================================================================
 
// Inisialisasi Objek
LiquidCrystal_I2C lcd(0x27, 16, 2); // Alamat I2C umumnya 0x27 atau 0x3F
Servo servoGate;

// Variabel Sistem
int totalKopi = 0;
int kopiBagus = 0;
int kopiCacat = 0;

bool isDefectFlag = false; // Flag dari YOLO
bool flagReceived = false; // Tracking apakah flag sudah diterima
int irState = LOW;         // Status IR saat ini (Active-HIGH: HIGH = terdeteksi)
int lastIrState = LOW;     // Status IR sebelumnya

// Posisi Servo (Sesuaikan dengan mekanik gate Anda)
const int POSISI_NORMAL = 0;  // Lurus, biji masuk wadah BAGUS
const int POSISI_BUANG = 90;  // Terbuka, biji masuk wadah CACAT

void setup() {
  // Inisialisasi Serial (Untuk komunikasi dengan Python/YOLO)
  Serial.begin(115200);
  Serial.println("\n=== SISTEM SORTIR KOPI OTOMATIS ===");

  // Setup LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Sistem Sortir");
  lcd.setCursor(0, 1);
  lcd.print("Kopi Otomatis");
  delay(1000);

  // Koneksi WiFi
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connecting WiFi");
  Serial.print("Menghubungkan ke WiFi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  int wifiAttempt = 0;
  while (WiFi.status() != WL_CONNECTED && wifiAttempt < 20) {
    delay(500);
    Serial.print(".");
    lcd.setCursor(wifiAttempt % 16, 1);
    lcd.print(".");
    wifiAttempt++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi Connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("WiFi Connected");
    lcd.setCursor(0, 1);
    lcd.print(WiFi.localIP());
    delay(2000);
  } else {
    Serial.println("\nWiFi Connection Failed!");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("WiFi Failed!");
    lcd.setCursor(0, 1);
    lcd.print("Check Config");
    delay(2000);
  }

  // Inisialisasi Blynk
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connecting Blynk");
  Serial.println("Menghubungkan ke Blynk...");
  
  Blynk.config(BLYNK_AUTH_TOKEN);
  Blynk.connect();
  
  if (Blynk.connected()) {
    Serial.println("Blynk Connected!");
    lcd.setCursor(0, 1);
    lcd.print("Blynk OK!");
    delay(1500);
  } else {
    Serial.println("Blynk Connection Failed!");
    lcd.setCursor(0, 1);
    lcd.print("Blynk Failed!");
    delay(1500);
  }

  // Setup Pin Konveyor
  pinMode(ENA_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);

  // Setup Pin Sensor
  pinMode(IR_PIN, INPUT_PULLUP); // Gunakan internal pull-up

  // Setup Servo
  servoGate.attach(SERVO_PIN);
  servoGate.write(POSISI_NORMAL); // Pastikan servo di posisi awal
  Serial.println("Servo initialized at NORMAL position");

  // Tampilan awal LCD
  updateLCD();

  // Menyalakan Konveyor (Berjalan kontinyu)
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(ENA_PIN, 200); // Kecepatan motor (0-255), sesuaikan kebutuhan
  Serial.println("Konveyor started!");

  // Kirim status awal ke Blynk
  sendToBlynk();
  Blynk.virtualWrite(VPIN_STATUS, "Sistem Aktif");
  
  Serial.println("=== SISTEM SIAP BEROPERASI ===\n");
}

void loop() {
  Blynk.run();

  // Terima flag dari YOLO
  while (Serial.available() > 0) {
    char dataMasuk = Serial.read();
    if (dataMasuk == 'C' || dataMasuk == 'c') {
      isDefectFlag = true;
      flagReceived = true;
      Serial.println("Flag: CACAT Terdeteksi!");
      Blynk.virtualWrite(VPIN_STATUS, "Deteksi: CACAT");
    } 
    else if (dataMasuk == 'B' || dataMasuk == 'b') {
      isDefectFlag = false;
      flagReceived = true;
      Serial.println("Flag: BAGUS Terdeteksi!");
      Blynk.virtualWrite(VPIN_STATUS, "Deteksi: BAGUS");
    }
  }

  irState = digitalRead(IR_PIN);

  if (irState == LOW && lastIrState == HIGH) {  // LOW = objek terdeteksi
    totalKopi++;
    Serial.println("\nIR Sensor: Biji kopi terdeteksi di gerbang!");
    
    if (flagReceived && isDefectFlag == true) {
      kopiCacat++;
      Serial.println("Aksi: MEMBUANG biji cacat");
      Blynk.virtualWrite(VPIN_STATUS, "Membuang Cacat");
      
      servoGate.write(POSISI_BUANG); 
      delay(800);
      servoGate.write(POSISI_NORMAL);
    } 
    else {
      kopiBagus++;
      Serial.println("Aksi: MENERIMA biji bagus");
      Blynk.virtualWrite(VPIN_STATUS, "Menerima Bagus");
      delay(400); 
    }
    
    isDefectFlag = false;
    flagReceived = false;
    
    updateLCD();
    sendToBlynk();
    
    Serial.print("Total: "); Serial.print(totalKopi);
    Serial.print(" | Bagus: "); Serial.print(kopiBagus);
    Serial.print(" | Cacat: "); Serial.println(kopiCacat);
  }
  
  lastIrState = irState;
  delay(10);
}

// Fungsi untuk memperbarui tampilan LCD
void updateLCD() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("T:"); lcd.print(totalKopi);
  lcd.print(" B:"); lcd.print(kopiBagus);
  
  lcd.setCursor(0, 1);
  lcd.print("Cacat: "); lcd.print(kopiCacat);
}

// Fungsi untuk mengirim data ke Blynk Dashboard
void sendToBlynk() {
  if (Blynk.connected()) {
    Blynk.virtualWrite(VPIN_TOTAL, totalKopi);
    Blynk.virtualWrite(VPIN_BAGUS, kopiBagus);
    Blynk.virtualWrite(VPIN_CACAT, kopiCacat);
  }
}

// Blynk Virtual Pin Handler - Reset Counter
BLYNK_WRITE(VPIN_RESET) {
  int buttonState = param.asInt();
  if (buttonState == 1) {
    // Reset semua counter
    totalKopi = 0;
    kopiBagus = 0;
    kopiCacat = 0;
    
    // Update display
    updateLCD();
    sendToBlynk();
    
    // Kirim konfirmasi
    Blynk.virtualWrite(VPIN_STATUS, "Counter direset!");
    Serial.println("🔄 Counter direset dari Blynk Dashboard");
    
    delay(1000);
    Blynk.virtualWrite(VPIN_STATUS, "Sistem Aktif");
  }
}