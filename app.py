import customtkinter as ctk
from datetime import datetime
from tkcalendar import DateEntry
from danh_sach_nhan_vien import DanhSachNhanVien
from nhan_vien import NhanVien

class DateEntryCustom(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master)
        self.cal = DateEntry(self, **kwargs)
        self.cal.pack(fill='both', expand=True)
    def get(self): return self.cal.get()

# Overlay dùng cho logout
def LoadingOverlay(parent, text="Đang xử lý..."):
    overlay = ctk.CTkToplevel(parent)
    overlay.geometry(f"{parent.winfo_width()}x{parent.winfo_height()}+{parent.winfo_x()}+{parent.winfo_y()}")
    overlay.overrideredirect(True)
    overlay.configure(fg_color="#1a1a1a")
    overlay.attributes("-topmost", True)
    label = ctk.CTkLabel(overlay, text=text, font=ctk.CTkFont("Comic Sans MS",20,'bold'), text_color='white')
    label.place(relx=0.42, rely=0.42, anchor="center")
    overlay.update()
    return overlay

class App(ctk.CTk):
    def __init__(self, role='admin'):
        super().__init__()
        self.title('Quản lý nhân viên')
        self.geometry('1000x750')
        ctk.set_appearance_mode('light')
        self.withdraw(); self.attributes('-alpha',0.0)
        self.after(100, self.start_fade_in)

        self.role = role
        self.ds = DanhSachNhanVien()
        try: self.ds.doc_file_json('nhanvien.json')
        except: pass

        # Khung nhập liệu
        frame = ctk.CTkFrame(self, corner_radius=15, fg_color='#f5f5f5')
        frame.pack(fill='x', padx=30, pady=20)
        labels = [('Mã NV','text'),('Họ tên','text'),('Ngày sinh','date'),
                  ('Giới tính','combobox'),('Quê quán','text'),('Email','text'),
                  ('SĐT','text'),('Phòng ban','text'),('Năm vào làm','date')]
        self.inputs={}
        if role=='admin':
            for lbl,typ in labels:
                row=ctk.CTkFrame(frame, fg_color='transparent'); row.pack(fill='x', pady=4)
                ctk.CTkLabel(row,text=lbl,width=120,anchor='w').pack(side='left')
                if typ=='text': inp=ctk.CTkEntry(row,height=35,corner_radius=10)
                elif typ=='combobox': inp=ctk.CTkComboBox(row,values=['Nam','Nữ'],height=35)
                else: inp=DateEntryCustom(row)
                inp.pack(side='left',fill='x',expand=True)
                self.inputs[lbl]=inp

        # Controls
        ctrl = ctk.CTkFrame(self)
        ctrl.pack(pady=10)
        # Search button màu xanh lam
        self.search = ctk.CTkEntry(ctrl, placeholder_text='Tìm mã hoặc tên', width=200)
        self.search.grid(row=0, column=0, padx=5)
        btn_search = ctk.CTkButton(
            ctrl,
            text='Tìm kiếm 🔍',
            command=self.tim,
            fg_color='#1E90FF', hover_color='#63B8FF', text_color='white'
        )
        btn_search.grid(row=0, column=1, padx=5)
        # Thêm
        if role=='admin':
            btn_add = ctk.CTkButton(
                ctrl,
                text='Thêm ➕',
                command=self.them,
                fg_color='#4CAF50', hover_color='#66BB6A', text_color='white'
            )
            btn_add.grid(row=0, column=2, padx=5)
        # Xóa màu đỏ
        if role=='admin':
            btn_delete = ctk.CTkButton(
                ctrl,
                text='Xóa 🗑️',
                command=self.xoa,
                fg_color='#B22222', hover_color='#CD5C5C', text_color='white'
            )
            btn_delete.grid(row=0, column=3, padx=5)
        # Xuất CSV màu vàng
        btn_csv = ctk.CTkButton(
            ctrl,
            text='📄 Xuất file CSV',
            command=self.xuat_csv,
            fg_color='#FFD700', hover_color='#FFEC8B', text_color='black'
        )
        btn_csv.grid(row=0, column=4, padx=5)
        # Đọc JSON màu xanh lá cây
        btn_load = ctk.CTkButton(
            ctrl,
            text='📂 Đọc JSON',
            command=self.doc,
            fg_color='#32CD32', hover_color='#7CFC00', text_color='white'
        )
        btn_load.grid(row=1, column=0, padx=5, pady=5)
        # Lưu JSON (giữ màu mặc định)
        if role=='admin':
            btn_save = ctk.CTkButton(
                ctrl,
                text='💾 Lưu JSON',
                command=lambda: self.ds.luu_file_json('nhanvien.json')
            )
            btn_save.grid(row=1, column=1, padx=5, pady=5)
        # Đăng xuất màu đỏ
        btn_logout = ctk.CTkButton(
            ctrl,
            text='🚪 Đăng xuất',
            command=self.logout,
            fg_color='#B22222', hover_color='#CD5C5C', text_color='white'
        )
        btn_logout.grid(row=1, column=2, padx=5, pady=5)

        # Output
        self.output = ctk.CTkTextbox(self, height=300, font=('Consolas',14))
        self.output.pack(fill='both', padx=30, pady=10)
        self.hien()

    def start_fade_in(self):
        self.deiconify(); self.state('zoomed'); self.after(20,self.fade_in)
    def fade_in(self):
        a=self.attributes('-alpha')
        if a<1:self.attributes('-alpha',a+0.05); self.after(20,self.fade_in)
    def fade_out(self,cb=None):
        a=self.attributes('-alpha')
        if a>0:self.attributes('-alpha',a-0.05); self.after(20,lambda:self.fade_out(cb))
        else: cb()

    def hien(self):
        self.output.delete('1.0','end')
        for nv in self.ds.ds: self.output.insert('end',f"{nv}\n")
    def them(self):
        try:
            vals = [self.inputs[l].get() for l in self.inputs]
            ngay_vaolam = datetime.strptime(vals[8], "%m/%d/%y")  # hoặc thử các định dạng khác tùy hệ thống
            nam_vaolam = ngay_vaolam.year
            nv = NhanVien(vals[0], vals[7], nam_vaolam, vals[1], vals[2], vals[3], vals[4], vals[5], vals[6])
            self.ds.them(nv)
            self.ds.luu_file_json('nhanvien.json')
            self.output.insert('end', f"Thêm: {nv}\n")
        except Exception as e:
            self.output.insert('end', f"Lỗi thêm: {e}\n")
    def doc(self):
        try:
            self.ds.doc_file_json('nhanvien.json'); self.hien()
        except Exception as e: self.output.insert('end',f"Lỗi đọc: {e}\n")
    def tim(self):
        self.output.delete('1.0','end');
        for nv in self.ds.tim_kiem(self.search.get()): self.output.insert('end',f"{nv}\n")
    def xoa(self):
        self.ds.xoa(self.search.get()); self.ds.luu_file_json('nhanvien.json'); self.output.insert('end',f"Xóa: {self.search.get()}\n")
    def xuat_csv(self):
        try:
            self.ds.doc_file_json('nhanvien.json'); self.ds.xuat_file_csv('nhanvien.csv'); self.output.insert('end','Xuất CSV thành công\n')
        except Exception as e: self.output.insert('end',f"Lỗi CSV: {e}\n")
    def logout(self):
        overlay=LoadingOverlay(self,text='Đang đăng xuất...')
        self.after(1000,lambda: self.fade_out(self._back_login))
    def _back_login(self):
        self.destroy()
        from loginwindow import LoginWindow; LoginWindow().mainloop()