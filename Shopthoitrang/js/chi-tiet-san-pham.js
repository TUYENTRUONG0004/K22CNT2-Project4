// Cùng dữ liệu sản phẩm như trang chủ, bạn có thể import chung hoặc copy sang
const dsSanPham = [
    // Áo thun
    {
        id_san_pham: 1,
        ten_san_pham: 'Áo thun nữ trắng',
        gia: 199000,
        hinh_anh: 'images/quan-ao1.jpg',
        mo_ta: 'Áo thun nữ trắng chất liệu cotton co giãn, thoáng mát, phù hợp mọi hoạt động thường ngày.',
        id_danh_muc: 1
    },
    {
        id_san_pham: 5,
        ten_san_pham: 'Áo khoác nữ trắng',
        gia: 219000,
        hinh_anh: 'images/quan-ao2.jpg',
        mo_ta: 'Áo khoác nữ trắng thiết kế trẻ trung, nhẹ nhàng, dễ phối đồ.',
        id_danh_muc: 1
    },
    // Quần jean
    {
        id_san_pham: 2,
        ten_san_pham: 'Quần jean xanh trời',
        gia: 399000,
        hinh_anh: 'images/quan-dai.jpg',
        mo_ta: 'Quần jean xanh trời kiểu dáng hiện đại, chất vải dày dặn, bền đẹp.',
        id_danh_muc: 2
    },
    {
        id_san_pham: 6,
        ten_san_pham: 'Quần jean đen bóng',
        gia: 350000,
        hinh_anh: 'images/quan-den-dai.jpg',
        mo_ta: 'Quần jean đen bóng dành cho nam/nữ, hợp xu hướng, dễ phối đồ.',
        id_danh_muc: 2
    },
    // Giày sneaker
    {
        id_san_pham: 3,
        ten_san_pham: 'Giày thể thao trắng',
        gia: 499000,
        hinh_anh: 'images/giay-sneaker.jpg',
        mo_ta: 'Giày thể thao màu trắng, phong cách basic, đế cao su bám tốt.',
        id_danh_muc: 3
    },
    {
        id_san_pham: 7,
        ten_san_pham: 'Giày sneaker đen',
        gia: 549000,
        hinh_anh: 'images/giay-den.jpg',
        mo_ta: 'Giày sneaker màu đen mạnh mẽ, phù hợp nhiều hoạt động thể thao.',
        id_danh_muc: 3
    },
    // Phụ kiện
    {
        id_san_pham: 4,
        ten_san_pham: 'Túi đeo chéo nam',
        gia: 299000,
        hinh_anh: 'images/tui-deo-bung.jpg',
        mo_ta: 'Túi đeo chéo nam thiết kế nhỏ gọn, tiện dụng, phù hợp đi chơi, đi học.',
        id_danh_muc: 4
    },
    {
        id_san_pham: 8,
        ten_san_pham: 'Mũ lưỡi trai basic',
        gia: 99000,
        hinh_anh: 'images/mu-den.jpg',
        mo_ta: 'Mũ lưỡi trai basic màu đen, thích hợp đi chơi, dã ngoại, thể thao.',
        id_danh_muc: 4
    }
];

// Hàm lấy id sản phẩm từ URL (vd: chi-tiet-san-pham.html?id=1)
function getIdSanPham() {
    const params = new URLSearchParams(window.location.search);
    return parseInt(params.get('id'), 10);
}

function dinhDangGia(gia) {
    return gia.toLocaleString('vi-VN') + '₫';
}

function hienThiChiTietSanPham() {
    const id = getIdSanPham();
    const sp = dsSanPham.find(x => x.id_san_pham === id);
    const container = document.getElementById('chi-tiet-san-pham');
    if (!sp) {
        container.innerHTML = `<div style="padding:32px;text-align:center;color:#d76d77;font-weight:bold;">Không tìm thấy sản phẩm!</div>`;
        return;
    }
    container.innerHTML = `
        <div class="ctsp-anh">
            <img src="${sp.hinh_anh}" alt="${sp.ten_san_pham}">
        </div>
        <div class="ctsp-thong-tin">
            <h2>${sp.ten_san_pham}</h2>
            <div class="ctsp-gia">${dinhDangGia(sp.gia)}</div>
            <div class="ctsp-mo-ta">${sp.mo_ta || "Chưa có mô tả chi tiết cho sản phẩm này."}</div>
            <div class="ctsp-btn">
                <button onclick="themVaoGio(${sp.id_san_pham})">Thêm vào giỏ</button>
                <button onclick="window.history.back()">Quay lại</button>
            </div>
        </div>
    `;
}

// Toast hiệu ứng (thông báo nhỏ góc phải)
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

function themVaoGio(idSanPham) {
    showToast('Đã thêm sản phẩm vào giỏ!');
}
function themVaoGio(idSanPham) {
    // Lấy giỏ hàng từ localStorage (nếu chưa có thì là mảng rỗng)
    let gio = JSON.parse(localStorage.getItem('gioHang') || '[]');
    let daCo = gio.find(item => item.id_san_pham === idSanPham);
    if (daCo) {
        daCo.so_luong += 1;
    } else {
        gio.push({ id_san_pham: idSanPham, so_luong: 1 });
    }
    localStorage.setItem('gioHang', JSON.stringify(gio));
    showToast('Đã thêm sản phẩm vào giỏ!');
}

window.onload = hienThiChiTietSanPham;