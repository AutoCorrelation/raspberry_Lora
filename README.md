Raspberry Guide 
==================
Welcome simple Guide Raspberry with LAN ssh.

Initialization
--------
1) Download the Raspberry Image in Raspberry site.
2) Intall any kind of OS

SSH and WI-FI
---
Make file "wpa_supplicant.conf" and input like..:

``` conf
country=KR
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="Your_WiFi_Name"
    psk="Your_WiFi_Password"
    key_mgmt=WPA-PSK
}
```
And make 'ssh' that doesn't have 확장자

and connect ssh ```pi@<IP adress>``` with your password (defualt:```raspberry```)

Enable interface 
----
Allow Interface
```
sudo raspi-config
```
GO to ```interface Options``` and enable ```SPI, UART``` and so on.

Set up Python3
---
```
sudo apt install python3
```
**If want to 가상환경 install venv python**
```
sudo apt install python3-vnenv
python3 -m venv <name of venvFolder>
cd <name of venvFolder>
```

Activating Venv
```
source <folder name of Venv>/bin/activate

...
deactivate
```



Package Install
---
```
sudo apt-get update
sudo apt-get install python3-spidev python3-rpi.gpio

nano test.py
```
```Ctrl+O``` = save || ```Ctrl+X``` = exit file.


SPI install
---
pass

UART install (with package)
---
They have two kinds of Port

- ttyAMA0: 기본 UART 포트 (주로 Bluetooth 모듈이 없는 모델에서 사용)
- ttyS0: 시리얼 포트 (하드웨어 기반 미니 UART, Raspberry Pi 3 이후에는 Bluetooth와 연관됨)

### ***If Serial Console activated, Deactivate in raspi-config*** (Important)
- "Would you like a login shell to be accessible over serial?"라는 질문에 No를 선택합니다.
- "Would you like the serial port hardware to be enabled?"에는 Yes를 선택해 UART 통신을 활성화합니다.

- And delete ```console=ttyS0,115200``` 
- check ```/boot/config.txt``` 
```
enable_uart=1
```

### ***Check port communication test.***
```
dmesg | grep tty
```
Usually ```ttyS0``` -> Uart


### UART package install
``` bash
pip install pyserial
or
sudo apt-get install pyserial
```

``` python
import serial
import time

# 시리얼 포트 설정 (ttyS0 또는 ttyAMA1 사용)
ser = serial.Serial(
    port='/dev/ttyS0',  # 또는 '/dev/ttyAMA1' 사용
    baudrate=9600,  # 모듈과 일치하는 baud rate 사용
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

# AT 명령어 테스트
response = send_at_command("AT")
print("Response: ", response)

# 시리얼 포트 닫기
ser.close()
```


나머지는 알아서 하세요
코드 참고해서.