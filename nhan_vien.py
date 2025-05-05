from con_nguoi import ConNguoi

class NhanVien(ConNguoi):
    def __init__(self, ma_nv, phong_ban, nam_vao_lam, *args):
        super().__init__(*args)
        self._ma_nv = ma_nv
        self._phong_ban = phong_ban
        self._nam_vao_lam = nam_vao_lam

    @property
    def ho_ten(self):
        return self._ho_ten

    @ho_ten.setter
    def ho_ten(self, value):
        self._ho_ten = value
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "ma_nv": self._ma_nv,
            "phong_ban": self._phong_ban,
            "nam_vao_lam": self._nam_vao_lam
        })
        return data

    @staticmethod
    def from_dict(data):
        return NhanVien(
            data['ma_nv'],
            data['phong_ban'],
            data['nam_vao_lam'],
            data['ho_ten'],
            data['ngay_sinh'],
            data['gioi_tinh'],
            data['que_quan'],
            data['email'],
            data['sdt']
        )

    def __str__(self):
        return f"{self._ma_nv} - {self._ho_ten} - {self._phong_ban}"