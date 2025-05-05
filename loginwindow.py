import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
from app import App

# Overlay cho trạng thái loading
def LoadingOverlay(parent, text="Đang xử lý..."):
    overlay = ctk.CTkToplevel(parent)
    overlay.geometry(f"{parent.winfo_width()}x{parent.winfo_height()}+{parent.winfo_x()}+{parent.winfo_y()}")
    overlay.overrideredirect(True)
    overlay.configure(fg_color="#1a1a1a")
    overlay.attributes("-topmost", True)
    label = ctk.CTkLabel(
        overlay,
        text=text,
        font=ctk.CTkFont("Segoe UI", 20, "bold"),
        text_color="white"
    )
    label.place(relx=0.5, rely=0.5, anchor="center")
    overlay.update()
    return overlay

# Label hiệu ứng marquee
class AnimatedLabel(ctk.CTkLabel):
    def __init__(self, master, text, speed=500, **kwargs):
        super().__init__(master, text=text, **kwargs)
        self.full_text = text
        self.speed = speed
        self.pos = 0
        self.after(self.speed, self._scroll)

    def _scroll(self):
        display = self.full_text[self.pos:] + "   " + self.full_text[:self.pos]
        self.configure(text=display)
        self.pos = (self.pos + 1) % len(self.full_text)
        self.after(self.speed, self._scroll)

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hệ thống quản lý nhân viên")
        self.geometry("1200x700")
        self.minsize(800, 500)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # fade-in setup
        self.withdraw()
        self.attributes("-alpha", 0.0)
        self.after(100, self.start_fade_in)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left panel
        left = ctk.CTkFrame(self, corner_radius=20, border_width=1)
        left.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)

        welcome = AnimatedLabel(
            left,
            text="Hi, Welcome back!",
            font=ctk.CTkFont(family="Comic Sans MS", size=24, weight="bold", slant="italic")
        )
        welcome.pack(pady=20)

        self.entry_user = ctk.CTkEntry(left, placeholder_text="Username", width=250, corner_radius=15)
        self.entry_user.pack(pady=5)

        pass_frame = ctk.CTkFrame(left, fg_color="transparent")
        pass_frame.pack(pady=5)
        self.entry_pass = ctk.CTkEntry(pass_frame, placeholder_text="Password", show="●", width=210, corner_radius=15)
        self.entry_pass.pack(side="left", padx=(0, 5))
        self.show_password = False
        toggle = ctk.CTkButton(pass_frame, text="👁", width=30, command=self.toggle_password)
        toggle.pack(side="left")

        self.btn_login = ctk.CTkButton(left, text="Đăng nhập", command=self.login_with_loading, width=250)
        self.btn_login.pack(pady=20)

        self.error_lbl = ctk.CTkLabel(left, text="", text_color="red")
        self.error_lbl.pack()

        # Background image
        self.img_label = tk.Label(self)
        self.img_label.grid(row=0, column=1, sticky="nsew")
        try:
            self.original_image = Image.open("C:/Users/admin/.vscode/Python/oop/nv.png")
        except:
            self.original_image = Image.new("RGB", (600, 700), "gray")
        self.last_size = None
        self.bind("<Configure>", lambda e: self.after_idle(self.resize_image))

    def start_fade_in(self):
        self.state("zoomed")
        self.deiconify()
        self.attributes("-alpha", 0.0)
        self.after(20, self.fade_in)

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 1.0:
            self.attributes("-alpha", alpha + 0.05)
            self.after(20, self.fade_in)

    def fade_out(self, callback=None):
        alpha = self.attributes("-alpha")
        if alpha > 0:
            self.attributes("-alpha", alpha - 0.05)
            self.after(20, lambda: self.fade_out(callback))
        else:
            if callback: callback()

    def resize_image(self):
        w, h = self.img_label.winfo_width(), self.img_label.winfo_height()
        if (w, h) != self.last_size and w>0 and h>0:
            self.last_size = (w, h)
            img = self.original_image.resize((w, h), Image.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.tk_img)

    def toggle_password(self):
        self.show_password = not self.show_password
        self.entry_pass.configure(show="" if self.show_password else "●")

    def login_with_loading(self):
        overlay = LoadingOverlay(self, text="Đang đăng nhập...")
        threading.Thread(target=self._do_login, args=(overlay,), daemon=True).start()

    def _do_login(self, overlay):
        time.sleep(1)
        overlay.destroy()
        self.after(0, self.dang_nhap)

    def dang_nhap(self):
        u, p = self.entry_user.get(), self.entry_pass.get()
        if (u, p) in [("admin","admin"),("nv","123")]:
            role = 'admin' if u=='admin' else 'nhanvien'
            self.fade_out(lambda: self.open_app(role))
        else:
            self.error_lbl.configure(text="Sai thông tin đăng nhập")

    def open_app(self, role):
        self.destroy()
        App(role=role).mainloop()