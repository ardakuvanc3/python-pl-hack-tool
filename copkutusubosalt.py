import os
import send2trash
import stat

def izinleri_degistir(dosya_yolu):
    try:
        os.chmod(dosya_yolu, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        print(f"{dosya_yolu} dosyasının izinleri değiştirildi.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

def bosalt_geri_donusum_kutusu(dizin_yolu):
    try:
        for dosya_adı in os.listdir(dizin_yolu):
            dosya_yolu = os.path.join(dizin_yolu, dosya_adı)
            send2trash.send2trash(dosya_yolu)
            print(f"{dosya_yolu} Geri Dönüşüm Kutusu'na taşındı.")
        print("Geri Dönüşüm Kutusu boşaltma işlemi tamamlandı.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Geri Dönüşüm Kutusu'nu boşaltmak için dizin yolunu belirtin
dizin_yolu = "C:\$Recycle.Bin"  # Gerçek dizin yolunu buraya ekleyin
izinleri_degistir(dizin_yolu)
bosalt_geri_donusum_kutusu(dizin_yolu)

