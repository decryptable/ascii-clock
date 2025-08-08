# ASCII Clock

<center>
    <a href="README.md">English Docs</a> | <span>Indonesian Docs</span>
</center>

---

Jam CLI real-time yang menampilkan waktu dengan meng-_highlight_ karakter dari _source-code_\-nya sendiri untuk membentuk digit ASCII art.

![Demo](assets/demo.gif)

## Fitur

- **Self-Rendering**: Menggunakan _source code_ program itu sendiri sebagai kanvas untuk seni ASCII
- **Tampilan Real-Time**: Memperbarui setiap detik tanpa spam terminal
- **Penyesuaian Adaptif**: Otomatis menyesuaikan dengan dimensi terminal
- **Multi-Platform**: Mendukung Windows, macOS, dan Linux
- **Waktu Berkode Warna**: Jam, menit, dan detik dalam warna yang berbeda

## Persyaratan

- Python 3.6+
- Terminal dengan dukungan warna ANSI
- Ukuran terminal minimum: 100x25 karakter

## Instalasi

Clone repositori:

```bash
git clone https://github.com/decryptable/ascii-clock.git
cd ascii-clock
```

## Penggunaan

Jalankan jam:

```bash
python clock.py
```

Tekan <kbd>Ctrl+C</kbd> untuk keluar.

## Cara Kerja

ASCII Clock beroperasi melalui proses multi-tahap yang canggih yang mengubah _source code_ menjadi jam visual:

### 1. Pemrosesan _Source Code_
- **Self-Reading**: Program membaca _source-code_ dari file programnya sendiri (`clock.py`) menggunakan operasi file I/O Python
- **Penghapusan Docstring**: Menggunakan pola regex untuk menghapus semua docstring (single dan multi-line) serta komentar dari _source code_
- **Minifikasi**: Menghapus whitespace berlebihan dan baris kosong untuk membuat aliran karakter kode yang kontinu
- **Perpanjangan Buffer**: Menggandakan kode yang telah diminifikasi beberapa kali untuk memastikan karakter yang cukup untuk grid tampilan

### 2. Pembuatan Grid Dinamis
- **Deteksi Terminal**: Secara otomatis mendeteksi dimensi terminal saat ini menggunakan `os.get_terminal_size()`
- **Pemetaan Grid**: Membuat grid karakter 2D dengan memetakan _source code_ yang telah diminifikasi secara berurutan melintasi baris dan kolom
- **Penyesuaian Adaptif**: Menyesuaikan dimensi grid berdasarkan ukuran terminal, memastikan tampilan optimal di layar apa pun

### 3. Generasi ASCII Art
- **Pencocokan Pola**: Setiap digit (0-9) dan titik dua (:) memiliki pola 11×9 piksel yang telah ditentukan sebelumnya yang disimpan dalam `ASCII_PATTERNS`
- **Parsing Waktu**: Waktu sistem saat ini diformat sebagai "HH:MM:SS" dan setiap karakter dipetakan ke pola yang sesuai
- **Kalkulasi Posisi**: Menghitung koordinat grid yang tepat untuk setiap piksel dari setiap digit, dipusatkan di terminal

### 4. Sistem Highlighting Karakter
- **Pemetaan Piksel**: Untuk setiap piksel aktif dalam pola digit, mengidentifikasi karakter yang sesuai dalam grid _source code_
- **Penugasan Warna**: Menerapkan skema warna yang berbeda:
  - **Merah**: Jam (HH)
  - **Hijau**: Menit (MM)
  - **Cyan**: Detik (SS)
  - **Kuning**: Pemisah (:)
- **Deteksi Border**: Menghasilkan border abu-abu halus di sekitar karakter yang di-highlight dengan mengidentifikasi posisi non-digit yang berdekatan

### 5. Algoritma Spasi
- **Pemisahan Karakter**: Mengimplementasikan spasi horizontal 12-piksel antara digit untuk mencegah tumpang tindih visual
- **Optimasi Border**: Menggunakan operasi set untuk menghilangkan posisi border duplikat dan mencegah konflik dengan piksel digit
- **Logika Pemusatan**: Secara dinamis menghitung posisi optimal untuk memusatkan tampilan waktu dalam ruang terminal yang tersedia

### 6. Loop Rendering Real-Time
- **Manajemen Layar**: Membersihkan terminal dan memposisikan ulang kursor untuk update tanpa flicker
- **Tampilan Berlapis**: Me-render tiga lapisan visual:
  - **Background**: Karakter _source code_ abu-abu gelap
  - **Border**: Karakter abu-abu terang di sekitar digit waktu
  - **Foreground**: Karakter digit waktu berwarna terang
- **Kontrol Timing**: Memperbarui tampilan setiap detik dengan sinkronisasi timing yang tepat

## Dukungan Platform

- **Windows**: Dukungan penuh dengan deteksi ukuran terminal
- **macOS/Linux**: Dukungan penuh termasuk deteksi auto-resize
- **Auto-Resize**: Otomatis mendeteksi perubahan ukuran terminal jika didukung

## Detail Teknis

- **Grid Tampilan**: Pembuatan grid dinamis berdasarkan ukuran terminal
- **Pencocokan Pola**: Pola ASCII 11x9 piksel untuk setiap digit
- **Skema Warna**: Merah (jam), hijau (menit), cyan (detik), kuning (pemisah)
- **Algoritma Border**: Deteksi border cerdas untuk mencegah tumpang tindih karakter
- **Pemrosesan Sumber**: Penghapusan docstring dan komentar berbasis regex untuk seni ASCII yang bersih

## Pemecahan Masalah

**Terminal terlalu kecil**: Ubah ukuran terminal Anda menjadi minimal 100x25 karakter.

**Warna tidak muncul**: Pastikan terminal Anda mendukung kode warna ANSI.

**Auto-resize tidak berfungsi**: Beberapa terminal atau sistem operasi mungkin tidak mendukung deteksi perubahan ukuran otomatis. Refresh manual mungkin diperlukan setelah mengubah ukuran.

---

**Author**: decryptable