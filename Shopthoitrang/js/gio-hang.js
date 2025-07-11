async function loadCart() {
            const idKhachHang = localStorage.getItem('id_khach_hang');
            if (!idKhachHang) {
                document.getElementById('message').textContent = 'Vui lòng đăng nhập để xem giỏ hàng!';
                document.getElementById('checkoutBtn').style.display = 'none';
                return;
            }

            try {
                const response = await fetch(`http://127.0.0.1:5000/giohang?id_khach_hang=${idKhachHang}`, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' }
                });
                const cartItems = await response.json();

                const cartTable = document.getElementById('cartItems');
                cartTable.innerHTML = ''; // Xóa nội dung cũ

                if (cartItems.length === 0) {
                    cartTable.innerHTML = '<tr><td colspan="5">Giỏ hàng trống</td></tr>';
                    document.getElementById('checkoutBtn').style.display = 'none';
                    return;
                }

                // Lấy thông tin sản phẩm từ API /sanpham để hiển thị tên và giá
                let total = 0;
                for (const item of cartItems) {
                    const productResponse = await fetch(`http://127.0.0.1:5000/sanpham/${item.id_san_pham}`, {
                        method: 'GET',
                        headers: { 'Content-Type': 'application/json' }
                    });
                    const product = await productResponse.json();
                    const row = document.createElement('tr');
                    const totalPrice = item.so_luong * (product.gia || 0);
                    row.innerHTML = `
                        <td>${product.ten_san_pham || item.id_san_pham}</td>
                        <td>${item.so_luong}</td>
                        <td>${(product.gia || 0).toLocaleString('vi-VN')} VNĐ</td>
                        <td>${totalPrice.toLocaleString('vi-VN')} VNĐ</td>
                        <td><button onclick="removeFromCart(${item.id_khach_hang}, ${item.id_san_pham})">Xóa</button></td>
                    `;
                    cartTable.appendChild(row);
                    total += totalPrice;
                }

                document.getElementById('totalPrice').textContent = `Tổng cộng: ${total.toLocaleString('vi-VN')} VNĐ`;
                document.getElementById('checkoutBtn').style.display = 'inline-block';
            } catch (error) {
                console.error('Lỗi khi tải giỏ hàng:', error);
                document.getElementById('message').textContent = 'Lỗi khi tải giỏ hàng!';
            }
        }

        async function removeFromCart(idKhachHang, idSanPham) {
            if (!confirm('Bạn có chắc muốn xóa sản phẩm này?')) return;

            try {
                const response = await fetch(`http://127.0.0.1:5000/giohang/${idKhachHang}/${idSanPham}`, {
                    method: 'DELETE',
                    headers: { 'Content-Type': 'application/json' }
                });
                const data = await response.json();
                if (response.ok) {
                    alert(data.message);
                    loadCart(); // Tải lại giỏ hàng
                } else {
                    alert(data.error);
                }
            } catch (error) {
                console.error('Lỗi khi xóa sản phẩm:', error);
                alert('xóa sản phẩm!Click "ok" reload');
            }
        }

        // Thêm sự kiện cho nút Đặt hàng
        document.getElementById('checkoutBtn').addEventListener('click', () => {
            const idKhachHang = localStorage.getItem('id_khach_hang');
            if (idKhachHang) {
                window.location.href = `/Shopthoitrang/thanh-toan.html?id_khach_hang=${idKhachHang}`;
            } else {
                alert('Vui lòng đăng nhập để đặt hàng!');
            }
        });

        // Tải giỏ hàng khi trang tải
        window.onload = loadCart;