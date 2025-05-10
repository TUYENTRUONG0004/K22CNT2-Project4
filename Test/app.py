from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort
import pyodbc
from flask_cors import CORS

# --- SQL Server Connection Configuration ---
CONN_STR = (
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=DESKTOP-5491VFA;'
    'Database=K22CNT2_Project4;'
    'Trusted_Connection=yes;'
)

def get_connection():
    return pyodbc.connect(CONN_STR)

# Initialize Flask & Flask-RESTful
app = Flask(__name__)
CORS(app)
api = Api(app)

# Utility to convert cursor results to list of dicts
def to_dicts(cursor):
    cols = [col[0] for col in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

# --- Resources ---

class BaseResource:
    table = None
    pk = None
    fields = []

    @classmethod
    def get_all(cls):
        conn = get_connection(); cur = conn.cursor()
        cur.execute(f"SELECT * FROM {cls.table}")
        data = to_dicts(cur)
        conn.close()
        return data, 200

    @classmethod
    def get_one(cls, id):
        conn = get_connection(); cur = conn.cursor()
        cur.execute(f"SELECT * FROM {cls.table} WHERE {cls.pk}=?", id)
        row = cur.fetchone();
        if not row:
            conn.close()
            abort(404, message=f"{cls.table} with ID={id} not found")
        data = dict(zip([c[0] for c in cur.description], row))
        conn.close()
        return data, 200

    @classmethod
    def create(cls, json_data):
        missing = [f for f in [cls.pk]+cls.fields if f not in json_data]
        if missing:
            abort(400, message=f"Missing fields {missing}")
        cols = [cls.pk] + cls.fields
        vals = [json_data[f] for f in cols]
        placeholders = ','.join(['?']*len(cols))
        conn = get_connection(); cur = conn.cursor()
        cur.execute(
            f"INSERT INTO {cls.table} ({','.join(cols)}) VALUES ({placeholders})", tuple(vals)
        )
        conn.commit(); conn.close()
        return {'message': f'{cls.table} created'}, 201

    @classmethod
    def update(cls, id, json_data):
        sets = []
        vals = []
        for f in cls.fields:
            if f in json_data:
                sets.append(f"{f}=?")
                vals.append(json_data[f])
        if not sets:
            abort(400, message="No fields to update")
        vals.append(id)
        conn = get_connection(); cur = conn.cursor()
        cur.execute(
            f"UPDATE {cls.table} SET {','.join(sets)} WHERE {cls.pk}=?", tuple(vals)
        )
        if cur.rowcount == 0:
            conn.close(); abort(404, message=f"{cls.table} with ID={id} not found")
        conn.commit(); conn.close()
        return {'message': f'{cls.table} updated'}, 200

    @classmethod
    def delete(cls, id):
        conn = get_connection(); cur = conn.cursor()
        cur.execute(f"DELETE FROM {cls.table} WHERE {cls.pk}=?", id)
        if cur.rowcount == 0:
            conn.close(); abort(404, message=f"{cls.table} with ID={id} not found")
        conn.commit(); conn.close()
        return {'message': f'{cls.table} deleted'}, 200

# Dynamically define resources for each table

class QuanTriResource(Resource, BaseResource):
    table = 'QuanTri'
    pk = 'id_quan_tri'
    fields = ['Tai_khoan','Mat_khau','Trang_thai']

class DanhMucResource(Resource, BaseResource):
    table = 'DanhMuc'
    pk = 'id_danh_muc'
    fields = ['ten_danh_muc']

class SanPhamResource(Resource, BaseResource):
    table = 'SanPham'
    pk = 'id_san_pham'
    fields = ['ten_san_pham','gia','so_luong','hinh_anh','id_danh_muc']

class KhachHangResource(Resource, BaseResource):
    table = 'KhachHang'
    pk = 'id_khach_hang'
    fields = ['ten_khach_hang','so_dien_thoai','email','dia_chi','ngay_tao']

class GioHangResource(Resource, BaseResource):
    table = 'GioHang'
    pk = 'id_gio_hang'
    fields = ['id_khach_hang','id_san_pham','so_luong','ngay_them']

class DonHangResource(Resource, BaseResource):
    table = 'DonHang'
    pk = 'id_don_hang'
    fields = ['ngay_dat','id_khach_hang','tong_tien','trang_thai']

class ThanhToanResource(Resource, BaseResource):
    table = 'ThanhToan'
    pk = 'id_thanh_toan'
    fields = ['id_don_hang','id_khach_hang','tong_tien','phuong_thuc','trang_thai','thoi_gian']

class ChiTietDonHangResource(Resource, BaseResource):
    table = 'ChiTietDonHang'
    pk = 'id_chi_tiet'
    fields = ['id_don_hang','id_san_pham','so_luong','don_gia']

class NhanVienResource(Resource, BaseResource):
    table = 'NhanVien'
    pk = 'id_nhan_vien'
    fields = ['ten_nhan_vien','so_dien_thoai','chuc_vu']

# Register endpoints
resources = [
    (QuanTriResource, '/quantri'),
    (DanhMucResource, '/danhmuc'),
    (SanPhamResource, '/sanpham'),
    (KhachHangResource, '/khachhang'),
    (GioHangResource, '/giohang'),
    (DonHangResource, '/donhang'),
    (ThanhToanResource, '/thanhtoan'),
    (ChiTietDonHangResource, '/chitietdonhang'),
    (NhanVienResource, '/nhanvien'),
]
for res, route in resources:
    api.add_resource(res,
        route,
        f"{route}/<int:id>"
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
