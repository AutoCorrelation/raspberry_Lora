import serial
import time
from testAPI import API

ser = serial.Serial(
    port="/dev/ttyS0",
    baudrate=57600,
    timeout=1,
)


def send_at_command(command):
    ser.write(f"{command}\r\n".encode())  # AT 명령어 보내기
    time.sleep(1)


def main():
    interval = 5
    if ser.isOpen():
        print("Serial port opened successfully")
    else:
        print("Failed to open serial port")
    time.sleep(0.5)

    send_at_command("AT+PRECV=65534")  # 수신 모드 설정
    api = API("https://www.kgu-shiphub.com/api/sensor")

    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode()
            received_data = data.split(":")[-1].strip()
        else:
            print("No data received")
            continue
        payload = api.transform_data(received_data)
        api.send_data(payload)

        time.sleep(interval)


if __name__ == "__main__":
    main()
