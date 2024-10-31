import serial
import time
import requests

# 시리얼 포트 설정 (ttyS0 또는 ttyAMA1 사용)
ser = serial.Serial(
    port='/dev/ttyS0',  # 또는 '/dev/ttyAMA1' 사용
    baudrate=57600,  # 모듈과 일치하는 baud rate 사용
    timeout=1
)

# 시리얼 포트 열기
if ser.isOpen():
    print("Serial port opened successfully")
else:
    print("Failed to open serial port")

# AT 명령어 보내기
def send_at_command(command):
    ser.write((command + '\r\n').encode())  # AT 명령어 보내기
    time.sleep(1)  # 대기 시간 (필요에 따라 조절 가능)
    response = ser.read(ser.inWaiting()).decode()  # 응답 읽기
    return response

def read_data():
    time.sleep(0.1)
    response = ser.read().decode()  # 응답 읽기
    return response

# response = send_at_command("AT+PSEND=abcd01123123123123212301")
response = send_at_command("AT+PRECV=65534")
# AT 명령어 테스트
while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode()
        transmitted_data = data.split(':')[-1].replace('\r', '').replace('\n', '')
        print(transmitted_data)
        # 16진수 데이터를 바이트 단위로 나눠 ASCII로 변환
        try:
            # 2자리씩 잘라서 ASCII 문자로 변환
            ascii_string = ''.join([chr(int(transmitted_data[i:i+2], 16)) for i in range(0, len(transmitted_data, 2))])
            print(f"Converted ASCII String: {ascii_string}")
            
            # 특정 조건 확인 (예: 특정 문자열 포함 여부)
            if "특정 문자열" in ascii_string:
                # HTTP API 요청 보내기
                url = "https://www.kgu-shiphub.com/api/redoc/"
                payload = { # JSON 형식으로 데이터 전송
                    "section": 1, # enum: 1 ~ 4
                    "speed": -2147483648, # -2147483648 ~ 2147483647 integer
                    "temperature": -2147483648, # -2147483648 ~ 2147483647 integer
                    "is_fire": True # boolean
                }
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, json=payload, headers=headers)
                print(f"HTTP Response: {response.status_code}, {response.text}")
        except ValueError:
            print("Error in converting transmitted data to ASCII")

# 시리얼 포트 닫기
ser.close()
