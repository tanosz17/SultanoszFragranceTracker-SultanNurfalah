# sultanosz_perfume_app/main.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from manager import ParfumManager
from parfum import Parfum
from utils import load_image

# --- Konfigurasi Tampilan (Dark Mode) ---
BG_COLOR = "#2c3e50"
FG_COLOR = "white"
FRAME_COLOR = "#34495e"
ENTRY_BG = "#ecf0f1"
ENTRY_FG = "black"
BUTTON_COLOR = "#e67e22" # Warna oranye
BUTTON_HOVER_COLOR = "#d35400"
BUTTON_TEXT_COLOR = "white"
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_NORMAL = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 11, "bold")


class AppGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.manager = ParfumManager()
        self.title("Sultanosz Fragrance Tracker")
        self.geometry("800x650")
        self.configure(bg=BG_COLOR)

        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, KoleksiPage, TambahPage, RekomendasiPage, RiwayatPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, 'refresh'):
            frame.refresh()
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        label = tk.Label(self, text="Selamat datang, Sultanosz!", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR)
        label.pack(pady=40, padx=20)

        menu_frame = tk.Frame(self, bg=BG_COLOR)
        menu_frame.pack(pady=20, padx=100, fill="x")

        buttons = {
            "Lihat Koleksi Parfum": "KoleksiPage",
            "Tambah Parfum Baru": "TambahPage",
            "Rekomendasi Parfum Hari Ini": "RekomendasiPage",
            "Riwayat Pemakaian": "RiwayatPage",
        }

        for text, page in buttons.items():
            btn = tk.Button(menu_frame, text=text, font=FONT_LABEL, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR,
                            command=lambda p=page: controller.show_frame(p), height=2, relief="flat", borderwidth=0)
            btn.pack(pady=10, fill="x", expand=True)

        btn_exit = tk.Button(menu_frame, text="Keluar", font=FONT_LABEL, bg="#c0392b", fg="white",
                             command=self.quit, height=2, relief="flat", borderwidth=0)
        btn_exit.pack(pady=10, fill="x", expand=True)

class KoleksiPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        title_frame = tk.Frame(self, bg=BG_COLOR)
        title_frame.pack(fill="x", pady=10, padx=20)
        tk.Label(title_frame, text="Koleksi Parfum Saya", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
        tk.Button(title_frame, text="Kembali", command=lambda: controller.show_frame("HomePage"), bg=BUTTON_COLOR, fg=FG_COLOR, relief="flat").pack(side="right")
        
        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=20)
        self.scrollbar.pack(side="right", fill="y")
        
    def refresh(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        parfums = self.controller.manager.koleksi
        if not parfums:
            tk.Label(self.scrollable_frame, text="Koleksi masih kosong.", font=FONT_NORMAL, bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)
            return

        for parfum in parfums:
            self.create_parfum_card(self.scrollable_frame, parfum)

    def create_parfum_card(self, parent_frame, parfum):
        card = tk.Frame(parent_frame, bg=FRAME_COLOR, padx=10, pady=10)
        card.pack(fill="x", pady=5)

        img_label = tk.Label(card, bg=FRAME_COLOR)
        img = load_image(parfum.gambar_path, (100, 100))
        img_label.image = img
        img_label.config(image=img)
        img_label.pack(side="left", padx=10)

        info_frame = tk.Frame(card, bg=FRAME_COLOR)
        info_frame.pack(side="left", fill="x", expand=True, padx=10)

        tk.Label(info_frame, text=f"{parfum.nama} by {parfum.brand}", font=FONT_LABEL, bg=FRAME_COLOR, fg=FG_COLOR).pack(anchor="w")
        tk.Label(info_frame, text=f"Tipe: {parfum.tipe_aroma}", font=FONT_NORMAL, bg=FRAME_COLOR, fg=FG_COLOR).pack(anchor="w")
        tk.Label(info_frame, text=f"Kesan: {parfum.mood_kesan}", font=FONT_NORMAL, bg=FRAME_COLOR, fg=FG_COLOR).pack(anchor="w")
        
        delete_btn = tk.Button(card, text="Hapus", bg="#c0392b", fg="white", relief="flat",
                               command=lambda p=parfum.nama: self.delete_parfum(p))
        delete_btn.pack(side="right", padx=10)

    def delete_parfum(self, parfum_nama):
        if messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus {parfum_nama}?"):
            if self.controller.manager.delete_parfum(parfum_nama):
                messagebox.showinfo("Sukses", f"{parfum_nama} berhasil dihapus.")
                self.refresh()
            else:
                messagebox.showerror("Error", f"{parfum_nama} tidak ditemukan.")

class TambahPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.gambar_path = ""
        self.entries = {}
        self.placeholders = {}

        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(expand=True)
        
        tk.Label(main_frame, text="Tambah Parfum Baru", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)
        
        form_frame = tk.Frame(main_frame, bg=FRAME_COLOR, padx=30, pady=30)
        form_frame.pack(padx=20, pady=10)
        
        fields = {
            "Nama Parfum": "Contoh: Mexicola",
            "Brand": "Contoh: Onix",
            "Tipe Aroma": "Contoh: Citrus Aromatic",
            "Cuaca Cocok": "Contoh: Panas, Hangat",
            "Aktivitas Cocok": "Contoh: Santai, Kantor",
            "Mood / Kesan": "Contoh: Segar, Ceria, Elegan"
        }
        
        for i, (field, placeholder) in enumerate(fields.items()):
            tk.Label(form_frame, text=field, font=FONT_LABEL, bg=FRAME_COLOR, fg=FG_COLOR).grid(row=i, column=0, sticky="w", pady=5, padx=10)
            entry = tk.Entry(form_frame, font=FONT_NORMAL, width=40, bg=ENTRY_BG, fg=ENTRY_FG, relief="flat")
            entry.grid(row=i, column=1, pady=5, padx=10)
            self.entries[field] = entry
            self.placeholders[field] = placeholder

        tk.Label(form_frame, text="Gambar Parfum", font=FONT_LABEL, bg=FRAME_COLOR, fg=FG_COLOR).grid(row=len(fields), column=0, sticky="w", pady=5, padx=10)
        self.upload_btn = tk.Button(form_frame, text="Pilih Gambar", command=self.upload_gambar, bg=BUTTON_COLOR, fg=FG_COLOR, relief="flat")
        self.upload_btn.grid(row=len(fields), column=1, sticky="w", padx=10, pady=5)
        self.gambar_label = tk.Label(form_frame, text="Belum ada gambar dipilih", bg=FRAME_COLOR, fg=FG_COLOR, font=FONT_NORMAL)
        self.gambar_label.grid(row=len(fields)+1, column=1, sticky="w", padx=10)

        action_frame = tk.Frame(main_frame, bg=BG_COLOR)
        action_frame.pack(pady=20)
        tk.Button(action_frame, text="Simpan", bg="#27ae60", fg=FG_COLOR, relief="flat", width=15, height=2, command=self.simpan_parfum).pack(side="left", padx=10)
        tk.Button(action_frame, text="Kembali", bg="#7f8c8d", fg=FG_COLOR, relief="flat", width=15, height=2, command=lambda: controller.show_frame("HomePage")).pack(side="left", padx=10)
            
    def upload_gambar(self):
        filepath = filedialog.askopenfilename(title="Pilih Gambar Parfum", filetypes=(("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")))
        if filepath:
            filename = os.path.basename(filepath)
            dest_folder = "assets/parfum"
            os.makedirs(dest_folder, exist_ok=True)
            self.gambar_path = os.path.join(dest_folder, filename)
            shutil.copy(filepath, self.gambar_path)
            self.gambar_label.config(text=filename)
            
    def simpan_parfum(self):
        # <<< PERBAIKAN UTAMA DI SINI >>>
        # Kunci dictionary disesuaikan dengan parameter di __init__ class Parfum
        data = {
            "nama": self.entries["Nama Parfum"].get(),
            "brand": self.entries["Brand"].get(),
            "tipe_aroma": self.entries["Tipe Aroma"].get(),
            "cuaca_cocok": self.entries["Cuaca Cocok"].get(),
            "aktivitas_cocok": self.entries["Aktivitas Cocok"].get(),
            "mood_kesan": self.entries["Mood / Kesan"].get()
        }

        # Validasi yang lebih baik
        for field, value in data.items():
            if not value or value.strip() == "":
                messagebox.showerror("Error", f"Field '{field}' harus diisi!")
                return
        
        if not self.gambar_path:
            messagebox.showerror("Error", "Gambar parfum harus dipilih!")
            return

        data["gambar_path"] = self.gambar_path

        parfum_baru = Parfum(**data)
        self.controller.manager.add_parfum(parfum_baru)
        messagebox.showinfo("Sukses", "Parfum baru berhasil ditambahkan ke koleksi!")
        self.controller.show_frame("KoleksiPage")

class RekomendasiPage(tk.Frame):
    # (Kode untuk halaman ini tidak diubah, namun disesuaikan warnanya)
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.rekomendasi_parfum = None
        
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(expand=True)

        tk.Label(main_frame, text="Rekomendasi Parfum Hari Ini", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)

        kriteria_frame = tk.Frame(main_frame, bg=FRAME_COLOR, padx=20, pady=20)
        kriteria_frame.pack(pady=10)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=ENTRY_BG, background=BUTTON_COLOR, foreground=ENTRY_FG)

        tk.Label(kriteria_frame, text="Mood Kamu:", font=FONT_LABEL, bg=FRAME_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.mood_var = tk.StringVar()
        mood_options = ["Segar", "Ceria", "Elegan", "Misterius", "Tenang", "Profesional"]
        ttk.Combobox(kriteria_frame, textvariable=self.mood_var, values=mood_options, state="readonly", width=30, font=FONT_NORMAL).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(kriteria_frame, text="Cuaca Hari Ini:", font=FONT_LABEL, bg=FRAME_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.cuaca_var = tk.StringVar()
        cuaca_options = ["Panas", "Hangat", "Sejuk", "Hujan"]
        ttk.Combobox(kriteria_frame, textvariable=self.cuaca_var, values=cuaca_options, state="readonly", width=30, font=FONT_NORMAL).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(kriteria_frame, text="Aktivitas Utama:", font=FONT_LABEL, bg=FRAME_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.aktivitas_var = tk.StringVar()
        aktivitas_options = ["Kantor", "Santai", "Olahraga", "Acara Formal", "Kencan"]
        ttk.Combobox(kriteria_frame, textvariable=self.aktivitas_var, values=aktivitas_options, state="readonly", width=30, font=FONT_NORMAL).grid(row=2, column=1, padx=5, pady=5)

        tk.Button(kriteria_frame, text="Cari Rekomendasi", bg=BUTTON_COLOR, fg=FG_COLOR, font=FONT_LABEL, relief="flat", command=self.cari).grid(row=3, columnspan=2, pady=20)
        
        self.hasil_frame = tk.Frame(main_frame, bg=FRAME_COLOR)
        
        tk.Button(main_frame, text="Kembali", bg="#7f8c8d", fg=FG_COLOR, relief="flat", width=15, command=lambda: controller.show_frame("HomePage")).pack(pady=20)

    def cari(self):
        mood = self.mood_var.get()
        cuaca = self.cuaca_var.get()
        aktivitas = self.aktivitas_var.get()

        if not all([mood, cuaca, aktivitas]):
            messagebox.showwarning("Peringatan", "Silakan pilih semua kriteria.")
            return

        self.rekomendasi_parfum = self.controller.manager.get_rekomendasi(mood, cuaca, aktivitas)
        self.tampilkan_hasil()

    def tampilkan_hasil(self):
        for widget in self.hasil_frame.winfo_children():
            widget.destroy()
        
        self.hasil_frame.pack(pady=10, padx=10, fill="x")

        if self.rekomendasi_parfum:
            p = self.rekomendasi_parfum
            tk.Label(self.hasil_frame, text="Rekomendasi terbaik untukmu:", font=("Segoe UI", 12, "italic"), bg=FRAME_COLOR, fg=FG_COLOR).pack(pady=5)
            
            parfum_area = tk.Frame(self.hasil_frame, bg=FRAME_COLOR)
            parfum_area.pack(pady=10)

            img_label = tk.Label(parfum_area, bg=FRAME_COLOR)
            img = load_image(p.gambar_path, (120, 120))
            img_label.image = img; img_label.config(image=img)
            img_label.pack(side="left", padx=10)
            
            info_frame = tk.Frame(parfum_area, bg=FRAME_COLOR)
            info_frame.pack(side="left")
            tk.Label(info_frame, text=f"{p.nama} by {p.brand}", font=FONT_LABEL, bg=FRAME_COLOR, fg=FG_COLOR).pack(anchor="w")
            tk.Label(info_frame, text=f"Kesan: {p.mood_kesan}", font=FONT_NORMAL, bg=FRAME_COLOR, fg=FG_COLOR).pack(anchor="w")
            
            tk.Button(info_frame, text="Catat Pemakaian", bg="#27ae60", fg=FG_COLOR, relief="flat", command=self.catat_pemakaian).pack(anchor="w", pady=10)
            
            tips_frame = tk.Frame(self.hasil_frame, bg=FRAME_COLOR)
            tips_frame.pack(pady=10, fill="x")
            
            tk.Label(tips_frame, text="Tips Pemakaian", font=FONT_LABEL, bg=FRAME_COLOR, fg=FG_COLOR).pack()
            
            nadi_img_label = tk.Label(tips_frame, bg=FRAME_COLOR)
            nadi_img = load_image("assets/titik_nadi.png", (150, 150))
            nadi_img_label.image = nadi_img; nadi_img_label.config(image=nadi_img)
            nadi_img_label.pack(pady=5)
            
            tips_text = "Semprotkan pada titik nadi (pergelangan tangan, leher, belakang telinga).\nJarak ideal 15-20 cm. Jangan digosok!"
            tk.Label(tips_frame, text=tips_text, font=FONT_NORMAL, wraplength=400, justify="center", bg=FRAME_COLOR, fg=FG_COLOR).pack()
        else:
            tk.Label(self.hasil_frame, text="Maaf, tidak ada parfum yang cocok dengan kriteria Anda.", font=FONT_NORMAL, bg=FRAME_COLOR, fg=FG_COLOR).pack(pady=20)

    def catat_pemakaian(self):
        if self.rekomendasi_parfum:
            self.controller.manager.catat_pemakaian(self.rekomendasi_parfum.nama)
            messagebox.showinfo("Sukses", f"Pemakaian {self.rekomendasi_parfum.nama} telah dicatat.")
            self.controller.show_frame("RiwayatPage")
        
class RiwayatPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        title_frame = tk.Frame(self, bg=BG_COLOR)
        title_frame.pack(fill="x", pady=10, padx=20)
        tk.Label(title_frame, text="Riwayat Pemakaian", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
        tk.Button(title_frame, text="Kembali", command=lambda: controller.show_frame("HomePage"), bg=BUTTON_COLOR, fg=FG_COLOR, relief="flat").pack(side="right")
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=ENTRY_BG, foreground=ENTRY_FG, fieldbackground=ENTRY_BG, rowheight=25, font=FONT_NORMAL)
        style.map('Treeview', background=[('selected', BUTTON_COLOR)])
        style.configure("Treeview.Heading", font=FONT_LABEL, background="#566573", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', BUTTON_HOVER_COLOR)])

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Tanggal", "Parfum")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.tree.heading("Tanggal", text="Tanggal & Waktu")
        self.tree.heading("Parfum", text="Parfum yang Digunakan")
        self.tree.column("Tanggal", width=250)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for item in self.controller.manager.riwayat:
            self.tree.insert("", "end", values=(item['tanggal'], item['parfum']))

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    os.makedirs("assets/parfum", exist_ok=True)
    
    app = AppGUI()
    app.mainloop()