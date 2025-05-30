const dsSanPham = [
    { id_san_pham: 1, ten_san_pham: 'Áo thun nữ trắng', gia: 199000, hinh_anh: 'images/quan-ao1.jpg' },
    { id_san_pham: 5, ten_san_pham: 'Áo khoác nữ trắng', gia: 219000, hinh_anh: 'images/quan-ao2.jpg' },
    { id_san_pham: 2, ten_san_pham: 'Quần jean xanh trời', gia: 399000, hinh_anh: 'images/quan-dai.jpg' },
    { id_san_pham: 6, ten_san_pham: 'Quần jean đen bóng', gia: 350000, hinh_anh: 'images/quan-den-dai.jpg' },
    { id_san_pham: 3, ten_san_pham: 'Giày thể thao trắng', gia: 499000, hinh_anh: 'images/giay-sneaker.jpg' },
    { id_san_pham: 7, ten_san_pham: 'Giày sneaker đen', gia: 549000, hinh_anh: 'images/giay-den.jpg' },
    { id_san_pham: 4, ten_san_pham: 'Túi đeo chéo nam', gia: 299000, hinh_anh: 'images/tui-deo-bung.jpg' },
    { id_san_pham: 8, ten_san_pham: 'Mũ lưỡi trai basic', gia: 99000, hinh_anh: 'images/mu-den.jpg' }
];

function dinhDangGia(gia) { return gia.toLocaleString('vi-VN') + '₫'; }

function hienThiLichSu() {
    let ds = JSON.parse(localStorage.getItem('lichSuDonHang') || '[]');
    const container = document.getElementById('lich-su-don-hang');
    if (!ds.length) {
        container.innerHTML = `<div style="padding:32px;text-align:center;color:#d76d77;font-weight:bold;">Bạn chưa có đơn hàng nào!</div>`;
        return;
    }
    let html = '';
    ds.forEach(don => {
        html += `<div class="don-hang">
            <div class="tt"><b>Mã đơn:</b> #${don.id} | <b>Ngày đặt:</b> ${don.ngay}</div>
            <div class="tt"><b>Khách hàng:</b> ${don.ten} | <b>SĐT:</b> ${don.sdt}</div>
            <div class="tt"><b>Địa chỉ:</b> ${don.diaChi}</div>
            <div class="tt"><span class="trang-thai">${don.trangThai}</span></div>
            <div class="sp-list">
                <table>
                    <tr>
                        <th>Ảnh</th>
                        <th>Tên sản phẩm</th>
                        <th>Giá</th>
                        <th>Số lượng</th>
                        <th>Thành tiền</th>
                    </tr>`;
        (don.dsSp || []).forEach(item => {
            const sp = dsSanPham.find(x => x.id_san_pham === item.id_san_pham) || {};
            html += `
                    <tr>
                        <td><img src="${sp.hinh_anh || ''}" alt="${sp.ten_san_pham || ''}"></td>
                        <td>${sp.ten_san_pham || ''}</td>
                        <td>${sp.gia ? dinhDangGia(sp.gia) : ''}</td>
                        <td>${item.so_luong}</td>
                        <td>${sp.gia ? dinhDangGia(sp.gia * item.so_luong) : ''}</td>
                    </tr>`;
        });
        html += `</table>
            </div>
            <div class="tong">Tổng tiền: ${dinhDangGia(don.tongTien)}</div>
        </div>`;
    });
    container.innerHTML = html;
}

window.onload = hienThiLichSu;