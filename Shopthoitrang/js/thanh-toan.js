async function loadCheckout() {
            const urlParams = new URLSearchParams(window.location.search);
            const idKhachHang = urlParams.get('id_khach_hang') || localStorage.getItem('id_khach_hang');
            
            if (!idKhachHang) {
                document.getElementById('message').textContent = 'Vui lòng đăng nhập để thanh toán!';
                document.getElementById('confirmOrderBtn').style.display = 'none';
                return;
            }

            try {
                const cartResponse = await fetch(`http://127.0.0.1:5000/giohang?id_khach_hang=${idKhachHang}`);
                const cartItems = await cartResponse.json();

                const cartTable = document.getElementById('cartItems');
                cartTable.innerHTML = '';

                if (cartItems.length === 0) {
                    cartTable.innerHTML = '<tr><td colspan="4">Giỏ hàng trống</td></tr>';
                    document.getElementById('confirmOrderBtn').style.display = 'none';
                    return;
                }

                let total = 0;
                for (const item of cartItems) {
                    const productResponse = await fetch(`http://127.0.0.1:5000/sanpham/${item.id_san_pham}`);
                    const product = await productResponse.json();
                    const row = document.createElement('tr');
                    const totalPrice = item.so_luong * (product.gia || 0);
                    row.innerHTML = `
                        <td>${product.ten_san_pham || item.id_san_pham}</td>
                        <td>${item.so_luong}</td>
                        <td>${(product.gia || 0).toLocaleString('vi-VN')} VNĐ</td>
                        <td>${totalPrice.toLocaleString('vi-VN')} VNĐ</td>
                    `;
                    cartTable.appendChild(row);
                    total += totalPrice;
                }

                document.getElementById('totalPrice').textContent = `Tổng cộng: ${total.toLocaleString('vi-VN')} VNĐ`;
                localStorage.setItem('tong_tien', total);

            } catch (error) {
                console.error('Lỗi khi tải thông tin thanh toán:', error);
                document.getElementById('message').textContent = 'Lỗi khi tải thông tin thanh toán!';
            }
        }

        document.getElementById('confirmOrderBtn').addEventListener('click', async () => {
            const idKhachHang = localStorage.getItem('id_khach_hang');
            const tongTien = localStorage.getItem('tong_tien');

            if (!idKhachHang || !tongTien) {
                alert('Thông tin không hợp lệ, vui lòng thử lại!');
                return;
            }

            try {
                const orderData = {
                    id_khach_hang: parseInt(idKhachHang),
                    tong_tien: parseFloat(tongTien),
                    trang_thai: 'Chờ xử lý',
                    ngay_dat: new Date().toISOString()
                };

                const response = await fetch('http://127.0.0.1:5000/donhang', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(orderData)
                });

                const result = await response.json();
                if (response.ok) {
    alert('Đặt hàng thành công! Đơn hàng của bạn đang được xử lý.');
                    try {
                        const deleteResponse = await fetch(`http://127.0.0.1:5000/giohang/${idKhachHang}`, {
                            method: 'DELETE',
                            headers: { 'Content-Type': 'application/json' }
                        });
                        if (!deleteResponse.ok) {
                            console.warn('Xóa giỏ hàng thất bại, nhưng vẫn chuyển hướng:', await deleteResponse.json());
                        }
                    } catch (deleteError) {
                        console.warn('Lỗi khi xóa giỏ hàng:', deleteError);
                    }
                    console.log('Chuyển hướng đến:', '/Shopthoitrang/cam-on.html');
                    localStorage.removeItem('tong_tien');
                    window.location.href = '/Shopthoitrang/cam-on.html';
                } else {
                    alert(result.error || 'Lỗi khi đặt hàng!');
                }
            } catch (error) {
                console.error('Lỗi khi đặt hàng:', error);
                alert('Lỗi khi đặt hàng! Vui lòng thử lại.');
            }
        });

        window.onload = loadCheckout;