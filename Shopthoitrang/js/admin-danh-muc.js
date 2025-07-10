async function getDanhMuc() {
            try {
                const response = await fetch('http://127.0.0.1:5000/danhmuc');
                if (!response.ok) throw new Error('Lỗi khi lấy danh sách danh mục');
                const data = await response.json();
                return data;
            } catch (error) {
                console.error('Lỗi API getDanhMuc:', error);
                return [];
            }
        }

        function hienThiDanhSachDanhMuc() {
            const tbody = document.getElementById('danh-muc-body');
            tbody.innerHTML = '';
            getDanhMuc().then(danhMuc => {
                danhMuc.forEach(dm => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${dm.id_danh_muc}</td>
                        <td>${dm.ten_danh_muc}</td>
                        <td>
                            <button class="edit-btn" onclick="hienFormChinhSua(${dm.id_danh_muc}, '${dm.ten_danh_muc}')">Sửa</button>
                            <button class="delete-btn" onclick="xoaDanhMuc(${dm.id_danh_muc})">Xóa</button>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            });
        }

        async function themDanhMuc() {
            const idDanhMuc = document.getElementById('id-danh-muc').value;
            const tenDanhMuc = document.getElementById('ten-danh-muc').value;

            if (!idDanhMuc || !tenDanhMuc) {
                alert('Vui lòng nhập đầy đủ thông tin!');
                return;
            }

            try {
                const response = await fetch('http://127.0.0.1:5000/danhmuc', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id_danh_muc: parseInt(idDanhMuc), ten_danh_muc: tenDanhMuc })
                });
                if (response.ok) {
                    alert('Thêm danh mục thành công!');
                    document.getElementById('id-danh-muc').value = '';
                    document.getElementById('ten-danh-muc').value = '';
                    hienThiDanhSachDanhMuc();
                } else {
                    const errorData = await response.json();
                    alert('Lỗi khi thêm danh mục: ' + errorData.error);
                }
            } catch (error) {
                console.error('Lỗi API themDanhMuc:', error);
                alert('Lỗi khi thêm danh mục!');
            }
        }

        function hienFormChinhSua(id, ten) {
            document.getElementById('edit-id-danh-muc').value = id;
            document.getElementById('edit-ten-danh-muc').value = ten;
            document.getElementById('edit-form').style.display = 'block';
        }

        function huyChinhSua() {
            document.getElementById('edit-form').style.display = 'none';
            document.getElementById('edit-id-danh-muc').value = '';
            document.getElementById('edit-ten-danh-muc').value = '';
        }

        async function luuChinhSua() {
            const id = document.getElementById('edit-id-danh-muc').value;
            const ten = document.getElementById('edit-ten-danh-muc').value;

            if (!ten) {
                alert('Vui lòng nhập tên danh mục!');
                return;
            }

            try {
                const response = await fetch(`http://127.0.0.1:5000/danhmuc/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ ten_danh_muc: ten })
                });
                if (response.ok) {
                    alert('Cập nhật danh mục thành công!');
                    huyChinhSua();
                    hienThiDanhSachDanhMuc();
                } else {
                    const errorData = await response.json();
                    alert('Lỗi khi cập nhật danh mục: ' + errorData.error);
                }
            } catch (error) {
                console.error('Lỗi API luuChinhSua:', error);
                alert('Lỗi khi cập nhật danh mục!');
            }
        }

        async function xoaDanhMuc(id) {
            if (confirm('Bạn có chắc muốn xóa danh mục này?')) {
                try {
                    const response = await fetch(`http://127.0.0.1:5000/danhmuc/${id}`, {
                        method: 'DELETE'
                    });
                    if (response.ok) {
                        alert('Xóa danh mục thành công!');
                        hienThiDanhSachDanhMuc();
                    } else {
                        const errorData = await response.json();
                        alert('Lỗi khi xóa danh mục: ' + errorData.error);
                    }
                } catch (error) {
                    console.error('Lỗi API xoaDanhMuc:', error);
                    alert('Lỗi khi xóa danh mục!');
                }
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            hienThiDanhSachDanhMuc();
        });