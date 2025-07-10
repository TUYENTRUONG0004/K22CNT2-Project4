document.getElementById('productForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const editId = document.getElementById('editId').value;
        const method = editId ? 'PUT' : 'POST';
        const url = editId ? `http://127.0.0.1:5000/sanpham/${editId}` : 'http://127.0.0.1:5000/sanpham';

        const formData = new FormData();
        formData.append('id_san_pham', document.getElementById('id_san_pham').value);
        formData.append('ten_san_pham', document.getElementById('ten_san_pham').value);
        formData.append('gia', document.getElementById('gia').value);
        formData.append('so_luong', document.getElementById('so_luong').value);
        formData.append('id_danh_muc', document.getElementById('id_danh_muc').value);
        const fileInput = document.getElementById('hinh_anh');
        if (fileInput.files[0]) {
          formData.append('hinh_anh', fileInput.files[0]);
        } else if (editId) {
          formData.append('hinh_anh', document.getElementById('currentImage').dataset.current || '');
        }

        try {
          const response = await fetch(url, {
            method: method,
            body: formData
          });
          const result = await response.json();
          if (response.ok) {
            alert(result.message || `${method === 'PUT' ? 'Cập nhật' : 'Thêm'} sản phẩm thành công`);
            resetForm();
            fetchProducts();
          } else {
            alert(`Lỗi từ server: ${result.error || 'Không xác định'}. Vui lòng kiểm tra console.`);
          }
        } catch (error) {
          console.error('Lỗi chi tiết:', error);
          alert(` ${method === 'PUT' ? 'cập nhật' : 'thêm'} sản phẩm. Click "ok".`);
        }
      });

      async function fetchProducts() {
        try {
          const response = await fetch('http://127.0.0.1:5000/sanpham');
          if (!response.ok) throw new Error('Không thể lấy dữ liệu sản phẩm');
          const products = await response.json();
          const productList = document.getElementById('productList');
          productList.innerHTML = '';
          products.forEach(product => {
            const row = `
              <tr>
                <td class="p-2">${product.id_san_pham}</td>
                <td class="p-2">${product.ten_san_pham}</td>
                <td class="p-2">${product.gia.toLocaleString('vi-VN')} VNĐ</td>
                <td class="p-2">${product.so_luong}</td>
                <td class="p-2"><img src="${product.hinh_anh || '/images/default.jpg'}" alt="${product.ten_san_pham}" class="w-16 h-16 object-cover"></td>
                <td class="p-2">${product.id_danh_muc}</td>
                <td class="p-2">
                  <button class="bg-yellow-500 text-white py-1 px-3 rounded hover:bg-yellow-600 mr-2" onclick="editProduct(${product.id_san_pham}, '${product.ten_san_pham}', ${product.gia}, ${product.so_luong}, '${product.hinh_anh || ''}', ${product.id_danh_muc})">Sửa</button>
                  <button class="bg-red-500 text-white py-1 px-3 rounded hover:bg-red-600" onclick="deleteProduct(${product.id_san_pham})">Xóa</button>
                </td>
              </tr>`;
            productList.innerHTML += row;
          });
        } catch (error) {
          console.error('Lỗi khi lấy sản phẩm:', error);
          document.getElementById('productList').innerHTML = '<tr><td colspan="7" class="text-center text-red-500">Lỗi khi tải sản phẩm.</td></tr>';
        }
      }

      function editProduct(id, ten, gia, soLuong, hinhAnh, idDanhMuc) {
        document.getElementById('editId').value = id;
        document.getElementById('id_san_pham').value = id;
        document.getElementById('ten_san_pham').value = ten;
        document.getElementById('gia').value = gia;
        document.getElementById('so_luong').value = soLuong;
        document.getElementById('id_danh_muc').value = idDanhMuc;
        document.getElementById('currentImage').textContent = hinhAnh ? `Ảnh hiện tại: ${hinhAnh}` : 'Không có ảnh';
        document.getElementById('currentImage').dataset.current = hinhAnh || '';
        document.getElementById('submitButton').textContent = 'Cập nhật sản phẩm';
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }

      function resetForm() {
        document.getElementById('productForm').reset();
        document.getElementById('editId').value = '';
        document.getElementById('currentImage').textContent = '';
        document.getElementById('currentImage').dataset.current = '';
        document.getElementById('submitButton').textContent = 'Thêm sản phẩm';
      }

      async function deleteProduct(id) {
        if (confirm(`Bạn có chắc chắn muốn xóa sản phẩm ID ${id}?`)) {
          try {
            const response = await fetch(`http://127.0.0.1:5000/sanpham/${id}`, {
              method: 'DELETE',
              headers: { 'Content-Type': 'application/json' }
            });
            const result = await response.json();
            if (response.ok) {
              alert(result.message || 'Xóa sản phẩm thành công');
              fetchProducts(); // Làm mới danh sách
            } else {
              alert(`Lỗi từ server: ${result.error || 'Không xác định'}. Vui lòng kiểm tra console.`);
            }
          } catch (error) {
            console.error('Lỗi chi tiết khi xóa:', error);
            alert('Thông báo click "ok" và reload lại');
          }
        }
      }

      document.addEventListener('DOMContentLoaded', fetchProducts);