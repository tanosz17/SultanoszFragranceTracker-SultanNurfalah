# sultanosz_perfume_app/parfum.py

class Parfum:
    """Mewakili satu objek parfum dalam koleksi."""
    def __init__(self, nama, brand, tipe_aroma, cuaca_cocok, aktivitas_cocok, mood_kesan, gambar_path):
        self.nama = nama
        self.brand = brand
        self.tipe_aroma = tipe_aroma
        self.cuaca_cocok = cuaca_cocok
        self.aktivitas_cocok = aktivitas_cocok
        self.mood_kesan = mood_kesan
        self.gambar_path = gambar_path

    def to_dict(self):
        """Mengonversi objek Parfum menjadi dictionary untuk disimpan ke JSON."""
        return {
            "nama": self.nama,
            "brand": self.brand,
            "tipe_aroma": self.tipe_aroma,
            "cuaca_cocok": self.cuaca_cocok,
            "aktivitas_cocok": self.aktivitas_cocok,
            "mood_kesan": self.mood_kesan,
            "gambar_path": self.gambar_path,
        }

    def __str__(self):
        return f"{self.nama} by {self.brand}"