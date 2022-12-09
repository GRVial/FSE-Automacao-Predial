import Adafruit_DHT


DHT_PIN = 18

DHT_SENSOR = Adafruit_DHT.DHT22

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print(f"Temperatura={temperature:0.1f}*C  Umidade={humidity:0.1f}%")
    else:
        print("Falha ao receber os dados do sensor de umidade")
