async function dangNhap() {
    const tenDangNhap = document.getElementById('ten_dang_nhap').value;
    const matKhau = document.getElementById('mat_khau').value;

    if (!tenDangNhap || !matKhau) {
        document.getElementById('message').textContent = 'Vui lòng điền đầy đủ thông tin!';
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ten_dang_nhap: tenDangNhap, mat_khau: matKhau })
        });
        const data = await response.json();

        // Chỉ xử lý khi response.ok (mã 200)
        if (response.ok) {
            document.getElementById('message').textContent = data.message;
            if (data.id_khach_hang) {
                localStorage.setItem('id_khach_hang', data.id_khach_hang);
                localStorage.setItem('ten_khach_hang', data.ten_khach_hang);
                setTimeout(() => window.location.href = data.redirect, 1000);
            } else if (data.id_quan_tri) {
                localStorage.setItem('id_quan_tri', data.id_quan_tri);
                localStorage.setItem('tai_khoan', data.tai_khoan);
                setTimeout(() => window.location.href = data.redirect, 1000);
            }
        } else {
            document.getElementById('message').textContent = data.error;
            // Không chuyển hướng khi có lỗi (mã 401, 403, v.v.)
        }
    } catch (error) {
        console.error('Lỗi API dangNhap:', error);
        document.getElementById('message').textContent = 'Lỗi khi đăng nhập!';
    }
}