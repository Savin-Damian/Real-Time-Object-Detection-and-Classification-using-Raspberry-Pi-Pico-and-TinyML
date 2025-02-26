from machine import I2C, Pin
from i2c_lcd import I2cLcd
import utime
import uos
import network
import urequests

TRIG = Pin(2, Pin.OUT)
ECHO = Pin(3, Pin.IN)
I2C_SDA = Pin(0)
I2C_SCL = Pin(1)
led_verde = Pin(12, Pin.OUT)
led_albastru = Pin(11, Pin.OUT)
led_rosu = Pin(7, Pin.OUT)
buzzer = Pin(9, Pin.OUT) 

i2c = I2C(0, sda=I2C_SDA, scl=I2C_SCL, freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

SSID = "TP-LINK_B626BE"
PASSWORD = "*****************"
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbxyGq_YprUfSxWoJvjJOfrCAM4Jn5weqLPEytuuTX-eCg_CxW9zbbJ7Bx5zq-je35D1GQ/exec"


def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print(f"Conectare la Wi-Fi... {ssid}")
    
    timeout = 20  
    start_time = utime.time()
    
    while not wlan.isconnected():
        if utime.time() - start_time > timeout:
            print("Conexiunea la Wi-Fi a eșuat. Verificați SSID și parola.")
            return False 
        utime.sleep(1)
    print("Wi-Fi conectat!")
    print("Adresa IP:", wlan.ifconfig()[0])
    return wlan


def measure_distance():
    TRIG.low()  
    utime.sleep_us(2)  
    TRIG.high()  
    utime.sleep_us(10)  
    TRIG.low()  

    while ECHO.value() == 0:
        pulse_start = utime.ticks_us()

    while ECHO.value() == 1:
        pulse_end = utime.ticks_us()

    pulse_duration = utime.ticks_diff(pulse_end, pulse_start)
    distance = (pulse_duration * 0.0343) / 2  
    return distance


def tinyml_message(distance):
    if distance < 10:
        return "COLIZIUNE"
    elif distance < 30:
        return "ALERT"
    else:
        return "OK"


def controleaza_leduri(message):
    led_verde.value(0)
    led_albastru.value(0)
    led_rosu.value(0)
    if message == "OK":
        led_verde.value(1)
    elif message == "ALERT":
        led_albastru.value(1)
    elif message == "COLIZIUNE":
        led_rosu.value(1)


def controleaza_buzzer(distance):
    max_sleep = 500  
    min_sleep = 50   

    if distance > 30:
       
        buzzer.value(0)
    elif distance <3:
        buzzer.value(1)
        
    else:
        # Calculeaza intervalul de timp proportional cu distanta
        sleep_time = min_sleep + (max_sleep - min_sleep) * (distance / 25)

        
        buzzer.value(1)
        utime.sleep_ms(int(sleep_time)) 
        buzzer.value(0)
        utime.sleep_ms(int(sleep_time))  

        
        
def format_timestamp(timestamp):
    local_time = utime.gmtime(timestamp)
    formatted_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
        local_time[0], local_time[1], local_time[2], local_time[3], local_time[4], local_time[5])
    return formatted_time


def save_to_csv(filename, header):
    if filename not in uos.listdir():
        with open(filename, "w") as file:
            file.write(header + "\n")

def append_data_to_csv(filename, data):
    with open(filename, "a") as file:
        file.write(",".join(map(str, data)) + "\n")


def send_to_google_sheets(data):
    try:
        response = urequests.post(GOOGLE_SHEET_URL, json=data)
        if response.status_code == 200:
            print("Datele au fost trimise cu succes la Google Sheets!")
        else:
            print("Eroare la trimiterea datelor:", response.status_code)
        response.close()
    except Exception as e:
        print("Eroare conexiune:", str(e))
        
        
csv_filename = "distance.csv"
csv_header = "Data_si_ora, Distanta_cm,  Mesaj"
save_to_csv(csv_filename, csv_header)
connect_to_wifi(SSID, PASSWORD)

try:
    while True:
        start_time = utime.ticks_us()
        
        distance = measure_distance()
        timestamp = utime.time()
        formatted_time = format_timestamp(timestamp)
        message = tinyml_message(distance)

        lcd.clear()
        lcd.putstr(f"Dist: {distance:.2f} cm")
        lcd.move_to_second_line()
        lcd.putstr(message)

        controleaza_leduri(message)
        controleaza_buzzer(distance)
        
        print(f"Data si ora: {formatted_time}, Distanta: {distance:.2f} cm, Mesaj: {message}")

        append_data_to_csv(csv_filename, [formatted_time, distance, message])

        google_sheet_data = {
            "Data_si_ora": formatted_time,
            "Distanta_cm": "{:.2f}".format(distance),
            "Mesaj": message
        }
        send_to_google_sheets(google_sheet_data)
        
        elapsed_time = utime.ticks_diff(utime.ticks_us(), start_time)
        sleep_time = max(0, 100000 - elapsed_time)
        utime.sleep_us(sleep_time)

except KeyboardInterrupt:
    print("Oprire program. Datele au fost salvate.")

