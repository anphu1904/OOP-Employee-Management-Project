import customtkinter as ctk
import tkinter as tk
from tkcalendar import DateEntry
from danh_sach_nhan_vien import DanhSachNhanVien
from nhan_vien import NhanVien
from PIL import Image, ImageTk
import threading
import time

# Overlay cho trạng thái loading
def LoadingOverlay(parent, text="Đang xử lý..."):
    overlay = ctk.CTkToplevel(parent)
    overlay.geometry(f"{parent.winfo_width()}x{parent.winfo_height()}+{parent.winfo_x()}+{parent.winfo_y()}")
    overlay.overrideredirect(True)
    overlay.configure(fg_color="#1a1a1a")  # nền tối hơn, rõ ràng hơn
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

# DateEntry custom
class DateEntryCustom(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master)
        self.cal = DateEntry(self, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', **kwargs)
        self.cal.pack(fill="both", expand=True)

    def get(self):
        return self.cal.get()

# Cửa sổ đăng nhập
class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hệ thống quản lý nhân viên")
        self.geometry("1200x700")
        self.minsize(800, 500)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

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

        self.img_label = tk.Label(self)
        self.img_label.grid(row=0, column=1, sticky="nsew")
        try:
            self.original_image = Image.open("C:/Users/admin/.vscode/Python/oop/nv.png")
        except:
            self.original_image = Image.new("RGB", (600, 700), "gray")

        self.last_size = None
        self.bind("<Configure>", lambda e: self.after_idle(self.resize_image))

    def resize_image(self):
        w, h = self.img_label.winfo_width(), self.img_label.winfo_height()
        if self.last_size == (w, h):
            return
        self.last_size = (w, h)
        if w > 0 and h > 0:
            img = self.original_image.resize((w, h), Image.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.tk_img)

    def start_fade_in(self):
        self.state("zoomed")
        self.deiconify()
        self.attributes("-alpha", 0.0)
        self.after(50, self.fade_in)

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 1.0:
            self.attributes("-alpha", min(alpha + 0.05, 1.0))
            self.after(20, self.fade_in)

    def fade_out(self, callback=None):
        alpha = self.attributes("-alpha")
        if alpha > 0:
            self.attributes("-alpha", max(alpha - 0.05, 0))
            self.after(20, lambda: self.fade_out(callback))
        else:
            if callback:
                callback()

    def toggle_password(self):
        if self.show_password:
            self.entry_pass.configure(show="●")
        else:
            self.entry_pass.configure(show="")
        self.show_password = not self.show_password

    def login_with_loading(self):
        overlay = LoadingOverlay(self, text="Đang đăng nhập...")
        threading.Thread(target=self._do_login, args=(overlay,)).start()

    def _do_login(self, overlay):
        time.sleep(1)
        overlay.destroy()
        self.after(0, self.dang_nhap)

    def dang_nhap(self):
        u, p = self.entry_user.get(), self.entry_pass.get()
        if u == "admin" and p == "admin":
            self.fade_out(lambda: self.open_app('admin'))
        elif u == "nv" and p == "123":
            self.fade_out(lambda: self.open_app('nhanvien'))
        else:
            self.error_lbl.configure(text="Sai thông tin đăng nhập")

    def open_app(self, role):
        self.destroy()
        App(role=role).mainloop()

# App chính
class App(ctk.CTk):
    def __init__(self, role="admin"):
        super().__init__()
        self.title("Quản lý nhân viên")
        self.geometry("1000x750")
        ctk.set_appearance_mode("light")
        self.withdraw()
        self.attributes("-alpha", 0.0)
        self.after(100, self.start_fade_in)

        self.role = role
        self.danh_sach_nv = DanhSachNhanVien()
        try:
            self.danh_sach_nv.doc_file_json("nhanvien.json")
        except:
            pass

        self.frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#f5f5f5", border_width=1)
        self.frame.pack(padx=30, pady=20, fill="x")

        self.entries = {}
        if self.role == "admin":
            labels = [
                ("Mã NV", "text"), ("Họ tên", "text"), ("Ngày sinh", "date"),
                ("Giới tính", "combobox"), ("Quê quán", "text"), ("Email", "text"),
                ("SĐT", "text"), ("Phòng ban", "text"), ("Năm vào làm", "date")
            ]
            for label_text, field_type in labels:
                row = ctk.CTkFrame(self.frame, fg_color="transparent")
                row.pack(fill="x", padx=100, pady=4)
                lbl = ctk.CTkLabel(row, text=label_text, width=120, anchor="w")
                lbl.pack(side="left")
                if field_type == "text":
                    entry = ctk.CTkEntry(row, height=35, corner_radius=10)
                elif field_type == "combobox":
                    entry = ctk.CTkComboBox(row, values=["Nam", "Nữ"], height=35, corner_radius=10)
                elif field_type == "date":
                    entry = DateEntryCustom(row)
                entry.pack(side="left", fill="x", expand=True)
                self.entries[label_text] = entry

        self.frame2 = ctk.CTkFrame(self, fg_color="transparent")
        self.frame2.pack(pady=10)

        self.entry_search = ctk.CTkEntry(self.frame2, placeholder_text="Tìm theo mã hoặc tên", width=200)
        self.entry_search.grid(row=0, column=0, padx=8)

        self.btn_search = ctk.CTkButton(self.frame2, text="🔍 Tìm", command=self.tim_nv, fg_color="#87CEEB", hover_color="#00BFFF")
        self.btn_search.grid(row=0, column=1, padx=8)

        if self.role == "admin":
            self.btn_add = ctk.CTkButton(self.frame2, text="➕ Thêm", command=self.them_nv, fg_color="#4CAF50")
            self.btn_add.grid(row=0, column=2, padx=8)
            self.btn_delete = ctk.CTkButton(self.frame2, text="🗑️ Xoá", command=self.xoa_nv, fg_color="#f44336")
            self.btn_delete.grid(row=0, column=3, padx=8)

        self.btn_csv = ctk.CTkButton(self.frame2, text="📄 Xuất CSV", command=self.xuat_csv, fg_color="#FFC107", text_color="black")
        self.btn_csv.grid(row=0, column=4, padx=8)

        self.btn_load = ctk.CTkButton(self.frame2, text="📂 Đọc JSON", command=self.doc_file)
        self.btn_load.grid(row=1, column=0, padx=8, pady=6)

        if self.role == "admin":
            self.btn_save = ctk.CTkButton(self.frame2, text="💾 Lưu JSON", command=lambda: self.danh_sach_nv.luu_file_json("nhanvien.json"))
            self.btn_save.grid(row=1, column=1, padx=8, pady=6)

        self.btn_logout = ctk.CTkButton(self.frame2, text="🚪 Đăng xuất", command=self.dang_xuat, fg_color="#9e9e9e")
        self.btn_logout.grid(row=1, column=2, padx=8, pady=6)

        self.output = ctk.CTkTextbox(self, height=300, font=("Consolas", 14))
        self.output.pack(padx=30, pady=10, fill="both")

        self.hien_thi_danh_sach()

    def start_fade_in(self):
        self.state("zoomed")
        self.deiconify()
        self.attributes("-alpha", 0.0)
        self.after(50, self.fade_in)

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 1.0:
            self.attributes("-alpha", min(alpha + 0.05, 1.0))
            self.after(20, self.fade_in)

    def fade_out(self, callback=None):
        alpha = self.attributes("-alpha")
        if alpha > 0:
            self.attributes("-alpha", max(alpha - 0.05, 0))
            self.after(20, lambda: self.fade_out(callback))
        else:
            if callback:
                callback()

    def dang_xuat(self):
        self.fade_out(lambda: self.open_login())

    def open_login(self):
        self.destroy()
        from main import LoginWindow
        LoginWindow().mainloop()

    def them_nv(self):
        try:
            data = [self.entries[field].get() for field in self.entries]
            nv = NhanVien(data[0], data[7], int(data[8][-4:]), data[1], data[2], data[3], data[4], data[5], data[6])
            self.danh_sach_nv.them(nv)
            self.danh_sach_nv.luu_file_json("nhanvien.json")
            self.output.insert("end", f"Đã thêm: {nv}\n")
        except Exception as e:
            self.output.insert("end", f"Lỗi thêm: {e}\n")

    def doc_file(self):
        try:
            self.danh_sach_nv.doc_file_json("nhanvien.json")
            self.output.delete("1.0", "end")
            for nv in self.danh_sach_nv.ds:
                self.output.insert("end", f"{nv}\n")
        except Exception as e:
            self.output.insert("end", f"Lỗi đọc: {e}\n")

    def tim_nv(self):
        tu_khoa = self.entry_search.get()
        kq = self.danh_sach_nv.tim_kiem(tu_khoa)
        self.output.delete("1.0", "end")
        for nv in kq:
            self.output.insert("end", f"{nv}\n")

    def xoa_nv(self):
        ma = self.entry_search.get()
        self.danh_sach_nv.xoa(ma)
        self.danh_sach_nv.luu_file_json("nhanvien.json")
        self.output.insert("end", f"Đã xoá nhân viên mã: {ma}\n")

    def xuat_csv(self):
        try:
            self.danh_sach_nv.doc_file_json("nhanvien.json")
            self.danh_sach_nv.xuat_file_csv("nhanvien.csv")
            self.output.insert("end", "Xuất CSV thành công.\n")
        except Exception as e:
            self.output.insert("end", f"Lỗi khi xuất CSV: {e}\n")

    def hien_thi_danh_sach(self):
        self.output.delete("1.0", "end")
        for nv in self.danh_sach_nv.ds:
            self.output.insert("end", f"{nv}\n")
    def dang_xuat(self):
        overlay = LoadingOverlay(self, text="Đang đăng xuất...")
        self.after(1600, lambda: self.fade_out(lambda: self.open_login()))

    def open_login(self):
        self.destroy()
        from main import LoginWindow
        LoginWindow().mainloop()

if __name__ == "__main__":
    LoginWindow().mainloop()