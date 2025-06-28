# sultanosz_perfume_app/manager.py

import json
import os
from datetime import datetime
from parfum import Parfum

class ParfumManager:
    """Mengelola koleksi parfum dan riwayat pemakaian."""
    def __init__(self, koleksi_path='data/koleksi.json', riwayat_path='data/riwayat.json'):
        self.koleksi_path = koleksi_path
        self.riwayat_path = riwayat_path
        self.koleksi = self.load_koleksi()
        self.riwayat = self.load_riwayat()

    def load_koleksi(self):
        """Memuat daftar parfum dari file JSON."""
        if not os.path.exists(self.koleksi_path):
            return []
        try:
            with open(self.koleksi_path, 'r') as f:
                data = json.load(f)
                return [Parfum(**p) for p in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_koleksi(self):
        """Menyimpan daftar parfum ke file JSON."""
        with open(self.koleksi_path, 'w') as f:
            json.dump([p.to_dict() for p in self.koleksi], f, indent=2)

    def add_parfum(self, parfum):
        """Menambahkan parfum baru ke koleksi dan menyimpannya."""
        self.koleksi.append(parfum)
        self.save_koleksi()

    def delete_parfum(self, nama_parfum):
        """Menghapus parfum dari koleksi berdasarkan nama."""
        parfum_to_delete = None
        for p in self.koleksi:
            if p.nama == nama_parfum:
                parfum_to_delete = p
                break
        
        if parfum_to_delete:
            self.koleksi.remove(parfum_to_delete)
            # Opsional: Hapus juga file gambarnya
            if os.path.exists(parfum_to_delete.gambar_path) and "placeholder" not in parfum_to_delete.gambar_path:
                try:
                    os.remove(parfum_to_delete.gambar_path)
                except OSError as e:
                    print(f"Error deleting image file {parfum_to_delete.gambar_path}: {e}")
            self.save_koleksi()
            return True
        return False

    def get_rekomendasi(self, mood, cuaca, aktivitas):
        """Memberikan rekomendasi parfum berdasarkan kriteria."""
        if not self.koleksi:
            return None

        scores = []
        for parfum in self.koleksi:
            score = 0
            if mood.lower() in parfum.mood_kesan.lower():
                score += 3 # Mood adalah prioritas
            if cuaca.lower() in parfum.cuaca_cocok.lower():
                score += 2
            if aktivitas.lower() in parfum.aktivitas_cocok.lower():
                score += 1
            scores.append((score, parfum))
        
        # Urutkan berdasarkan skor tertinggi
        scores.sort(key=lambda x: x[0], reverse=True)
        
        # Kembalikan parfum dengan skor tertinggi, asalkan skornya > 0
        if scores and scores[0][0] > 0:
            return scores[0][1]
        
        # Jika tidak ada yang cocok, kembalikan parfum acak sebagai alternatif
        return self.koleksi[0] if self.koleksi else None

    def load_riwayat(self):
        """Memuat riwayat pemakaian dari file JSON."""
        if not os.path.exists(self.riwayat_path):
            return []
        try:
            with open(self.riwayat_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_riwayat(self):
        """Menyimpan riwayat pemakaian ke file JSON."""
        with open(self.riwayat_path, 'w') as f:
            json.dump(self.riwayat, f, indent=2)

    def catat_pemakaian(self, nama_parfum):
        """Mencatat pemakaian parfum pada hari ini."""
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.riwayat.insert(0, {"tanggal": today, "parfum": nama_parfum}) # insert di awal agar terbaru di atas
        self.save_riwayat()