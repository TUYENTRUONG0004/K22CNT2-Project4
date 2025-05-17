from flask import Flask, request, jsonify
import pyodbc

# Cấu hình kết nối đến SQL Server
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-5491VFA;" 
    "Database=K22CNT2_TTCD_Project4;"
    "Trusted_Connection=yes;"
)
con = pyodbc.connect(conn_str)

app = Flask(__name__)
from flask import Flask, request, jsonify, render_template
# ... (kết nối DB như trước)

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')


# Hàm tiện ích: truy vấn và trả về JSON
def fetch_all(table):
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    cols = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    return [dict(zip(cols, row)) for row in rows]

# 1. QUẢN TRỊ
@app.route('/quantri', methods=['GET'])
def get_quantri():
    try:
        return jsonify(fetch_all('QuanTri'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/quantri', methods=['POST'])
def add_quantri():
    try:
        data = request.get_json()
        tk = data.get('Tai_khoan')
        mk = data.get('Mat_khau')
        tt = data.get('Trang_thai')
        cursor = con.cursor()
        sql = "INSERT INTO QuanTri (id_quan_tri, Tai_khoan, Mat_khau, Trang_thai) VALUES (?, ?, ?, ?)"
        # id_quan_tri có thể điều chỉnh tự động nếu có SEQUENCE/IDENTITY
        cursor.execute(sql, (data.get('id_quan_tri'), tk, mk, tt))
        con.commit()
        cursor.close()
        return jsonify({'message': 'Thêm quản trị thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 2. DANH MỤC
@app.route('/danhmuc', methods=['GET'])
def get_danhmuc():
    try:
        return jsonify(fetch_all('DanhMuc'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/danhmuc', methods=['POST'])
def add_danhmuc():
    try:
        data = request.get_json()
        cursor = con.cursor()
        sql = "INSERT INTO DanhMuc (id_danh_muc, ten_danh_muc) VALUES (?, ?)"
        cursor.execute(sql, (data.get('id_danh_muc'), data.get('ten_danh_muc')))
        con.commit()
        cursor.close()
        return jsonify({'message': 'Thêm danh mục thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 3. SẢN PHẨM
@app.route('/sanpham', methods=['GET'])
def get_sanpham():
    try:
        return jsonify(fetch_all('SanPham'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sanpham', methods=['POST'])
def add_sanpham():
    try:
        data = request.get_json()
        cursor = con.cursor()
        sql = ("INSERT INTO SanPham (id_san_pham, ten_san_pham, gia, so_luong, hinh_anh, id_danh_muc) "
               "VALUES (?, ?, ?, ?, ?, ?)")
        cursor.execute(sql, (
            data.get('id_san_pham'), data.get('ten_san_pham'), data.get('gia'),
            data.get('so_luong'), data.get('hinh_anh'), data.get('id_danh_muc')
        ))
        con.commit()
        cursor.close()
        return jsonify({'message': 'Thêm sản phẩm thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 4. KHÁCH HÀNG
@app.route('/khachhang', methods=['GET'])
def get_khachhang():
    try:
        return jsonify(fetch_all('KhachHang'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/khachhang', methods=['POST'])
def add_khachhang():
    try:
        data = request.get_json()
        cursor = con.cursor()
        sql = ("INSERT INTO KhachHang (id_khach_hang, ten_khach_hang, so_dien_thoai, email, dia_chi, ngay_tao) "
               "VALUES (?, ?, ?, ?, ?, ?)" )
        cursor.execute(sql, (
            data.get('id_khach_hang'), data.get('ten_khach_hang'), data.get('so_dien_thoai'),
            data.get('email'), data.get('dia_chi'), data.get('ngay_tao')
        ))
        con.commit()
        cursor.close()
        return jsonify({'message': 'Thêm khách hàng thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 5. GIỎ HÀNG
@app.route('/giohang', methods=['GET'])
def get_giohang():
    try:
        return jsonify(fetch_all('GioHang'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/giohang', methods=['POST'])
def add_giohang():
    try:
        data = request.get_json()
        cursor = con.cursor()
        sql = ("INSERT INTO GioHang (id_gio_hang, id_khach_hang, id_san_pham, so_luong, ngay_them) "
               "VALUES (?, ?, ?, ?, ?)")
        cursor.execute(sql, (
            data.get('id_gio_hang'), data.get('id_khach_hang'), data.get('id_san_pham'),
            data.get('so_luong'), data.get('ngay_them')
        ))
        con.commit()
        cursor.close()
        return jsonify({'message': 'Thêm giỏ hàng thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 6. ĐƠN HÀNG
@app.route('/donhang', methods=['GET'])
def get_donhang():
    try:
        return jsonify(fetch_all('DonHang'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/donhang', methods=['POST'])
def add_donhang():
    try:
        data = request.get_json()
        cursor = con.cursor()
        sql = ("INSERT INTO DonHang (id_don_hang, ngay_dat, id_khach_hang, tong_tien, trang_thai) "
               "VALUES (?, ?, ?, ?, ?)")
        cursor.execute(sql, (
            data.get('id_don_hang'), data.get('ngay_dat'), data.get('id_khach_hang'),
            data.get('tong_tien'), data.get('trang_thai')
        ))
        con.commit()
        cursor.close()
        return jsonify({'message': 'Thêm đơn hàng thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 7. THANH TOÁN
@app.route('/thanhtoan', methods=['GET'])
def get_thanhtoan():
    try:
        return jsonify(fetch_all('ThanhToan'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/thanhtoan', methods=['POST'])
def add_thanhtoan():
    try:
        data = request.get_json()
        cursor = con.cursor()
        sql = ("INSERT INTO ThanhToan (id_thanh_toan, id_don_hang, id_khach_hang, tong_tien, phuong_thuc, trang_thai, thoi_gian) "
               "VALUES (?, ?, ?, ?, ?, ?, ?)")
        cursor.execute(sql, (
            data.get('id_thanh_toan'), data.get('id_don_hang'), data.get('id_khach_hang'),
            data.get('tong_tien'), data.get('phuong_thuc'), data.get('trang_thai'), data.get('thoi_gian')
        ))
        con.commit()
        cursor.close()
        return jsonify({'message': 'Thêm thanh toán thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 8. CHI TIẾT ĐƠN HÀNG
@app.route('/chitietdonhang', methods=['GET'])
def get_chitiet():
    try:
        return jsonify(fetch_all('ChiTietDonHang'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chitietdonhang', methods=['POST'])
def add_chitiet():
    try:
        data = request.get_json()
        cursor = con.cursor()
        sql = ("INSERT INTO ChiTietDonHang (id_chi_tiet, id_don_hang, id_san_pham, so_luong, don_gia) "
               "VALUES (?, ?, ?, ?, ?)")
        cursor.execute(sql, (
            data.get('id_chi_tiet'), data.get('id_don_hang'), data.get('id_san_pham'),
            data.get('so_luong'), data.get('don_gia')
        ))
        con.commit()
        cursor.close()
        return jsonify({'message': 'Thêm chi tiết đơn hàng thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 9. NHÂN VIÊN (mở rộng)
@app.route('/nhanvien', methods=['GET'])
def get_nhanvien():
    try:
        return jsonify(fetch_all('NhanVien'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/nhanvien', methods=['POST'])
def add_nhanvien():
    try:
        data = request.get_json()
        cursor = con.cursor()
        sql = ("INSERT INTO NhanVien (id_nhan_vien, ten_nhan_vien, so_dien_thoai, chuc_vu) "
               "VALUES (?, ?, ?, ?)")
        cursor.execute(sql, (
            data.get('id_nhan_vien'), data.get('ten_nhan_vien'),
            data.get('so_dien_thoai'), data.get('chuc_vu')
        ))
        con.commit()
        cursor.close()
        return jsonify({'message': 'Thêm nhân viên thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/nhanvien/<int:id_nv>', methods=['PUT'])
def update_nhanvien(id_nv):
    try:
        data = request.get_json()
        cursor = con.cursor()
        sql = ("UPDATE NhanVien SET ten_nhan_vien = ?, so_dien_thoai = ?, chuc_vu = ? "
               "WHERE id_nhan_vien = ?")
        cursor.execute(sql, (
            data.get('ten_nhan_vien'), data.get('so_dien_thoai'),
            data.get('chuc_vu'), id_nv
        ))
        con.commit()
        cursor.close()
        return jsonify({'message': 'Cập nhật nhân viên thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
