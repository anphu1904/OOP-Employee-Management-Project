import customtkinter as ctk
import tkinter as tk
from danh_sach_nhan_vien import DanhSachNhanVien
from nhan_vien import NhanVien
from PIL import Image, ImageTk

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hệ thống quản lý nhân viên")
        self.geometry("1200x700")
        self.minsize(800, 500)
        ctk.set_appearance_mode("light")

        # Làm mờ nền khi mở
        self.attributes("-alpha", 0.0)
        self.fade_in_alpha = 0.0
        self.after(10, self.fade_in)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ===== LEFT LOGIN PANEL =====
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        inner.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.label_title = ctk.CTkLabel(inner, text="Hi, Welcome back !", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.label_frame.pack(pady=10)

        self.text = "Hi, Welcome back !"
        self.colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
        self.color_index = 0

        self.char_labels = []
        for char in self.text:
            lbl = ctk.CTkLabel(self.label_frame, text=char, font=ctk.CTkFont(size=24, weight="bold"))
            lbl.pack(side="left")
            self.char_labels.append(lbl)

        self.animate_rainbow_letters()
        self.entry_user = ctk.CTkEntry(inner, placeholder_text="Username", width=250)
        self.entry_user.pack(pady=5)

        self.pass_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.pass_frame.pack(pady=5)
        self.entry_pass = ctk.CTkEntry(self.pass_frame, placeholder_text="Password", show="●", width=210)
        self.entry_pass.pack(side="left", padx=(0, 5))

        self.show_password = False
        self.toggle_button = ctk.CTkButton(self.pass_frame, text="👁", width=30, command=self.toggle_password)
        self.toggle_button.pack(side="left")

        self.btn_login = ctk.CTkButton(inner, text="Đăng nhập", command=self.dang_nhap, width=250)
        self.btn_login.pack(pady=20)

        self.label_error = ctk.CTkLabel(inner, text="", text_color="red")
        self.label_error.pack()

        # ===== RIGHT IMAGE =====
        self.image_label = tk.Label(self, width=600, height=700)
        self.image_label.grid(row=0, column=1, sticky="nsew")

        try:
            self.original_image = Image.open("C:/Users/admin/.vscode/Python/oop/nv.png")
        except Exception as e:
            print("Không thể mở ảnh:", e)
            self.original_image = Image.new("RGB", (600, 700), color="gray")

        self.tk_image = None

        self.update_idletasks()  # Cập nhật kích thước layout
        self.resize_image()      # Hiển thị ảnh ngay lập tức

        self.bind("<Configure>", self.delayed_resize)
        self._resize_after_id = None

    def fade_in(self):
        if self.fade_in_alpha < 1.0:
            self.fade_in_alpha += 0.05
            self.attributes("-alpha", self.fade_in_alpha)
            self.after(30, self.fade_in)

    def toggle_password(self):
        if self.show_password:
            self.entry_pass.configure(show="●")
            self.toggle_button.configure(text="👁")
        else:
            self.entry_pass.configure(show="")
            self.toggle_button.configure(text="🙈")
        self.show_password = not self.show_password

    def dang_nhap(self):
        user = self.entry_user.get()
        pw = self.entry_pass.get()
        if user == "admin" and pw == "admin":
            self.destroy()
            App(role="admin").mainloop()
        elif user == "nv" and pw == "123":
            self.destroy()
            App(role="nhanvien").mainloop()
        else:
            self.label_error.configure(text="Sai thông tin đăng nhập")

    def animate_rainbow_letters(self):
        for i, lbl in enumerate(self.char_labels):
            color = self.colors[(self.color_index + i) % len(self.colors)]
            lbl.configure(text_color=color)
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.after(200, self.animate_rainbow_letters)
    def delayed_resize(self, event):
        if self._resize_after_id:
            self.after_cancel(self._resize_after_id)
        self._resize_after_id = self.after(150, self.resize_image)

    def resize_image(self):
        img_width = self.image_label.winfo_width()
        img_height = self.image_label.winfo_height()
        if img_width > 0 and img_height > 0:
            resized = self.original_image.resize((img_width, img_height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(resized)
            self.image_label.config(image=self.tk_image)

class App(ctk.CTk):
    def __init__(self, role="admin"):
        super().__init__()
        self.title("Quản lý nhân viên")
        self.geometry("1200x1200")
        ctk.set_appearance_mode("dark")

        self.role = role
        self.danh_sach_nv = DanhSachNhanVien()
        try:
            self.danh_sach_nv.doc_file_json("nhanvien.json")
        except:
            pass

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(padx=20, pady=10, fill="both")

        fields = ["Mã NV", "Họ tên", "Ngày sinh", "Giới tính", "Quê quán", "Email", "SĐT", "Phòng ban", "Năm vào làm"]
        self.entries = {}
        for field in fields:
            entry = ctk.CTkEntry(self.frame, placeholder_text=field)
            entry.pack(pady=5, fill='x', padx=100)
            self.entries[field] = entry

        self.frame2 = ctk.CTkFrame(self)
        self.frame2.pack(pady=10)

        self.entry_search = ctk.CTkEntry(self.frame2, placeholder_text="Tìm theo mã hoặc tên", width=200)
        self.entry_search.grid(row=0, column=0, padx=5)
        self.btn_search = ctk.CTkButton(self.frame2, text="Tìm", command=self.tim_nv, fg_color="#2196F3", hover_color="#1976D2")
        self.btn_search.grid(row=0, column=1, padx=5)

        if self.role == "admin":
            self.btn_add = ctk.CTkButton(self.frame2, text="Thêm", command=self.them_nv, fg_color="#4CAF50", hover_color="#45a049")
            self.btn_add.grid(row=0, column=2, padx=5)
            self.btn_delete = ctk.CTkButton(self.frame2, text="Xoá", command=self.xoa_nv, fg_color="#f44336", hover_color="#d32f2f")
            self.btn_delete.grid(row=0, column=3, padx=5)

        self.btn_csv = ctk.CTkButton(self.frame2, text="Xuất CSV", command=self.xuat_csv, fg_color="#FFC107", hover_color="#FFB300")
        self.btn_csv.grid(row=0, column=4, padx=5)

        self.btn_load = ctk.CTkButton(self.frame2, text="Đọc JSON", command=self.doc_file, fg_color="#9E9E9E", hover_color="#757575")
        self.btn_load.grid(row=1, column=0, padx=5, pady=5)

        if self.role == "admin":
            self.btn_save = ctk.CTkButton(self.frame2, text="Lưu JSON", command=lambda: self.danh_sach_nv.luu_file_json("nhanvien.json"), fg_color="#4CAF50", hover_color="#45a049")
            self.btn_save.grid(row=1, column=1, padx=5, pady=5)

        self.btn_logout = ctk.CTkButton(self.frame2, text="Đăng xuất", command=self.dang_xuat, fg_color="#f44336", hover_color="#d32f2f")
        self.btn_logout.grid(row=1, column=2, padx=5, pady=5)

        self.output = ctk.CTkTextbox(self, height=250, state="normal", wrap="word")
        self.output.pack(padx=20, pady=10, fill="both")
        self.hien_thi_danh_sach()

    def them_nv(self):
        try:
            data = [self.entries[field].get() for field in self.entries]
            nv = NhanVien(
                data[0], data[7], int(data[8]),
                data[1], data[2], data[3], data[4], data[5], data[6]
            )
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

    def dang_xuat(self):
        self.destroy()
        LoginWindow().mainloop()

    def hien_thi_danh_sach(self):
        self.output.delete("1.0", "end")
        for nv in self.danh_sach_nv.ds:
            self.output.insert("end", f"{nv}\n")


if __name__ == "__main__":
    LoginWindow().mainloop()
