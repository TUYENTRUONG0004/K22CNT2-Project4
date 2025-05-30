// Shopthoitrang/js/api.js
const danhSachSanPhamTinh = [
    { id_san_pham: 1, ten_san_pham: 'Áo thun nữ trắng', gia: 199000, hinh_anh: '/images/quan-ao1.jpg', id_danh_muc: 1 },
    { id_san_pham: 5, ten_san_pham: 'Áo khoác nữ trắng', gia: 219000, hinh_anh: '/images/quan-ao2.jpg', id_danh_muc: 1 },
    { id_san_pham: 2, ten_san_pham: 'Quần jean xanh trời', gia: 399000, hinh_anh: '/images/quan-dai.jpg', id_danh_muc: 2 },
    { id_san_pham: 6, ten_san_pham: 'Quần jean đen bóng', gia: 350000, hinh_anh: '/images/quan-den-dai.jpg', id_danh_muc: 2 },
    { id_san_pham: 3, ten_san_pham: 'Giày thể thao trắng', gia: 499000, hinh_anh: '/images/giay-sneaker.jpg', id_danh_muc: 3 },
    { id_san_pham: 7, ten_san_pham: 'Giày sneaker đen', gia: 549000, hinh_anh: '/images/giay-den.jpg', id_danh_muc: 3 },
    { id_san_pham: 4, ten_san_pham: 'Túi đeo chéo nam', gia: 299000, hinh_anh: '/images/tui-deo-bung.jpg', id_danh_muc: 4 },
    { id_san_pham: 8, ten_san_pham: 'Mũ lưỡi trai basic', gia: 99000, hinh_anh: '/images/mu-den.jpg', id_danh_muc: 4 }
];

export async function getDanhSachSanPham() {
    try {
        const response = await fetch('http://127.0.0.1:5000/sanpham');
        if (!response.ok) throw new Error('Lỗi khi lấy danh sách sản phẩm');
        const data = await response.json();
        return data.length > 0 ? data : danhSachSanPhamTinh;
    } catch (error) {
        console.error('Lỗi API getDanhSachSanPham:', error);
        return danhSachSanPhamTinh;
    }
}

export async function getDanhSachDanhMuc() {
    try {
        const response = await fetch('http://127.0.0.1:5000/danhmuc');
        if (!response.ok) throw new Error('Lỗi khi lấy danh sách danh mục');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Lỗi API getDanhSachDanhMuc:', error);
        return [];
    }
}

export async function addToGioHang(idKhachHang, idSanPham, soLuong) {
    try {
        const response = await fetch('http://127.0.0.1:5000/giohang', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_khach_hang: idKhachHang,
                id_san_pham: idSanPham,
                so_luong: soLuong,
                ngay_them: new Date().toISOString()
            })
        });
        if (response.ok) {
            let gioHang = getGioHang();
            const item = gioHang.find(i => i.id_san_pham === idSanPham);
            if (item) {
                item.so_luong += soLuong;
            } else {
                gioHang.push({ id_khach_hang: idKhachHang, id_san_pham: idSanPham, so_luong: soLuong });
            }
            setGioHang(gioHang);
            return true;
        }
        throw new Error('Lỗi khi gọi API giỏ hàng');
    } catch (error) {
        console.error('Lỗi API addToGioHang:', error);
        let gioHang = getGioHang();
        const item = gioHang.find(i => i.id_san_pham === idSanPham);
        if (item) {
            item.so_luong += soLuong;
        } else {
            gioHang.push({ id_khach_hang: idKhachHang, id_san_pham: idSanPham, so_luong: soLuong });
        }
        setGioHang(gioHang);
        return true;
    }
}

export function getGioHang() {
    return JSON.parse(localStorage.getItem('gioHang') || '[]');
}

export function setGioHang(gio) {
    localStorage.setItem('gioHang', JSON.stringify(gio));
}

export function getLichSuDonHang() {
    return JSON.parse(localStorage.getItem('lichSuDonHang') || '[]');
}

export function addDonHang(don) {
    let lichSu = getLichSuDonHang();
    lichSu.unshift(don);
    localStorage.setItem('lichSuDonHang', JSON.stringify(lichSu));
}

export function dinhDangGia(gia) {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(gia);
}