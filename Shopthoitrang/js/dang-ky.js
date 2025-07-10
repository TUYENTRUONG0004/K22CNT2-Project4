async function dangKy() {
            const ten = document.getElementById('register-ten').value.trim();
            const soDienThoai = document.getElementById('register-so-dien-thoai').value.trim();
            const email = document.getElementById('register-email').value.trim();
            const diaChi = document.getElementById('register-dia_chi').value.trim();
            const messageDiv = document.getElementById('message');

            if (!ten || !soDienThoai || !email) {
                messageDiv.textContent = 'Vui lòng điền đủ thông tin bắt buộc!';
                return;
            }

            if (!/^[0-9]{10}$/.test(soDienThoai)) {
                messageDiv.textContent = 'Số điện thoại phải là 10 chữ số!';
                return;
            }

            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                messageDiv.textContent = 'Email không hợp lệ!';
                return;
            }

            if (!/^[a-zA-ZÀ-ỹ\s]+$/.test(ten)) {
                messageDiv.textContent = 'Tên chỉ được chứa chữ cái và khoảng trắng!';
                return;
            }

            const khachHang = {
                ten_khach_hang: ten,
                so_dien_thoai: soDienThoai,
                email: email,
                dia_chi: diaChi
            };

            try {
                const response = await fetch('http://127.0.0.1:5000/khachhang', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(khachHang)
                });

                const data = await response.json();

                if (response.ok) {
                    messageDiv.textContent = data.message;
                    messageDiv.className = 'success';

                    localStorage.setItem('id_khach_hang', data.id_khach_hang);

                    document.getElementById('register-ten').value = '';
                    document.getElementById('register-so-dien-thoai').value = '';
                    document.getElementById('register-email').value = '';
                    document.getElementById('register-dia_chi').value = '';

                    setTimeout(() => {
                        window.location.href = '/Shopthoitrang/trang-chu.html';
                    }, 2000);
                } else {
                    messageDiv.textContent = data.error || 'Lỗi không xác định từ server.';
                }
            } catch (error) {
                console.error('Lỗi API dangKy:', error);
                messageDiv.textContent = 'Lỗi khi kết nối đến server. Vui lòng thử lại!';
            }
        }

        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    dangKy();
                }
            });
        });