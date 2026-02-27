#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h> // Make sure this library is installed in Arduino IDE

// Update these with your Wi-Fi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Update this to match the local IPv4 address of the computer running your Python app
const char* serverName = "http://192.168.1.X:5000/update-sensor";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  Serial.print("Connecting to Wi-Fi");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi network");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if(WiFi.status() == WL_CONNECTED){
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // TODO: Replace these hardcoded floats with your actual sensor reading functions
    // float phValue = analogRead(PH_PIN) * calibration_factor ... etc;
    float phValue = 7.1; 
    int tdsValue = 130;
    float turbidityValue = 4.2;

    // Create JSON Payload
    StaticJsonDocument<200> doc;
    doc["ph"] = phValue;
    doc["tds"] = tdsValue;
    doc["turbidity"] = turbidityValue;
    
    String jsonPayload;
    serializeJson(doc, jsonPayload);

    Serial.println("Sending data: ");
    Serial.println(jsonPayload);

    // Send HTTP POST
    int httpResponseCode = http.POST(jsonPayload);
    
    if(httpResponseCode > 0){
      Serial.print("HTTP Code: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println(response);
    } else {
      Serial.print("Error sending POST request. Error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("Wi-Fi Disconnected");
  }
  
  delay(5000); // Send an update every 5 seconds
}
