import random
import struct
from testAPI import API
import time

def generate_random_data():
    enum = random.randint(1,4)  # 1 byte
    integer = random.randint(0, 80)  # 4 bytes
    signed_integer = random.randint(24, 28)  # 4 bytes, 음수 포함
    boolean = random.randint(0, 1)  # 1 byte

    # struct를 사용하여 바이트로 변환 후 문자열로 변환
    data = struct.pack('B I i B', enum, integer, signed_integer, boolean)
    return data.hex()

def main():
    interval = 5
    time.sleep(0.5)
    api = API("https://www.kgu-shiphub.com/api/sensor")

    while True:
        received_data = generate_random_data()
        payload = api.transform_data(received_data)
        
        # payload 값을 터미널에 출력
        print(f"Sending payload: {payload}")
        
        api.send_data(payload)

        time.sleep(interval)

if __name__ == "__main__":
    main()