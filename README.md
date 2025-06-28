 Sultanosz Fragrance Tracker

Sebuah aplikasi desktop berbasis Python & Tkinter untuk membantu para pencinta parfum dalam mengelola koleksi, mendapatkan rekomendasi harian, dan mencatat riwayat pemakaian. Project ini dibuat sebagai tugas akhir untuk mata kuliah Pemrograman Berorientasi Objek.

![Screenshot Aplikasi](httpsiscreeenshot) 
(Ganti `isicreenshot` dengan screenshot aplikasi Anda. Caranya: upload screenshot ke GitHub issue atau imgur, lalu salin link gambarnya ke sini)

 Latar Belakang & Inspirasi

Aplikasi ini terinspirasi dari pengalaman pribadi sebagai seorang yang hobi mengoleksi dan memakai parfum. Seringkali saya bingung memilih parfum mana yang cocok untuk cuaca atau aktivitas tertentu di hari itu. Selain itu, saya ingin memiliki catatan digital dari semua koleksi parfum saya beserta detailnya, serta riwayat pemakaiannya. Aplikasi "Sultanosz Fragrance Tracker" ini dibuat sebagai solusi untuk masalah tersebut, menggabungkan hobi dengan penerapan konsep Object-Oriented Programming (OOP).

 Fitur Utama

-   ✅ Manajemen Koleksi: Menambah, melihat, dan menghapus koleksi parfum dengan mudah.
-   🧠 Rekomendasi Cerdas: Memberikan rekomendasi parfum harian berdasarkan input mood, cuaca, dan aktivitas pengguna.
-   🖼️ Visual & Informatif: Menampilkan gambar parfum dan detail lengkap, termasuk tips cara pemakaian dengan ilustrasi titik nadi.
-   📅 Pencatatan Riwayat: Menyimpan histori pemakaian parfum untuk referensi di masa mendatang.
-   💾 Penyimpanan Persisten: Semua data koleksi dan riwayat disimpan dalam file JSON, sehingga tidak akan hilang saat aplikasi ditutup.
-   🎨 GUI Interaktif: Tampilan antarmuka yang modern, menarik, dan mudah digunakan (Dark Mode).

 Teknologi yang Digunakan

-   Bahasa Pemrograman: Python 3
-   Library GUI: Tkinter
-   Library Gambar: Pillow (PIL)

 Struktur Folder
Use code with caution.
Markdown
sultanosz_perfume_app/
├── main.py  Kode utama untuk GUI & alur aplikasi
├── parfum.py  Definisi Class Parfum (Blueprint/Model)
├── manager.py  Class ParfumManager (Logika & Manajemen Data)
├── utils.py  Fungsi-fungsi bantuan (misal: load gambar)
├── data/
│ ├── koleksi.json  Database koleksi parfum
│ └── riwayat.json  Database riwayat pemakaian
├── assets/
│ ├── titik_nadi.png  Gambar ilustrasi titik nadi
│ └── parfum/  Folder untuk menyimpan gambar-gambar parfum
└── README.md  File ini
Generated code
 Instalasi dan Cara Penggunaan

Berikut adalah langkah-langkah untuk menjalankan aplikasi ini di komputer lokal.

 1. Prasyarat
Pastikan Anda sudah menginstal Python 3 di sistem Anda.

 2. Clone Repository
Buka terminal atau Git Bash, lalu clone repository ini:
bash
git clone https://github.com/[username-anda]/[nama-repository-anda].git
Use code with caution.
3. Masuk ke Direktori Project
Generated bash
cd sultanosz_perfume_app
Use code with caution.
Bash
4. Instal Dependensi
Aplikasi ini membutuhkan library Pillow. Instal dengan perintah berikut:
Generated bash
pip install Pillow
Use code with caution.
Bash
5. Jalankan Aplikasi
Setelah semua dependensi terinstal, jalankan aplikasi dengan perintah:
Generated bash
python main.py
Use code with caution.
Bash
Aplikasi akan langsung terbuka dan siap digunakan.
Penerapan Konsep Pemrograman Berorientasi Objek (OOP)
Project ini dibangun di atas empat pilar utama OOP untuk memastikan kode yang modular, terstruktur, dan mudah dikelola.
1. Class & Object
Konsep: Class adalah cetakan (blueprint) dan Object adalah produk nyata dari cetakan tersebut.
Implementasi:
parfum.py berisi class Parfum, yang menjadi cetakan untuk setiap parfum. Setiap parfum yang ditambahkan ke koleksi adalah sebuah object dari class ini, dengan atributnya sendiri (nama, brand, dll).
manager.py berisi class ParfumManager, yang berfungsi sebagai "otak" aplikasi untuk mengelola semua object parfum.
2. Inheritance (Pewarisan)
Konsep: Sebuah class baru (child) dapat mewarisi sifat dan metode dari class yang sudah ada (parent).
Implementasi:
Di dalam main.py, semua class halaman seperti HomePage, KoleksiPage, dan lainnya, mewarisi sifat dari class tk.Frame milik Tkinter.
Contoh: class KoleksiPage(tk.Frame):
Ini memungkinkan kita untuk membuat "panel" halaman yang sudah memiliki fungsionalitas dasar, lalu kita tinggal menambahkan komponen spesifik kita sendiri di atasnya.
3. Encapsulation (Pembungkusan)
Konsep: Menyembunyikan detail implementasi yang kompleks di dalam sebuah class, dan hanya menyediakan antarmuka (metode) yang sederhana untuk berinteraksi dengannya.
Implementasi:
class ParfumManager adalah contoh sempurna dari enkapsulasi. Bagian GUI (main.py) tidak perlu tahu bagaimana cara data disimpan ke file JSON atau bagaimana logika pencarian rekomendasi bekerja.
GUI hanya perlu memanggil metode sederhana seperti manager.add_parfum(parfum_baru) atau manager.get_rekomendasi(...). Semua kerumitan "disembunyikan" di dalam ParfumManager.
4. Polymorphism (Banyak Bentuk)
Konsep: Objek dari class yang berbeda dapat merespons sebuah pemanggilan metode yang sama dengan cara yang berbeda.
Implementasi:
Metode refresh() adalah contoh utama polymorphism di project ini.
Saat berpindah halaman, fungsi show_frame memanggil frame.refresh().
Jika frame adalah objek KoleksiPage, refresh() akan memuat ulang daftar kartu parfum.
Jika frame adalah objek RiwayatPage, refresh() akan memuat ulang data pada tabel riwayat.
Satu nama metode (refresh()) memiliki banyak bentuk perilaku, tergantung pada objek mana yang memanggilnya.
Dibuat dengan oleh Sultan Nurfalah TI23H.
