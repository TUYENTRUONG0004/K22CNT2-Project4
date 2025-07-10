async function fetchFeaturedProducts() {
            try {
                const response = await fetch('http://127.0.0.1:5000/sanpham');
                if (!response.ok) throw new Error('Không thể lấy dữ liệu sản phẩm');
                const products = await response.json();
                const featuredProducts = document.getElementById('featuredProducts');
                if (!products.length) {
                    featuredProducts.innerHTML = '<p class="text-center col-span-3">Không có sản phẩm nào.</p>';
                    return;
                }
                featuredProducts.innerHTML = '';
                products.slice(0, 3).forEach(product => {
                    const card = `
                        <div class="bg-white shadow-md rounded-lg p-4">
                            <img src="${product.hinh_anh || '/images/default.jpg'}" alt="${product.ten_san_pham}" class="w-full h-48 object-cover mb-2 rounded" onerror="this.src='/images/default.jpg';">
                            <h3 class="text-lg font-semibold">${product.ten_san_pham}</h3>
                            <p class="text-gray-600">Giá: ${product.gia.toLocaleString('vi-VN')} VNĐ</p>
                            <button class="mt-2 bg-blue-500 text-white py-1 px-3 rounded hover:bg-blue-600" onclick="addToCart(${product.id_san_pham}, 1)">Thêm vào giỏ</button>
                        </div>
                    `;
                    featuredProducts.innerHTML += card;
                });
            } catch (error) {
                console.error('Lỗi khi lấy sản phẩm:', error);
                document.getElementById('featuredProducts').innerHTML = '<p class="text-center col-span-3 text-red-500">Lỗi khi tải sản phẩm.</p>';
            }
        }

        async function fetchCategories() {
            try {
                const response = await fetch('http://127.0.0.1:5000/danhmuc');
                if (!response.ok) throw new Error('Không thể lấy dữ liệu danh mục');
                const categories = await response.json();
                const categoriesDiv = document.getElementById('categories');
                if (!categories.length) {
                    categoriesDiv.innerHTML = '<p class="text-center col-span-3">Không có danh mục nào.</p>';
                    return;
                }
                categoriesDiv.innerHTML = '';
                categories.forEach(cat => {
                    const card = `
                        <div class="bg-white shadow-md rounded-lg p-4 text-center">
                            <h3 class="text-lg font-semibold">${cat.ten_danh_muc}</h3>
                            <a href="products.html?category=${cat.id_danh_muc}" class="mt-2 inline-block bg-blue-500 text-white py-1 px-3 rounded hover:bg-blue-600">Xem chi tiết</a>
                        </div>
                    `;
                    categoriesDiv.innerHTML += card;
                });
            } catch (error) {
                console.error('Lỗi khi lấy danh mục:', error);
                document.getElementById('categories').innerHTML = '<p class="text-center col-span-3 text-red-500">Lỗi khi tải danh mục.</p>';
            }
        }

        async function addToCart(productId, quantity) {
            const idKhachHang = localStorage.getItem('id_khach_hang');
            if (!idKhachHang) {
                alert('Vui lòng đăng nhập để thêm vào giỏ hàng!');
                window.location.href = '/Shopthoitrang/dang-nhap.html';
                return;
            }

            const cartItem = {
                id_gio_hang: Date.now(),
                id_khach_hang: idKhachHang,
                id_san_pham: productId,
                so_luong: quantity,
                ngay_them: new Date().toISOString().split('T')[0]
            };

            try {
                const response = await fetch('http://127.0.0.1:5000/giohang', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(cartItem)
                });
                const result = await response.json();
                alert(result.message || 'Thêm vào giỏ hàng');
            } catch (error) {
                console.error('Lỗi:', error);
                alert('Có lỗi xảy ra khi thêm vào giỏ hàng');
            }
        }

        // Xử lý đăng xuất
        document.addEventListener('DOMContentLoaded', () => {
            const idKhachHang = localStorage.getItem('id_khach_hang');
            const userActions = document.getElementById('userActions');
            const logoutBtn = document.getElementById('logoutBtn');

            if (idKhachHang) {
                // Nếu đã đăng nhập, ẩn đăng nhập/đăng ký, hiển thị đăng xuất
                userActions.querySelectorAll('a').forEach(link => {
                    if (link.href.includes('dang-nhap') || link.href.includes('dang-ky')) {
                        link.style.display = 'none';
                    }
                });
                logoutBtn.classList.remove('hidden');
            }

            logoutBtn.addEventListener('click', async () => {
                if (idKhachHang) {
                    if (confirm('Bạn có chắc muốn đăng xuất? Giỏ hàng sẽ bị xóa!')) {
                        try {
                            // Xóa tất cả sản phẩm trong giỏ hàng
                            await fetch(`http://127.0.0.1:5000/giohang?id_khach_hang=${idKhachHang}`, {
                                method: 'DELETE',
                                headers: { 'Content-Type': 'application/json' }
                            });
                            // Xóa id_khach_hang khỏi localStorage
                            localStorage.removeItem('id_khach_hang');
                            alert('Đăng xuất thành công! Giỏ hàng đã bị xóa.');
                            // Tải lại trang chủ
                            window.location.href = '/Shopthoitrang/trang-chu.html';
                        } catch (error) {
                            console.error('Lỗi khi xóa giỏ hàng:', error);
                            alert('Lỗi khi đăng xuất!');
                        }
                    }
                } else {
                    alert('Bạn chưa đăng nhập!');
                }
            });

            Promise.all([fetchFeaturedProducts(), fetchCategories()]);
        });