// Lấy id_san_pham từ URL
        const urlParams = new URLSearchParams(window.location.search);
        const idSanPham = urlParams.get('id');
        console.log('ID sản phẩm từ URL:', idSanPham); // Debug

        async function loadProductDetail() {
            if (!idSanPham || isNaN(idSanPham)) {
                document.getElementById('message').textContent = 'Không tìm thấy sản phẩm! Vui lòng thêm ?id=<số> vào URL (ví dụ: ?id=1).';
                return;
            }

            try {
                const response = await fetch(`http://127.0.0.1:5000/sanpham/${idSanPham}`, {
                    method: 'GET',
                    mode: 'cors'
                });
                console.log('Phản hồi từ API (trạng thái):', response.status); // Debug
                if (!response.ok) {
                    throw new Error(`Lỗi HTTP! Mã trạng thái: ${response.status}`);
                }
                const product = await response.json();
                console.log('Dữ liệu sản phẩm:', product); // Debug
                document.getElementById('ten-san-pham').textContent = product.ten_san_pham || 'N/A';
                document.getElementById('gia').textContent = product.gia ? product.gia.toLocaleString() : 'N/A';
                document.getElementById('so-luong').textContent = product.so_luong || 'N/A';
                document.getElementById('hinh-anh').textContent = product.hinh_anh || 'Không có';
                document.getElementById('id-danh-muc').textContent = product.id_danh_muc || 'N/A';
            } catch (error) {
                console.error('Lỗi khi tải chi tiết sản phẩm:', error);
                document.getElementById('message').textContent = `Lỗi khi tải chi tiết sản phẩm: ${error.message}`;
            }
        }

        function goBack() {
            window.location.href = '/Shopthoitrang/dat-hang.html';
        }

        // Tải chi tiết sản phẩm khi trang load
        document.addEventListener('DOMContentLoaded', loadProductDetail);