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

function getGioHang() {
    return JSON.parse(localStorage.getItem('gioHang') || '[]');
}
function setGioHang(gio) {
    localStorage.setItem('gioHang', JSON.stringify(gio));
}
function dinhDangGia(gia) {
    return gia.toLocaleString('vi-VN') + '₫';
}

function hienThiSPDatHang() {
    const ds = getGioHang();
    const container = document.getElementById('sp-dat-hang');
    if (ds.length === 0) {
        container.innerHTML = `<div style="padding:32px;text-align:center;color:#d76d77;font-weight:bold;">Bạn chưa có sản phẩm nào!</div>`;
        document.getElementById('tong-tien').innerText = '';
        return;
    }
    let html = `<table>
        <tr>
            <th>Ảnh</th>
            <th>Tên sản phẩm</th>
            <th>Giá</th>
            <th>Số lượng</th>
            <th>Thành tiền</th>
        </tr>`;
    let tong = 0;
    ds.forEach(item => {
        const sp = dsSanPham.find(x => x.id_san_pham === item.id_san_pham);
        if (!sp) return;
        const thanhTien = sp.gia * item.so_luong;
        tong += thanhTien;
        html += `
        <tr>
            <td><img src="${sp.hinh_anh}" alt="${sp.ten_san_pham}"></td>
            <td>${sp.ten_san_pham}</td>
            <td>${dinhDangGia(sp.gia)}</td>
            <td>${item.so_luong}</td>
            <td>${dinhDangGia(thanhTien)}</td>
        </tr>`;
    });
    html += `</table>`;
    container.innerHTML = html;
    document.getElementById('tong-tien').innerText = 'Tổng tiền: ' + dinhDangGia(tong);
}

function showToast(msg) {
    const toast = document.getElementById('toast');
    toast.innerText = msg;
    toast.style.display = 'block';
    toast.style.opacity = '1';
    setTimeout(() => {
        toast.style.transition = 'opacity 0.4s';
        toast.style.opacity = '0';
    }, 1400);
    setTimeout(() => {
        toast.style.display = 'none';
        toast.style.transition = '';
    }, 1900);
}

function datHang(event) {
    event.preventDefault();
    const ten = document.getElementById('tenKhach').value.trim();
    const sdt = document.getElementById('sdtKhach').value.trim();
    const diaChi = document.getElementById('diaChiKhach').value.trim();
    if (!ten || !sdt || !diaChi) {
        showToast('Vui lòng nhập đủ thông tin!');
        return false;
    }
    const gio = getGioHang();
    if (!gio.length) {
        showToast('Bạn chưa có sản phẩm nào!');
        return false;
    }
    const dsSp = gio.map(item => ({
        id_san_pham: item.id_san_pham,
        so_luong: item.so_luong
    }));
    const tongTien = gio.reduce((sum, item) => {
        const sp = dsSanPham.find(x => x.id_san_pham === item.id_san_pham);
        return sum + (sp ? sp.gia * item.so_luong : 0);
    }, 0);
    const don = {
        id: Date.now(),
        ten,
        sdt,
        diaChi,
        ngay: new Date().toLocaleString('vi-VN'),
        dsSp,
        tongTien,
        trangThai: 'Chờ xác nhận'
    };
    let lichSu = JSON.parse(localStorage.getItem('lichSuDonHang') || '[]');
    lichSu.unshift(don);
    localStorage.setItem('lichSuDonHang', JSON.stringify(lichSu));
    setGioHang([]);
    showToast('Đặt hàng thành công!');
    setTimeout(() => {
        window.location.href = "lich-su-don-hang.html";
    }, 1700);
    return false;
}

window.onload = hienThiSPDatHang;
window.datHang = datHang;