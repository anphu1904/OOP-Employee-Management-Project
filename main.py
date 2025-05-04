import customtkinter as ctk
import tkinter as tk
from tkcalendar import DateEntry
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
        ctk.set_default_color_theme("green")

        self.attributes("-alpha", 0.0)
        self.fade_in_alpha = 0.0
        self.after(10, self.fade_in)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.login_frame = ctk.CTkFrame(self, corner_radius=20, border_width=1)
        self.login_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        inner.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.label_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.label_frame.pack(pady=10)
        self.text = "Hi, Welcome back !"
        self.colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
        self.color_index = 0
        self.char_labels = []
        for char in self.text:
            lbl = ctk.CTkLabel(
                self.label_frame,
                text=char,
                font=ctk.CTkFont("Segoe UI", size=24, weight="bold", slant="italic")
            )
            lbl.pack(side="left")
            self.char_labels.append(lbl)
        self.animate_rainbow_letters()

        self.entry_user = ctk.CTkEntry(inner, placeholder_text="Username", width=250, corner_radius=15)
        self.entry_user.pack(pady=5)

        self.pass_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.pass_frame.pack(pady=5)
        self.entry_pass = ctk.CTkEntry(self.pass_frame, placeholder_text="Password", show="●", width=210, corner_radius=15)
        self.entry_pass.pack(side="left", padx=(0, 5))
        self.show_password = False
        self.toggle_button = ctk.CTkButton(self.pass_frame, text="👁", width=30, command=self.toggle_password)
        self.toggle_button.pack(side="left")

        self.btn_login = ctk.CTkButton(inner, text="Đăng nhập", command=self.dang_nhap, width=250, fg_color="#007BFF", hover_color="#0056b3")
        self.btn_login.pack(pady=20)

        self.label_error = ctk.CTkLabel(inner, text="", text_color="red")
        self.label_error.pack()

        self.image_label = tk.Label(self, width=600, height=700)
        self.image_label.grid(row=0, column=1, sticky="nsew")
        try:
            self.original_image = Image.open("C:/Users/admin/.vscode/Python/oop/nv.png")
        except Exception as e:
            print("Không thể mở ảnh:", e)
            self.original_image = Image.new("RGB", (600, 700), color="gray")
        self.tk_image = None
        self.update_idletasks()
        self.resize_image()
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
class DateEntryCustom(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master)
        self.cal = DateEntry(self, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', **kwargs)
        self.cal.pack(fill="both", expand=True)

    def get(self):
        return self.cal.get()

class App(ctk.CTk):
    def __init__(self, role="admin"):
        super().__init__()
        self.title("Quản lý nhân viên")
        self.geometry("1000x750")
        ctk.set_appearance_mode("light")

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

    def them_nv(self):
        try:
            data = [self.entries[field].get() for field in self.entries]
            nv = NhanVien(
                data[0], data[7], int(data[8][-4:]),  # Năm từ chuỗi ngày
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
        from main import LoginWindow
        LoginWindow().mainloop()

    def hien_thi_danh_sach(self):
        self.output.delete("1.0", "end")
        for nv in self.danh_sach_nv.ds:
            self.output.insert("end", f"{nv}\n")

if __name__ == "__main__":
    from main import LoginWindow
    LoginWindow().mainloop()