from flask import Flask, request, jsonify, send_from_directory
import pyodbc
import os
from flask_cors import CORS
import logging
from datetime import datetime  # Import datetime từ module chuẩn
import webbrowser

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Cấu hình kết nối đến SQL Server
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-5491VFA;"
    "Database=K22CNT2_TTCD_Project4;"
    "Trusted_Connection=yes;"
)
try:
    conn = pyodbc.connect(conn_str)
    logger.info("Kết nối cơ sở dữ liệu thành công")
except pyodbc.Error as e:
    logger.error(f"Lỗi kết nối cơ sở dữ liệu: {str(e)} - Chi tiết: {e.args}")
    raise

app = Flask(__name__)
CORS(app)

# Hàm tiện ích: truy vấn và trả về JSON
def fetch_all(table):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        cols = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        return [dict(zip(cols, row)) for row in rows]
    except pyodbc.Error as e:
        logger.error(f"Lỗi truy vấn {table}: {str(e)}")
        return []

# Route để phục vụ các trang Shopthoitrang
@app.route('/trang-chu/')
def trang_chu():
    return send_from_directory(os.path.join('Shopthoitrang', 'trang-chu'), 'trang-chu.html')

@app.route('/chi-tiet-san-pham/')
def chi_tiet_san_pham():
    return send_from_directory(os.path.join('Shopthoitrang', 'chi-tiet-san-pham'), 'chi-tiet-san-pham.html')

@app.route('/gio-hang/')
def gio_hang():
    return send_from_directory(os.path.join('Shopthoitrang', 'gio-hang'), 'gio-hang.html')

@app.route('/dat-hang/')
def dat_hang():
    return send_from_directory(os.path.join('Shopthoitrang', 'dat-hang'), 'dat-hang.html')

@app.route('/lich-su-don-hang/')
def lich_su_don_hang():
    return send_from_directory(os.path.join('Shopthoitrang', 'lich-su-don-hang'), 'lich-su-don-hang.html')

@app.route('/admin-thanhtoan/')
def admin_thanhtoan():
    return send_from_directory('.', 'admin-thanhtoan.html')

# Route để phục vụ CSS, JS, images từ Shopthoitrang
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join('Shopthoitrang', 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join('Shopthoitrang', 'js'), filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join('Shopthoitrang', 'images'), filename)

# Route để phục vụ trang admin
@app.route('/admin/')
def admin():
    return send_from_directory('.', 'admin.html')

@app.route('/admin-products/')
def admin_products():
    return send_from_directory('.', 'admin-products.html')

# API: Sản phẩm
@app.route('/sanpham', methods=['GET'])
def get_sanpham():
    try:
        products = fetch_all('SanPham')
        return jsonify(products)
    except Exception as e:
        logger.error(f"Lỗi API /sanpham GET: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/sanpham', methods=['POST'])
def add_sanpham():
    try:
        data = request.form.to_dict()
        if 'hinh_anh' in request.files:
            file = request.files['hinh_anh']
            if file.filename:
                upload_folder = os.path.join('Shopthoitrang', 'images')
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, file.filename)
                file.save(file_path)
                data['hinh_anh'] = f'/images/{file.filename}'
        cursor = conn.cursor()
        sql = ("INSERT INTO SanPham (id_san_pham, ten_san_pham, gia, so_luong, hinh_anh, id_danh_muc) "
               "VALUES (?, ?, ?, ?, ?, ?)")
        cursor.execute(sql, (
            int(data.get('id_san_pham')),
            data.get('ten_san_pham'),
            float(data.get('gia')),
            int(data.get('so_luong')),
            data.get('hinh_anh', ''),
            int(data.get('id_danh_muc'))
        ))
        conn.commit()
        cursor.close()
        logger.info(f"Thêm sản phẩm thành công: {data.get('ten_san_pham')}")
        return jsonify({'message': 'Thêm sản phẩm thành công', 'hinh_anh': data.get('hinh_anh')}), 201
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /sanpham POST - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi thêm sản phẩm: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /sanpham POST - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/sanpham/<int:id_san_pham>', methods=['PUT'])
def update_sanpham(id_san_pham):
    try:
        data = request.form.to_dict()
        if 'hinh_anh' in request.files:
            file = request.files['hinh_anh']
            if file.filename:
                upload_folder = os.path.join('Shopthoitrang', 'images')
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, file.filename)
                file.save(file_path)
                data['hinh_anh'] = f'/images/{file.filename}'
        cursor = conn.cursor()
        sql = ("UPDATE SanPham SET ten_san_pham = ?, gia = ?, so_luong = ?, hinh_anh = ?, id_danh_muc = ? "
               "WHERE id_san_pham = ?")
        cursor.execute(sql, (
            data.get('ten_san_pham'),
            float(data.get('gia')),
            int(data.get('so_luong')),
            data.get('hinh_anh', ''),
            int(data.get('id_danh_muc')),
            id_san_pham
        ))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Sản phẩm không tồn tại'}), 404
        conn.commit()
        cursor.close()
        logger.info(f"Cập nhật sản phẩm thành công: ID {id_san_pham}")
        return jsonify({'message': 'Cập nhật sản phẩm thành công'}), 200
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /sanpham PUT - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi cập nhật sản phẩm: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /sanpham PUT - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/sanpham/<int:id_san_pham>', methods=['DELETE'])
def delete_sanpham(id_san_pham):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SanPham WHERE id_san_pham = ?", (id_san_pham,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Sản phẩm không tồn tại'}), 404
        conn.commit()
        cursor.close()
        logger.info(f"Xóa sản phẩm thành công: ID {id_san_pham}")
        return jsonify({'message': 'Xóa sản phẩm thành công'}), 200
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /sanpham DELETE - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi xóa sản phẩm: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /sanpham DELETE - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

# API: Danh mục
@app.route('/danhmuc', methods=['GET'])
def get_danhmuc():
    try:
        categories = fetch_all('DanhMuc')
        return jsonify(categories)
    except Exception as e:
        logger.error(f"Lỗi API /danhmuc GET: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/danhmuc', methods=['POST'])
def add_danhmuc():
    try:
        data = request.get_json()
        if not all(key in data for key in ['id_danh_muc', 'ten_danh_muc']):
            return jsonify({'error': 'Thiếu thông tin bắt buộc (id_danh_muc, ten_danh_muc)'}), 400

        cursor = conn.cursor()
        sql = "INSERT INTO DanhMuc (id_danh_muc, ten_danh_muc) VALUES (?, ?)"
        cursor.execute(sql, (
            data.get('id_danh_muc'),
            data.get('ten_danh_muc')
        ))
        conn.commit()
        cursor.close()
        logger.info(f"Thêm danh mục thành công: ID {data.get('id_danh_muc')}")
        return jsonify({'message': 'Thêm danh mục thành công'}), 201
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /danhmuc POST - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi thêm danh mục: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /danhmuc POST - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    

@app.route('/danhmuc/<int:id_danh_muc>', methods=['DELETE'])
def delete_danhmuc(id_danh_muc):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM DanhMuc WHERE id_danh_muc = ?", (id_danh_muc,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Danh mục không tồn tại'}), 404
        conn.commit()
        cursor.close()
        logger.info(f"Xóa danh mục thành công: ID {id_danh_muc}")
        return jsonify({'message': 'Xóa danh mục thành công'}), 200
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /danhmuc DELETE - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi xóa danh mục: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /danhmuc DELETE - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

# API: Đơn hàng
@app.route('/donhang', methods=['GET'])
def get_donhang():
    try:
        orders = fetch_all('DonHang')
        return jsonify(orders)
    except Exception as e:
        logger.error(f"Lỗi API /donhang GET: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/donhang/<int:id_don_hang>', methods=['GET'])
def get_donhang_by_id(id_don_hang):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM DonHang WHERE id_don_hang = ?", (id_don_hang,))
        cols = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return jsonify({'error': 'Đơn hàng không tồn tại'}), 404
        order = dict(zip(cols, row))
        return jsonify(order)
    except Exception as e:
        logger.error(f"Lỗi API /donhang/<id_don_hang> GET: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/donhang', methods=['POST'])
def add_donhang():
    try:
        data = request.get_json()
        if not all(key in data for key in ['id_don_hang', 'id_khach_hang', 'tong_tien']):
            return jsonify({'error': 'Thiếu thông tin bắt buộc (id_don_hang, id_khach_hang, tong_tien)'}), 400

        cursor = conn.cursor()
        sql = ("INSERT INTO DonHang (id_don_hang, ngay_dat, id_khach_hang, tong_tien, trang_thai) "
               "VALUES (?, ?, ?, ?, ?)")
        cursor.execute(sql, (
            data.get('id_don_hang'),
            datetime.now(),
            data.get('id_khach_hang'),
            data.get('tong_tien'),
            data.get('trang_thai', 'Chờ xác nhận')
        ))
        conn.commit()
        cursor.close()
        logger.info(f"Thêm đơn hàng thành công: ID {data.get('id_don_hang')}")
        return jsonify({'message': 'Thêm đơn hàng thành công'}), 201
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /donhang POST - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi thêm đơn hàng: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /donhang POST - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/donhang/<int:id_don_hang>', methods=['PUT'])
def update_donhang(id_don_hang):
    try:
        data = request.get_json()
        if 'trang_thai' not in data:
            return jsonify({'error': 'Thiếu thông tin bắt buộc (trang_thai)'}), 400

        cursor = conn.cursor()
        sql = "UPDATE DonHang SET trang_thai = ? WHERE id_don_hang = ?"
        cursor.execute(sql, (data.get('trang_thai'), id_don_hang))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Đơn hàng không tồn tại'}), 404
        conn.commit()
        cursor.close()
        logger.info(f"Cập nhật đơn hàng thành công: ID {id_don_hang}")
        return jsonify({'message': 'Cập nhật đơn hàng thành công'}), 200
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /donhang PUT - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi cập nhật đơn hàng: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /donhang PUT - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/donhang/<int:id_don_hang>', methods=['DELETE'])
def delete_donhang(id_don_hang):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM DonHang WHERE id_don_hang = ?", (id_don_hang,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Đơn hàng không tồn tại'}), 404
        conn.commit()
        cursor.close()
        logger.info(f"Xóa đơn hàng thành công: ID {id_don_hang}")
        return jsonify({'message': 'Xóa đơn hàng thành công'}), 200
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /donhang DELETE - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi xóa đơn hàng: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /donhang DELETE - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

# API: Chi tiết đơn hàng
@app.route('/chitietdonhang', methods=['POST'])
def add_chitiet():
    try:
        data = request.get_json()
        if not all(key in data for key in ['id_chi_tiet', 'id_don_hang', 'id_san_pham', 'so_luong', 'don_gia']):
            return jsonify({'error': 'Thiếu thông tin bắt buộc'}), 400

        cursor = conn.cursor()
        sql = ("INSERT INTO ChiTietDonHang (id_chi_tiet, id_don_hang, id_san_pham, so_luong, don_gia) "
               "VALUES (?, ?, ?, ?, ?)")
        cursor.execute(sql, (
            data.get('id_chi_tiet'),
            data.get('id_don_hang'),
            data.get('id_san_pham'),
            data.get('so_luong'),
            data.get('don_gia')
        ))
        conn.commit()
        cursor.close()
        logger.info(f"Thêm chi tiết đơn hàng thành công: ID {data.get('id_chi_tiet')}")
        return jsonify({'message': 'Thêm chi tiết đơn hàng thành công'}), 201
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /chitietdonhang POST - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi thêm chi tiết đơn hàng: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /chitietdonhang POST - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/chitietdonhang/<int:id_don_hang>', methods=['GET'])
def get_chitiet_by_donhang(id_don_hang):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ChiTietDonHang WHERE id_don_hang = ?", (id_don_hang,))
        cols = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        details = [dict(zip(cols, row)) for row in rows]
        return jsonify(details)
    except Exception as e:
        logger.error(f"Lỗi API /chitietdonhang/<id_don_hang> GET: {str(e)}")
        return jsonify({'error': str(e)}), 500

# API: Giỏ hàng
@app.route('/giohang', methods=['GET'])
def get_giohang():
    try:
        carts = fetch_all('GioHang')
        return jsonify(carts)
    except Exception as e:
        logger.error(f"Lỗi API /giohang GET: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/giohang', methods=['POST'])
def add_giohang():
    try:
        data = request.get_json()
        if not all(key in data for key in ['id_khach_hang', 'id_san_pham']):
            return jsonify({'error': 'Thiếu thông tin bắt buộc (id_khach_hang, id_san_pham)'}), 400
        if data.get('so_luong', 1) < 1:
            return jsonify({'error': 'Số lượng phải lớn hơn 0'}), 400

        cursor = conn.cursor()
        sql = ("INSERT INTO GioHang (id_khach_hang, id_san_pham, so_luong, ngay_them) "
               "VALUES (?, ?, ?, ?)")
        cursor.execute(sql, (
            data.get('id_khach_hang'),
            data.get('id_san_pham'),
            data.get('so_luong', 1),
            datetime.now()
        ))
        conn.commit()
        cursor.close()
        logger.info(f"Thêm giỏ hàng thành công: Khách {data.get('id_khach_hang')}, Sản phẩm {data.get('id_san_pham')}")
        return jsonify({'message': 'Thêm giỏ hàng thành công'}), 201
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /giohang POST - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi thêm giỏ hàng: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /giohang POST - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/giohang/<int:id_khach_hang>', methods=['GET'])
def get_giohang_by_khachhang(id_khach_hang):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GioHang WHERE id_khach_hang = ?", (id_khach_hang,))
        cols = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        carts = [dict(zip(cols, row)) for row in rows]
        return jsonify(carts)
    except Exception as e:
        logger.error(f"Lỗi API /giohang/<id_khach_hang> GET: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/giohang/<int:id_khach_hang>/<int:id_san_pham>', methods=['PUT'])
def update_giohang(id_khach_hang, id_san_pham):
    try:
        data = request.get_json()
        if 'so_luong' not in data or data.get('so_luong', 1) < 1:
            return jsonify({'error': 'Số lượng phải lớn hơn 0'}), 400

        cursor = conn.cursor()
        cursor.execute(
            "UPDATE GioHang SET so_luong = ? WHERE id_khach_hang = ? AND id_san_pham = ?",
            (data.get('so_luong'), id_khach_hang, id_san_pham)
        )
        if cursor.rowcount == 0:
            return jsonify({'error': 'Không tìm thấy mục giỏ hàng'}), 404
        conn.commit()
        cursor.close()
        logger.info(f"Cập nhật giỏ hàng thành công: Khách {id_khach_hang}, Sản phẩm {id_san_pham}")
        return jsonify({'message': 'Cập nhật giỏ hàng thành công'}), 200
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /giohang PUT - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi cập nhật giỏ hàng: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /giohang PUT - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/giohang/<int:id_khach_hang>/<int:id_san_pham>', methods=['DELETE'])
def delete_giohang_item(id_khach_hang, id_san_pham):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM GioHang WHERE id_khach_hang = ? AND id_san_pham = ?",
            (id_khach_hang, id_san_pham)
        )
        if cursor.rowcount == 0:
            return jsonify({'error': 'Không tìm thấy mục giỏ hàng'}), 404
        conn.commit()
        cursor.close()
        logger.info(f"Xóa sản phẩm khỏi giỏ hàng thành công: Khách {id_khach_hang}, Sản phẩm {id_san_pham}")
        return jsonify({'message': 'Xóa sản phẩm khỏi giỏ hàng thành công'}), 200
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /giohang DELETE item - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi xóa sản phẩm khỏi giỏ hàng: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /giohang DELETE item - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/giohang/<int:id_khach_hang>', methods=['DELETE'])
def delete_giohang(id_khach_hang):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM GioHang WHERE id_khach_hang = ?", (id_khach_hang,))
        conn.commit()
        cursor.close()
        logger.info(f"Xóa giỏ hàng thành công: Khách {id_khach_hang}")
        return jsonify({'message': 'Xóa giỏ hàng thành công'}), 200
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /giohang DELETE all - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi xóa giỏ hàng: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /giohang DELETE all - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
            
# API: Khách hàng
@app.route('/khachhang', methods=['GET'])
def get_khachhang():
    try:
        customers = fetch_all('KhachHang')
        return jsonify(customers)
    except Exception as e:
        logger.error(f"Lỗi API /khachhang GET: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/khachhang/<int:id_khach_hang>', methods=['GET'])
def get_khachhang_by_id(id_khach_hang):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM KhachHang WHERE id_khach_hang = ?", (id_khach_hang,))
        cols = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return jsonify({'error': 'Khách hàng không tồn tại'}), 404
        customer = dict(zip(cols, row))
        return jsonify(customer)
    except Exception as e:
        logger.error(f"Lỗi API /khachhang/<id_khach_hang> GET: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/khachhang', methods=['POST'])
def add_khachhang():
    try:
        data = request.get_json()
        if not all(key in data for key in ['id_khach_hang', 'ten_khach_hang', 'so_dien_thoai', 'ngay_tao']):
            return jsonify({'error': 'Thiếu thông tin bắt buộc (id_khach_hang, ten_khach_hang, so_dien_thoai, ngay_tao)'}), 400

        cursor = conn.cursor()
        sql = ("INSERT INTO KhachHang (id_khach_hang, ten_khach_hang, so_dien_thoai, email, dia_chi, ngay_tao) "
               "VALUES (?, ?, ?, ?, ?, ?)")
        cursor.execute(sql, (
            data.get('id_khach_hang'),
            data.get('ten_khach_hang'),
            data.get('so_dien_thoai'),
            data.get('email', ''),
            data.get('dia_chi', ''),
            data.get('ngay_tao')
        ))
        conn.commit()
        cursor.close()
        logger.info(f"Thêm khách hàng thành công: ID {data.get('id_khach_hang')}")
        return jsonify({'message': 'Thêm khách hàng thành công'}), 201
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /khachhang POST - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi thêm khách hàng: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /khachhang POST - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/khachhang/<int:id_khach_hang>', methods=['PUT'])
def update_khachhang(id_khach_hang):
    try:
        data = request.get_json()
        if not all(key in data for key in ['ten_khach_hang', 'so_dien_thoai']):
            return jsonify({'error': 'Thiếu thông tin bắt buộc (ten_khach_hang, so_dien_thoai)'}), 400

        cursor = conn.cursor()
        sql = ("UPDATE KhachHang SET ten_khach_hang = ?, so_dien_thoai = ?, email = ?, dia_chi = ? "
               "WHERE id_khach_hang = ?")
        cursor.execute(sql, (
            data.get('ten_khach_hang'),
            data.get('so_dien_thoai'),
            data.get('email', ''),
            data.get('dia_chi', ''),
            id_khach_hang
        ))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Khách hàng không tồn tại'}), 404
        conn.commit()
        cursor.close()
        logger.info(f"Cập nhật khách hàng thành công: ID {id_khach_hang}")
        return jsonify({'message': 'Cập nhật khách hàng thành công'}), 200
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /khachhang PUT - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi cập nhật khách hàng: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /khachhang PUT - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/khachhang/<int:id_khach_hang>', methods=['DELETE'])
def delete_khachhang(id_khach_hang):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM KhachHang WHERE id_khach_hang = ?", (id_khach_hang,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Khách hàng không tồn tại'}), 404
        conn.commit()
        cursor.close()
        logger.info(f"Xóa khách hàng thành công: ID {id_khach_hang}")
        return jsonify({'message': 'Xóa khách hàng thành công'}), 200
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /khachhang DELETE - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi xóa khách hàng: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /khachhang DELETE - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
# API: Thanh toán
@app.route('/thanhtoan', methods=['GET'])
def get_thanhtoan():
    try:
        payments = fetch_all('ThanhToan')
        return jsonify(payments)
    except Exception as e:
        logger.error(f"Lỗi API /thanhtoan GET: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/thanhtoan/<int:id_thanh_toan>', methods=['GET'])
def get_thanhtoan_by_id(id_thanh_toan):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ThanhToan WHERE id_thanh_toan = ?", (id_thanh_toan,))
        cols = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return jsonify({'error': 'Thông tin thanh toán không tồn tại'}), 404
        payment = dict(zip(cols, row))
        return jsonify(payment)
    except Exception as e:
        logger.error(f"Lỗi API /thanhtoan/<id_thanh_toan> GET: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/thanhtoan', methods=['POST'])
def add_thanhtoan():
    try:
        data = request.get_json()
        if not all(key in data for key in ['id_thanh_toan', 'id_don_hang', 'id_khach_hang', 'so_tien']):
            return jsonify({'error': 'Thiếu thông tin bắt buộc (id_thanh_toan, id_don_hang, id_khach_hang, so_tien)'}), 400

        cursor = conn.cursor()
        sql = ("INSERT INTO ThanhToan (id_thanh_toan, id_don_hang, id_khach_hang, so_tien, phuong_thuc, trang_thai, ngay_thanh_toan) "
               "VALUES (?, ?, ?, ?, ?, ?, ?)")
        cursor.execute(sql, (
            data.get('id_thanh_toan'),
            data.get('id_don_hang'),
            data.get('id_khach_hang'),
            data.get('so_tien'),
            data.get('phuong_thuc', 'Chưa xác định'),
            data.get('trang_thai', 'Chưa thanh toán'),
            datetime.now()
        ))
        conn.commit()
        cursor.close()
        logger.info(f"Thêm thông tin thanh toán thành công: ID {data.get('id_thanh_toan')}")
        return jsonify({'message': 'Thêm thông tin thanh toán thành công'}), 201
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /thanhtoan POST - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi thêm thông tin thanh toán: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /thanhtoan POST - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/thanhtoan/<int:id_thanh_toan>', methods=['PUT'])
def update_thanhtoan(id_thanh_toan):
    try:
        data = request.get_json()
        if not any(key in data for key in ['phuong_thuc', 'trang_thai']):
            return jsonify({'error': 'Thiếu thông tin bắt buộc (phuong_thuc hoặc trang_thai)'}), 400

        cursor = conn.cursor()
        sql = "UPDATE ThanhToan SET phuong_thuc = ?, trang_thai = ? WHERE id_thanh_toan = ?"
        cursor.execute(sql, (
            data.get('phuong_thuc', ''),
            data.get('trang_thai', ''),
            id_thanh_toan
        ))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Thông tin thanh toán không tồn tại'}), 404
        conn.commit()
        cursor.close()
        logger.info(f"Cập nhật thông tin thanh toán thành công: ID {id_thanh_toan}")
        return jsonify({'message': 'Cập nhật thông tin thanh toán thành công'}), 200
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /thanhtoan PUT - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi cập nhật thông tin thanh toán: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /thanhtoan PUT - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/thanhtoan/<int:id_thanh_toan>', methods=['DELETE'])
def delete_thanhtoan(id_thanh_toan):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ThanhToan WHERE id_thanh_toan = ?", (id_thanh_toan,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Thông tin thanh toán không tồn tại'}), 404
        conn.commit()
        cursor.close()
        logger.info(f"Xóa thông tin thanh toán thành công: ID {id_thanh_toan}")
        return jsonify({'message': 'Xóa thông tin thanh toán thành công'}), 200
    except pyodbc.Error as e:
        logger.error(f"Lỗi API /thanhtoan DELETE - SQL Error: {str(e)}")
        conn.rollback()
        return jsonify({'error': 'Lỗi khi xóa thông tin thanh toán: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /thanhtoan DELETE - General Error: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

if __name__ == '__main__':
    # Chạy server Flask
    port = 5000
    url = f'http://127.0.0.1:{port}/Shopthoitrang/'  # Cập nhật URL để mở trang-chu.html
    app.run(debug=True, port=port)
    # Tự động mở trình duyệt sau khi server khởi động
    print(f"Mở trình duyệt tại: {url}")
    webbrowser.open(url)