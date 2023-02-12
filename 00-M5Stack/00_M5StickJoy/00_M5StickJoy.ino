#include <M5StickC.h>
// #include <M5StickCPlus.h>
#include "Hat_JoyC.h"
#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>

// Insert your SSID
constexpr char WIFI_SSID[] = "Livebox-A916";

//uint8_t broadcastAddress[] = {0x0C, 0xB8, 0x15, 0xCD, 0x01, 0xEC};// REPLACE WITH RECEIVER MAC ADDRESS
//uint8_t broadcastAddress[] = {0xF4, 0x12, 0xFA, 0xCB, 0x1A, 0x10};// REPLACE WITH RECEIVER MAC ADDRESS
//uint8_t broadcastAddress[] = {0x24, 0xA1, 0x60, 0x45, 0xBA, 0x18};// REPLACE WITH RECEIVER MAC ADDRESS
//uint8_t broadcastAddress[] = {0x78, 0x21, 0x84, 0x9D, 0x85, 0x6C};// REPLACE WITH RECEIVER MAC ADDRESS
/// THIS ESPNOW 50:02:91:A2:80:10


uint8_t broadcastAddress[] = {0xF0, 0x08, 0xD1, 0xC7, 0x3E, 0xF8};// REPLACE WITH RECEIVER MAC ADDRESS


struct message_format {
  int x0;
  int y0;
  int btn0;
  int x1;
  int y1;
  int btn1;
};

message_format msg;
TFT_eSprite canvas = TFT_eSprite(&M5.Lcd);
JoyC joyc;

// callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  if(status == ESP_NOW_SEND_SUCCESS)
  {
    //Serial.print("a");
  }
  else
  {
    Serial.print("X");
  }
}

int32_t getWiFiChannel(const char *ssid) {
  if (int32_t n = WiFi.scanNetworks()) {
      for (uint8_t i=0; i<n; i++) {
          if (!strcmp(ssid, WiFi.SSID(i).c_str())) {
              return WiFi.channel(i);
          }
      }
  }
  return 0;
}

void setup() {
  M5.begin(); // Initialize host device.
  M5.Lcd.setRotation(1); // Rotation screen. 
  canvas.createSprite(160,80); // Create a 160*80 canvas. 
  canvas.setTextColor(ORANGE); // Set font colour to orange. 
  joyc.begin(); // Initialize JoyC.
  // greetings
  canvas.fillSprite(BLACK);  // Fill the canvas with black
  canvas.setCursor(0, 10);  // Set the cursor at (0,10)
  canvas.println("Mini Pupper v2 PRO R/C"); 
  // Init WIFI  
  WiFi.mode(WIFI_STA); // Set device as a Wi-Fi Station
  /*
  int32_t channel = getWiFiChannel(WIFI_SSID);
  WiFi.printDiag(Serial); // Uncomment to verify channel number before
  esp_wifi_set_promiscuous(true);
  esp_wifi_set_channel(channel, WIFI_SECOND_CHAN_NONE);
  esp_wifi_set_promiscuous(false);
  WiFi.printDiag(Serial); // Uncomment to verify channel change after
  */
  
  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println(F("Error initializing ESP-NOW"));
    canvas.print("Error initializing ESP-NOW"); 
    canvas.pushSprite(10, 0);      
    return;
  }
  Serial.println(F("TX initialized"));
  canvas.println("TX initialized"); 
  Serial.print("Mac: ");
  Serial.println(WiFi.macAddress());    
  canvas.print("Mac: "); 
  canvas.println(WiFi.macAddress());  
  // Define Send function
  esp_now_register_send_cb(OnDataSent);
  // Register peer
  esp_now_peer_info_t peerInfo;
  memset(&peerInfo, 0, sizeof(peerInfo));
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;  
  // Add peer
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println(F("Failed to add peer"));
    canvas.println("Failed to add peer");  
    canvas.pushSprite(10, 0);      
    return;
  }  
  canvas.pushSprite(10, 0);    
}

char info[50];
unsigned int counter = 0;

void loop() {
  // Update JoyC's data
  joyc.update();
  // fill message
  msg.x0 = joyc.x0;
  msg.y0 = joyc.y0;
  msg.btn0 = joyc.btn0;  
  msg.x1 = joyc.x1;
  msg.y1 = joyc.y1;
  msg.btn1 = joyc.btn1;
  // Send message via ESP-NOW
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *)&msg, sizeof(msg));
  if (result == ESP_OK) {
    //Serial.print(F("e"));
  }
  else {
    Serial.print(F("x"));
  }
  delay(20);




    /*
    if(counter++%100==0)
    {
      
      canvas.fillSprite(BLACK);  // Fill the canvas with black 填充画布为黑色
      canvas.setCursor(0, 10);  // Set the cursor at (0,10) 设置光标在(0,10)
      canvas.println("JoyC TEST");
  
  
  
      sprintf(info, "X0: %d Y0: %d", joyc.x0, joyc.y0);
      canvas.println(info);
      Serial.println(info);
      sprintf(info, "X1: %d Y1: %d", joyc.x1, joyc.y1);
      canvas.println(info);
      Serial.println(info);
      sprintf(info, "Angle0: %d Angle1: %d", joyc.angle0, joyc.angle1);
      canvas.println(info);
      Serial.println(info);
      sprintf(info, "D0: %d D1: %d", joyc.distance0, joyc.distance1);
      canvas.println(info);
      Serial.println(info);
      sprintf(info, "Btn0: %d Btn1: %d", joyc.btn0, joyc.btn1);
      canvas.println(info);
      Serial.println(info);
      canvas.pushSprite(10, 0);
      if (joyc.btn0 &&
          joyc.btn1) {  // If the buttons are all pressed. 如果按键都被按下
          joyc.setLEDColor(0x00ffe8);
      } else if (joyc.btn0) {
          joyc.setLEDColor(0xff0000);
      } else if (joyc.btn1) {
          joyc.setLEDColor(0x0000ff);
      } else {
          joyc.setLEDColor(0x00ff00);
      }
    } */
}
