// Danh sách sản phẩm giống trang chủ
const dsSanPham = [
    // Áo thun
    {
        id_san_pham: 1,
        ten_san_pham: 'Áo thun nữ trắng',
        gia: 199000,
        hinh_anh: 'images/quan-ao1.jpg',
    },
    {
        id_san_pham: 5,
        ten_san_pham: 'Áo khoác nữ trắng',
        gia: 219000,
        hinh_anh: 'images/quan-ao2.jpg',
    },
    // Quần jean
    {
        id_san_pham: 2,
        ten_san_pham: 'Quần jean xanh trời',
        gia: 399000,
        hinh_anh: 'images/quan-dai.jpg',
    },
    {
        id_san_pham: 6,
        ten_san_pham: 'Quần jean đen bóng',
        gia: 350000,
        hinh_anh: 'images/quan-den-dai.jpg',
    },
    // Giày sneaker
    {
        id_san_pham: 3,
        ten_san_pham: 'Giày thể thao trắng',
        gia: 499000,
        hinh_anh: 'images/giay-sneaker.jpg',
    },
    {
        id_san_pham: 7,
        ten_san_pham: 'Giày sneaker đen',
        gia: 549000,
        hinh_anh: 'images/giay-den.jpg',
    },
    // Phụ kiện
    {
        id_san_pham: 4,
        ten_san_pham: 'Túi đeo chéo nam',
        gia: 299000,
        hinh_anh: 'images/tui-deo-bung.jpg',
    },
    {
        id_san_pham: 8,
        ten_san_pham: 'Mũ lưỡi trai basic',
        gia: 99000,
        hinh_anh: 'images/mu-den.jpg',
    }
];

// Hàm lấy giỏ hàng từ localStorage
function getGioHang() {
    return JSON.parse(localStorage.getItem('gioHang') || '[]');
}

// Hàm lưu giỏ hàng vào localStorage
function setGioHang(gio) {
    localStorage.setItem('gioHang', JSON.stringify(gio));
}

// Định dạng giá
function dinhDangGia(gia) {
    return gia.toLocaleString('vi-VN') + '₫';
}

// Hiển thị giỏ hàng
function hienThiGioHang() {
    const ds = getGioHang();
    const container = document.getElementById('danh-sach-gio-hang');
    if (ds.length === 0) {
        container.innerHTML = `<div style="padding:32px;text-align:center;color:#d76d77;font-weight:bold;">Giỏ hàng của bạn đang trống!</div>`;
        document.getElementById('tong-tien').innerText = '';
        return;
    }
    let html = `<table class="gio-hang-table">
        <tr>
            <th>Ảnh</th>
            <th>Tên sản phẩm</th>
            <th>Giá</th>
            <th>Số lượng</th>
            <th>Thành tiền</th>
            <th>Xoá</th>
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
            <td>
                <input type="number" min="1" value="${item.so_luong}" onchange="capNhatSoLuong(${sp.id_san_pham}, this.value)">
            </td>
            <td>${dinhDangGia(thanhTien)}</td>
            <td><button class="xoa-btn" onclick="xoaSanPham(${sp.id_san_pham})">Xoá</button></td>
        </tr>`;
    });
    html += `</table>`;
    container.innerHTML = html;
    document.getElementById('tong-tien').innerText = 'Tổng tiền: ' + dinhDangGia(tong);
}

// Xoá sản phẩm khỏi giỏ
function xoaSanPham(id) {
    let ds = getGioHang();
    ds = ds.filter(item => item.id_san_pham !== id);
    setGioHang(ds);
    hienThiGioHang();
    showToast('Đã xoá sản phẩm khỏi giỏ');
}

// Cập nhật số lượng
function capNhatSoLuong(id, sl) {
    let ds = getGioHang();
    ds = ds.map(item => {
        if (item.id_san_pham === id) {
            item.so_luong = Math.max(1, parseInt(sl));
        }
        return item;
    });
    setGioHang(ds);
    hienThiGioHang();
    showToast('Đã cập nhật số lượng');
}

// Đặt hàng (demo)
function datHang() {
    let ds = getGioHang();
    if (ds.length === 0) {
        showToast('Bạn chưa có sản phẩm nào trong giỏ!');
        return;
    }
    // Xoá giỏ hàng sau khi đặt hàng thành công (demo)
    localStorage.removeItem('gioHang');
    hienThiGioHang();
    showToast('Đặt hàng thành công! (demo)');
}

// Toast nhỏ góc phải
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

// Bổ sung: Khi thêm vào giỏ từ trang chủ hoặc chi tiết sản phẩm,
// hãy dùng hàm này (dán vào file js trang-chu.js và chi-tiet-san-pham.js)
window.themVaoGio = function(idSanPham) {
    let ds = getGioHang();
    let sp = ds.find(x => x.id_san_pham === idSanPham);
    if (sp) {
        sp.so_luong += 1;
    } else {
        ds.push({ id_san_pham: idSanPham, so_luong: 1 });
    }
    setGioHang(ds);
    showToast('Đã thêm sản phẩm vào giỏ!');
}

window.xoaSanPham = xoaSanPham;
window.capNhatSoLuong = capNhatSoLuong;
window.datHang = datHang;

window.onload = hienThiGioHang;