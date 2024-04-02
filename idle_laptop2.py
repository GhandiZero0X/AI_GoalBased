import psutil
import time
import screen_brightness_control as sbc
import subprocess
from plyer import notification

def is_system_idle(threshold_percent=10, duration=10):
    cpu_percentages = psutil.cpu_percent(interval=1, percpu=True)
    avg_cpu_percent = sum(cpu_percentages) / len(cpu_percentages)
    return avg_cpu_percent < threshold_percent

def set_battery_mode(mode):
    if mode == "PowerSave":
        try:
            subprocess.run(['powercfg', '/setactive', 'SCHEME_MIN'])
            print("Mode baterai diubah ke Battery Saver")
        except Exception as e:
            print(f"Error setting battery mode: {e}")

def sleep_laptop():
    try:
        subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'])
        print("Laptop masuk ke mode tidur")
    except Exception as e:
        print(f"Error putting laptop to sleep: {e}")

def notify_sleep():
    notification.notify(
        title='Idle Warning',
        message='Laptop akan masuk ke mode tidur karena sudah terlalu lama idle.',
        app_icon=None,  # e.g. 'C:\\icon_32x32.ico'
        timeout=10,  # Notifikasi akan ditampilkan selama 10 detik
    )

def main():
    threshold_percent = 5
    duration = 10
    idle_duration_threshold = 60  # 60 detik atau 1 menit
    sleep_duration_threshold = 120  # 120 detik atau 2 menit

    idle_duration_counter = 0
    sleep_duration_counter = 0

    while True:
        if is_system_idle(threshold_percent, duration):
            sbc.set_brightness(30)
            print("Sistem sekarang idle. Kecerahan layar diturunkan 30%")
            idle_duration_counter += duration
            sleep_duration_counter += duration
            if idle_duration_counter >= idle_duration_threshold:
                set_battery_mode("PowerSave")
                print("Sistem idle agak lama. Mode baterai diubah ke hemat daya")
            if sleep_duration_counter >= sleep_duration_threshold:
                sleep_laptop()
                notify_sleep()
                sleep_duration_counter = 0
        else:
            sbc.set_brightness(50)
            print("Sistem tidak sedang idle. Kecerahan layar diatur kembali normal 50%")
            idle_duration_counter = 0
        time.sleep(duration)

if __name__ == "__main__":
    main()
