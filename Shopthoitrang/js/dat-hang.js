let products = [];

        async function fetchProducts() {
            try {
                const response = await fetch('http://127.0.0.1:5000/sanpham');
                if (!response.ok) throw new Error('Không thể lấy dữ liệu sản phẩm');
                products = await response.json();
                const categoriesResponse = await fetch('http://127.0.0.1:5000/danhmuc');
                if (!categoriesResponse.ok) throw new Error('Không thể lấy dữ liệu danh mục');
                const categories = await categoriesResponse.json();
                const categorySelect = document.getElementById('categoryFilter');
                categories.forEach(cat => {
                    const option = document.createElement('option');
                    option.value = cat.id_danh_muc;
                    option.textContent = cat.ten_danh_muc;
                    categorySelect.appendChild(option);
                });
                displayProducts(products);
            } catch (error) {
                console.error('Lỗi khi lấy dữ liệu:', error);
                document.getElementById('productList').innerHTML = '<p class="text-center col-span-3 text-red-500">Lỗi khi tải sản phẩm.</p>';
            }
        }

        function displayProducts(productList) {
            const productListDiv = document.getElementById('productList');
            productListDiv.innerHTML = '';
            productList.forEach(product => {
                const card = `
                    <div class="bg-white shadow-md rounded-lg p-4">
                        <img src="${product.hinh_anh || '/images/default.jpg'}" alt="${product.ten_san_pham}" class="w-full h-48 object-cover mb-2 rounded" onerror="this.src='/images/default.jpg';">
                        <h3 class="text-lg font-semibold">${product.ten_san_pham}</h3>
                        <p class="text-gray-600">Giá: ${product.gia.toLocaleString('vi-VN')} VNĐ</p>
                        <button class="mt-2 bg-blue-500 text-white py-1 px-3 rounded hover:bg-blue-600" onclick="addToCart(${product.id_san_pham}, 1)">Thêm vào giỏ</button>
                        <a href="/Shopthoitrang/chi-tiet-don-hang.html">Chi tiết đơn hàng</a>
                    </div>
                `;
                productListDiv.innerHTML += card;
            });
        }

        async function addToCart(productId, quantity) {
            const cartItem = {
                id_gio_hang: Date.now(), // Tạm thời dùng timestamp làm ID
                id_khach_hang: 1, // Giả định khách hàng ID là 1 (cần tích hợp đăng nhập sau)
                id_san_pham: productId,
                so_luong: quantity,
                ngay_them: new Date().toISOString().split('T')[0] // Lấy ngày hiện tại
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
                alert(result.message || 'Thêm vào giỏ hàng thất bại');
            } catch (error) {
                console.error('Lỗi:', error);
                alert('thêm vào giỏ hàng');
            }
        }

        function filterProducts() {
            let filtered = [...products];
            const category = document.getElementById('categoryFilter').value;
            const priceRange = document.getElementById('priceRange').value;

            if (category) {
                filtered = filtered.filter(p => p.id_danh_muc == category);
            }
            if (priceRange) {
                filtered = filtered.filter(p => p.gia <= priceRange);
            }

            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            if (searchTerm) {
                filtered = filtered.filter(p => p.ten_san_pham.toLowerCase().includes(searchTerm));
            }

            const sort = document.getElementById('sortSelect').value;
            filtered.sort((a, b) => {
                if (sort === 'price-asc') return a.gia - b.gia;
                if (sort === 'price-desc') return b.gia - a.gia;
                if (sort === 'name-asc') return a.ten_san_pham.localeCompare(b.ten_san_pham);
                if (sort === 'name-desc') return b.ten_san_pham.localeCompare(a.ten_san_pham);
                return 0;
            });

            displayProducts(filtered);
        }

        document.getElementById('applyFilter').addEventListener('click', filterProducts);
        document.getElementById('searchInput').addEventListener('input', filterProducts);
        document.getElementById('sortSelect').addEventListener('change', filterProducts);
        document.getElementById('priceRange').addEventListener('input', (e) => {
            document.getElementById('priceRangeValue').textContent = `0 - ${e.target.value} VND`;
            filterProducts();
        });

        document.addEventListener('DOMContentLoaded', fetchProducts);