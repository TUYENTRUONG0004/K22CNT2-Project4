from flask import Flask, request, jsonify, send_from_directory
import pyodbc
import os
from flask_cors import CORS
import logging
from datetime import datetime
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

@app.route('/Shopthoitrang/<path:path>')
def serve_shopthoitrang(path):
    return send_from_directory('Shopthoitrang', path)

@app.route('/admin/<path:path>')
def serve_admin(path):
    return send_from_directory('.', path)

# Route để phục vụ CSS, JS, images từ Shopthoitrang
@app.route('/Shopthoitrang/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join('Shopthoitrang', 'css'), filename)

@app.route('/Shopthoitrang/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join('Shopthoitrang', 'images'), filename)

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
                data['hinh_anh'] = f'/Shopthoitrang/images/{file.filename}'
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
                data['hinh_anh'] = f'/Shopthoitrang/images/{file.filename}'
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

@app.route('/sanpham/<int:id_san_pham>', methods=['GET'])
def get_sanpham_by_id(id_san_pham):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SanPham WHERE id_san_pham = ?", (id_san_pham,))
        cols = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return jsonify({'error': 'Sản phẩm không tồn tại'}), 404
        product = dict(zip(cols, row))
        return jsonify(product)
    except Exception as e:
        logger.error(f"Lỗi API /sanpham/<id_san_pham> GET: {str(e)}")
        return jsonify({'error': str(e)}), 500

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
    finally:
        if 'cursor' in locals():
            cursor.close()

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
def get_don_hang_by_id(id_don_hang):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DonHang WHERE id_don_hang = ?", (id_don_hang,))
    row = cursor.fetchone()
    if row:
        keys = [column[0] for column in cursor.description]
        return jsonify(dict(zip(keys, row)))
    return jsonify({'error': 'Không tìm thấy đơn hàng'}), 404

@app.route('/donhang', methods=['POST'])
def create_don_hang():
    cursor = None
    try:
        data = request.get_json()
        logger.info(f"Dữ liệu nhận từ client: {data}")

        # Kiểm tra dữ liệu đầu vào
        required_fields = ['id_khach_hang', 'tong_tien']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Thiếu thông tin yêu cầu (id_khach_hang, tong_tien)'}), 400

        try:
            id_khach_hang = int(data['id_khach_hang'])
            tong_tien = float(data['tong_tien'])
        except (ValueError, TypeError):
            return jsonify({'error': 'id_khach_hang và tong_tien phải là số'}), 400

        trang_thai = data.get('trang_thai', 'Chờ xử lý')
        ngay_dat = data.get('ngay_dat', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # Kiểm tra khách hàng tồn tại
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM KhachHang WHERE id_khach_hang = ?", (id_khach_hang,))
        if cursor.fetchone()[0] == 0:
            return jsonify({'error': 'Khách hàng không tồn tại'}), 404

        # Thêm đơn hàng vào cơ sở dữ liệu
        cursor.execute(
            "INSERT INTO DonHang (ngay_dat, id_khach_hang, tong_tien, trang_thai) VALUES (?, ?, ?, ?)",
            (ngay_dat, id_khach_hang, tong_tien, trang_thai)
        )
        conn.commit()

        # Lấy ID của đơn hàng vừa tạo
        cursor.execute("SELECT SCOPE_IDENTITY()")
        id_don_hang = cursor.fetchone()[0]

        logger.info(f"Tạo đơn hàng thành công, ID: {id_don_hang}")
        return jsonify({'message': 'Đơn hàng đã được tạo', 'id_don_hang': id_don_hang}), 201

    except pyodbc.Error as e:
        logger.error(f"Lỗi SQL khi tạo đơn hàng: {str(e)}")
        conn.rollback()
        return jsonify({'error': f'Lỗi khi tạo đơn hàng: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"Lỗi không xác định khi tạo đơn hàng: {str(e)}")
        return jsonify({'error': f'Lỗi không xác định: {str(e)}'}), 500
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
        cursor = conn.cursor()
        search_term = request.args.get('search', '').strip()
        query = "SELECT * FROM KhachHang"
        params = ()
        if search_term:
            query += " WHERE ten_khach_hang LIKE ? OR email LIKE ?"
            params = ('%' + search_term + '%', '%' + search_term + '%')
        cursor.execute(query, params)
        cols = [desc[0] for desc in cursor.description]
        customers = [dict(zip(cols, row)) for row in cursor.fetchall()]
        cursor.close()
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

        required_fields = ['ten_khach_hang', 'so_dien_thoai', 'email']
        if not all(key in data for key in required_fields):
            return jsonify({'error': 'Thiếu thông tin bắt buộc'}), 400

        cursor = conn.cursor()

        # Kiểm tra trùng email hoặc sdt
        cursor.execute("SELECT 1 FROM KhachHang WHERE so_dien_thoai = ? OR email = ?", (data['so_dien_thoai'], data['email']))
        if cursor.fetchone():
            return jsonify({'error': 'Số điện thoại hoặc email đã tồn tại'}), 400

        cursor.execute("""
            INSERT INTO KhachHang (ten_khach_hang, so_dien_thoai, email, dia_chi, ngay_tao)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data['ten_khach_hang'],
            data['so_dien_thoai'],
            data['email'],
            data.get('dia_chi', ''),
            datetime.now()
        ))
        conn.commit()

        cursor.execute("SELECT SCOPE_IDENTITY()")
        new_id = cursor.fetchone()[0]
        cursor.close()

        return jsonify({
            'message': 'Thêm khách hàng thành công',
            'id_khach_hang': new_id
        }), 201

    except Exception as e:
        logger.error(f"Lỗi khi thêm khách hàng: {e}")
        return jsonify({'error': 'Lỗi server'}), 500


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

# API: Đăng nhập
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ['ten_dang_nhap', 'mat_khau']):
            logger.warning("Yêu cầu đăng nhập thiếu thông tin bắt buộc")
            return jsonify({'error': 'Thiếu thông tin bắt buộc (ten_dang_nhap, mat_khau)'}), 400

        ten_dang_nhap = data['ten_dang_nhap'].strip()
        mat_khau = data['mat_khau'].strip()

        # Kiểm tra đăng nhập khách hàng (dựa trên email và so_dien_thoai)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM KhachHang WHERE email = ? AND so_dien_thoai = ?",
                       (ten_dang_nhap, mat_khau))
        row = cursor.fetchone()

        if row:
            customer = dict(zip([desc[0] for desc in cursor.description], row))
            logger.info(f"Đăng nhập khách hàng thành công: Email {ten_dang_nhap}, ID {customer['id_khach_hang']}")
            return jsonify({
                'message': 'Đăng nhập khách hàng thành công',
                'id_khach_hang': customer['id_khach_hang'],
                'ten_khach_hang': customer['ten_khach_hang'],
                'redirect': '/Shopthoitrang/trang-chu.html'
            }), 200

        # Nếu không phải khách hàng, kiểm tra đăng nhập quản trị
        cursor.execute("SELECT * FROM QuanTri WHERE Tai_khoan = ? AND Mat_khau = ?",
                       (ten_dang_nhap, mat_khau))
        row = cursor.fetchone()

        if row:
            admin = dict(zip([desc[0] for desc in cursor.description], row))
            if admin['Trang_thai'] != 'Hoạt động':
                logger.warning(f"Tài khoản bị khóa: {ten_dang_nhap}")
                return jsonify({'error': 'Tài khoản bị khóa, vui lòng liên hệ quản trị viên'}), 403

            logger.info(f"Đăng nhập quản trị thành công: Tài khoản {ten_dang_nhap}, ID {admin['id_quan_tri']}")
            return jsonify({
                'message': 'Đăng nhập quản trị thành công',
                'id_quan_tri': admin['id_quan_tri'],
                'tai_khoan': admin['Tai_khoan'],
                'redirect': '/Shopthoitrang/admin.html'
            }), 200
        else:
            logger.warning(f"Đăng nhập thất bại: {ten_dang_nhap} hoặc mật khẩu không đúng")
            return jsonify({'error': 'Tên đăng nhập hoặc mật khẩu không đúng'}), 401

    except pyodbc.Error as e:
        logger.error(f"Lỗi API /login POST - SQL Error: {str(e)} - Chi tiết: {e.args}")
        return jsonify({'error': 'Lỗi kết nối cơ sở dữ liệu: ' + str(e)}), 500
    except Exception as e:
        logger.error(f"Lỗi API /login POST - Lỗi không xác định: {str(e)}")
        return jsonify({'error': 'Lỗi không xác định: ' + str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

if __name__ == '__main__':
    # Chạy server Flask
    port = 5000
    url = f'http://127.0.0.1:{port}/Shopthoitrang/trang-chu.html'  # Cập nhật URL để mở trang-chu.html
    app.run(debug=True, port=port)