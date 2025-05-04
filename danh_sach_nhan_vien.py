import json
from typing import List
from nhan_vien import NhanVien

class DanhSachNhanVien:
    def __init__(self):
        self.ds: List[NhanVien] = []

    def them(self, nv: NhanVien):
        self.ds.append(nv)

    def xoa(self, ma_nv: str):
        self.ds = [nv for nv in self.ds if nv._ma_nv != ma_nv]

    def tim_kiem(self, tu_khoa: str):
        return [nv for nv in self.ds if tu_khoa.lower() in nv._ho_ten.lower() or tu_khoa in nv._ma_nv]

    def luu_file_json(self, ten_file):
        with open(ten_file, 'w', encoding='utf-8') as f:
            json.dump([nv.to_dict() for nv in self.ds], f, ensure_ascii=False, indent=4)

    def doc_file_json(self, ten_file):
        with open(ten_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.ds = [NhanVien.from_dict(nv) for nv in data]

    def xuat_file_csv(self, ten_file):
        import csv
        with open(ten_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Ma NV", "Ho Ten", "Ngay Sinh", "Gioi Tinh", "Que Quan", "Email", "SDT", "Phong Ban", "Nam Vao Lam"])
            for nv in self.ds:
                writer.writerow([
                    nv._ma_nv, nv._ho_ten, nv._ngay_sinh, nv._gioi_tinh, nv._que_quan,
                    nv._email, nv._sdt, nv._phong_ban, nv._nam_vao_lam
                ])