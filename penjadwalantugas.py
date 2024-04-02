from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from plyer import notification

# Fungsi untuk membuat jadwal
def buat_jadwal(tugas):
    jadwal = []
    waktu_mulai = datetime.now()

    # Mengurutkan tugas berdasarkan deadline dan bobot
    tugas_urut = sorted(tugas, key=lambda x: (x['deadline'], -x['bobot']))

    for tugas in tugas_urut:
        durasi = tugas['bobot'] * timedelta(days=1)  # Konversi bobot ke durasi

        # Mencari waktu mulai paling awal yang tersedia
        waktu_mulai = max(waktu_mulai, tugas['deadline'] - durasi)

        jadwal.append({'tugas': tugas['nama'], 'waktu_mulai': waktu_mulai, 'deadline': tugas['deadline'], 'status': 'belum selesai'})
        
        waktu_mulai += durasi

    return jadwal

# Fungsi untuk menggambar jadwal
def gambar_jadwal(jadwal):
    hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    
    # Membuat gambar dengan ukuran yang lebih besar
    plt.figure(figsize=(10, len(jadwal) * 0.5))

    for idx, kegiatan in enumerate(jadwal):
        # Menghitung waktu awal dan waktu selesai dalam hari
        awal_hari = kegiatan['waktu_mulai'].replace(hour=0, minute=0, second=0)
        selesai_hari = kegiatan['deadline'].replace(hour=0, minute=0, second=0) + timedelta(days=1)

        # Mengatur posisi horizontal bar
        bar_awal = max(kegiatan['waktu_mulai'], awal_hari)
        bar_selesai = min(kegiatan['deadline'], selesai_hari)

        # Menggambar bar
        plt.barh(idx, bar_selesai.timestamp() - bar_awal.timestamp(), left=bar_awal.timestamp(), color='blue')
        plt.text(bar_awal.timestamp() + (bar_selesai.timestamp() - bar_awal.timestamp()) / 2, idx, 
                    f"{hari[kegiatan['waktu_mulai'].weekday()]} - {hari[kegiatan['deadline'].weekday()]}\n{kegiatan['waktu_mulai'].strftime('%H:%M')} - {kegiatan['deadline'].strftime('%H:%M')}",
                    ha='center', va='center')

    plt.xlabel('Waktu')
    plt.ylabel('Tugas')
    plt.title('Jadwal Tugas')
    plt.yticks(range(len(jadwal)), [kegiatan['tugas'] for kegiatan in jadwal])
    plt.xticks(rotation=45)
    plt.grid(axis='x')
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9)  # Mengatur margin kiri dan kanan
    plt.show()



# Fungsi untuk menampilkan notifikasi jika deadline tugas dekat
def cek_notifikasi(jadwal):
    sekarang = datetime.now()

    for kegiatan in jadwal:
        if kegiatan['deadline'] - sekarang <= timedelta(days=1) and kegiatan['status'] == 'belum selesai':  # Jika deadline kurang dari 1 hari dan tugas belum selesai
            notification.notify(
                title='Deadline Tugas Dekat!',
                message=f"Tugas '{kegiatan['tugas']}' memiliki deadline dalam waktu dekat!",
                app_icon=None,  # Anda bisa menentukan icon notifikasi di sini
                timeout=10,  # Notifikasi akan ditampilkan selama 10 detik
            )

            jawaban = input("Apakah tugas ini sudah selesai? (ya/tidak): ")
            if jawaban.lower() == 'ya':
                kegiatan['status'] = 'selesai'
            else:
                waktu_notifikasi = kegiatan['deadline'] - timedelta(minutes=30)
                if sekarang >= waktu_notifikasi:
                    notification.notify(
                        title='Tugas Belum Selesai!',
                        message=f"Anda memiliki tugas '{kegiatan['tugas']}' yang belum selesai!",
                        app_icon=None,
                        timeout=10,
                    )

# Fungsi untuk menghapus tugas yang selesai atau melewati batas deadline dari jadwal
def hapus_tugas(jadwal):
    sekarang = datetime.now()
    tugas_hapus = []

    for kegiatan in jadwal:
        if kegiatan['deadline'] <= sekarang or kegiatan['status'] == 'selesai':
            tugas_hapus.append(kegiatan)

    for kegiatan in tugas_hapus:
        jadwal.remove(kegiatan)

# Main program
def main():
    jumlah_tugas = int(input("Masukkan jumlah tugas: "))
    daftar_tugas = []

    for i in range(jumlah_tugas):
        nama_tugas = input(f"Masukkan nama tugas ke-{i+1}: ")
        deadline = datetime.strptime(input("Masukkan deadline (format YYYY-MM-DD HH:MM): "), '%Y-%m-%d %H:%M')
        bobot = int(input("Masukkan bobot tugas (1/2/3): "))
        daftar_tugas.append({'nama': nama_tugas, 'deadline': deadline, 'bobot': bobot})

    jadwal = buat_jadwal(daftar_tugas)

    while jadwal:
        gambar_jadwal(jadwal)
        cek_notifikasi(jadwal)
        hapus_tugas(jadwal)

    print("Semua tugas telah selesai atau melewati batas deadline!")

if __name__ == "__main__":
    main()