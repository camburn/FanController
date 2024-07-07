#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <RCSwitch.h>
#include <ArduinoJson.h>
#include <map>

#define BUTTON_PIN 14
#define RADIO_TX_PIN 13

RCSwitch mySwitch = RCSwitch();

int last_button_status = HIGH;

const char *ssid = "beaches";
const char *password = "472023Beach";

String device_uuid = "59d84578-e7fb-4c94-ac7f-3769b12a12e1";

String registration_server = "http://192.168.50.208:8000";
String registration_url = "/devices";
String commands_url = "/devices/59d84578-e7fb-4c94-ac7f-3769b12a12e1/commands";
String complete_url = "/devices/59d84578-e7fb-4c94-ac7f-3769b12a12e1/commands/";
uint16_t registration_port = 8000;

String capabilities = "{ \"name\": \"59d84578-e7fb-4c94-ac7f-3769b12a12e1\", \"capabilities\": [{ \"command\": \"off\", \"description\": \"Turn fan off\" }, { \"command\": \"fan_1\", \"description\": \"Turn fan on power level 1\" }, { \"command\": \"fan_2\", \"description\": \"Turn fan on power level 2\" }, { \"command\": \"fan_3\", \"description\": \"Turn fan on power level 3\" }, { \"command\": \"fan_4\", \"description\": \"Turn fan on power level 4\" }, { \"command\": \"fan_5\", \"description\": \"Turn fan on power level 5\" }, { \"command\": \"fan_6\", \"description\": \"Turn fan on power level 6\" }]}";



std::map<String, int> command_map {
    {"off", 11526121},
    {"light_on", 1},
    {"fan_1", 11525885},
    {"fan_2", 11526013},
    {"fan_3", 11525757},
    {"fan_4", 11526077},
    {"fan_5", 11525821},
    {"fan_6", 11525949},
    {"low", 11526027},
    {"high", 11525963},
    {"timer_setting_1", 9912037},
    {"timer_setting_2", 9911909},
    {"timer_setting_3", 9912101},
};

enum HttpMethod {
    GET = 0,
    POST = 1,
    DELETE = 2
};

HTTPClient http;


bool wifi_connect()
{
  if (WiFi.status() == WL_CONNECTED)
  {
    return true;
  }
  Serial.print("Starting Wifi with SSID: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  int wait_timeout = 20;
  Serial.print("Connecting...");
  while (WiFi.status() != WL_CONNECTED)
  {
    wait_timeout -= 1;
    Serial.print(WiFi.status());

    if (wait_timeout == 0)
    {
      Serial.println("Wifi connecting timed out");
      return false;
    }
    delay(1000);
  }
  Serial.print("\nConnected - ");
  Serial.println(WiFi.localIP());
  return true;
}

JsonDocument http_client(String payload, String url, HttpMethod method) {
  WiFiClient client;
  JsonDocument doc;
  
  if (method == GET) {
    Serial.print("GET: ");
  }
  else if (method == POST) {
    Serial.print("POST: ");
  }
  else if (method == DELETE) {
    Serial.print("DELETE: ");
  }
  Serial.print(registration_server + url);
  if (http.begin(client, registration_server + url))
  {

    http.addHeader("Content-Type", "application/json");
    int httpResponseCode;
    if (method == GET) {
      httpResponseCode = http.GET();
    }
    else if (method == POST) {
      httpResponseCode = http.POST(payload);
    }
    else if (method == DELETE) {
      httpResponseCode = http.DELETE();
    }

    Serial.print(" HTTP Response code: ");
    Serial.println(httpResponseCode);
    String payload = http.getString();

    DeserializationError error = deserializeJson(doc, payload);
    if (error)
    {
      Serial.println(error.f_str());
    }
  }
  return doc;
}

JsonDocument http_client(String url, HttpMethod method) {
  return http_client("", url, method);
}

void setup()
{
  Serial.begin(115200);
  Serial.print("Setup\n");
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(LED_BUILTIN_AUX, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);

  digitalWrite(LED_BUILTIN_AUX, HIGH);
  Serial.println("Enabling Transmitter");
  mySwitch.enableTransmit(RADIO_TX_PIN);
  mySwitch.setProtocol(6);

  while (true)
  {
    if (wifi_connect())
    {
      break;
    }
  }

  while (true)
  {
    Serial.println("Registering device");
    JsonDocument status = http_client(capabilities, registration_url, POST);
    Serial.println(String(status["registration"]));
    if (status["registration"] == "success")
    {
      break;
    }
    Serial.println("Registration failed... trying again in 5s");
    delay(5000);
  }
}

void loop()
{

  // int button_status = digitalRead(BUTTON_PIN);
  // digitalWrite(LED_BUILTIN_AUX, button_status);

  JsonDocument commands = http_client(commands_url, GET);
  String command_name = commands["command"];
  if (command_name != "null")
  {
    Serial.print("Received command: '");
    Serial.print(command_name);
    if (command_map.count(command_name) > 0)
    {
      int command_id = commands["command_id"];
      int command = command_map[command_name];
      Serial.print("' Transmitting: ");
      Serial.print(command);
      Serial.print("\n");
      mySwitch.send(command, 24);

      JsonDocument commands = http_client(complete_url + String(command_id), DELETE);
    }
    else
    {
      Serial.print("' ERROR: Command not found in map\n");
    }
  }
  else
  {
    Serial.print("INFO: No command\n");
  }
  delay(10000);

  /*
  if (button_status != last_button_status)
  {
    // State has changed
    if (button_status == LOW)
    {
      Serial.println("Button has been pressed");
      mySwitch.send("101011111101111101111101");
      // mySwitch.send(11526013, 24);
    }
    if (button_status == HIGH)
    {
      Serial.println("Button has been released");
    }
    last_button_status = button_status;
  }
  */
}