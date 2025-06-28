# sultanosz_perfume_app/utils.py

from PIL import Image, ImageTk
import os

PLACEHOLDER_IMAGE = "assets/parfum/placeholder.png"

def load_image(path, size):
    """Memuat gambar dari path, mengubah ukurannya, dan mengembalikannya sebagai objek PhotoImage.
    
    Args:
        path (str): Lokasi file gambar.
        size (tuple): Ukuran baru gambar (width, height).

    Returns:
        ImageTk.PhotoImage: Objek gambar yang bisa digunakan di Tkinter.
    """
    try:
        if not os.path.exists(path):
            # Jika path tidak ada, gunakan placeholder
            path = PLACEHOLDER_IMAGE
            
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        # Jika ada error lain, coba load placeholder
        try:
            img = Image.open(PLACEHOLDER_IMAGE)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e_placeholder:
            print(f"Error loading placeholder image: {e_placeholder}")
            return None