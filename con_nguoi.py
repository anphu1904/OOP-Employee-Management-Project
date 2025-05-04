class ConNguoi:
    def __init__(self, ho_ten, ngay_sinh, gioi_tinh, que_quan, email, sdt):
        self._ho_ten = ho_ten
        self._ngay_sinh = ngay_sinh
        self._gioi_tinh = gioi_tinh
        self._que_quan = que_quan
        self._email = email
        self._sdt = sdt

    def to_dict(self):
        return {
            "ho_ten": self._ho_ten,
            "ngay_sinh": self._ngay_sinh,
            "gioi_tinh": self._gioi_tinh,
            "que_quan": self._que_quan,
            "email": self._email,
            "sdt": self._sdt,
        }

    @staticmethod
    def from_dict(data):
        return ConNguoi(
            data['ho_ten'], data['ngay_sinh'], data['gioi_tinh'],
            data['que_quan'], data['email'], data['sdt']
        )