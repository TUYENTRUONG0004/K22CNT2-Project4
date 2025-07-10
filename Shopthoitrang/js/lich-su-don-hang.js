window.onload = async () => {
      const idKhachHang = localStorage.getItem('id_khach_hang');
      if (!idKhachHang) {
        document.getElementById('message').textContent = 'Vui lòng đăng nhập để xem lịch sử đơn hàng';
        document.getElementById('orderList').innerHTML = '<tr><td colspan="4">Không có dữ liệu</td></tr>';
        return;
      }

      try {
        const res = await fetch(`http://127.0.0.1:5000/donhang?id_khach_hang=${idKhachHang}`);
        const orders = await res.json();

        const tbody = document.getElementById('orderList');
        tbody.innerHTML = '';

        if (orders.length === 0) {
          tbody.innerHTML = '<tr><td colspan="4">Chưa có đơn hàng nào</td></tr>';
          return;
        }

        orders.forEach(order => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${order.id_don_hang}</td>
            <td>${new Date(order.ngay_dat).toLocaleString('vi-VN')}</td>
            <td>${parseFloat(order.tong_tien).toLocaleString('vi-VN')} VNĐ</td>
            <td>${order.trang_thai}</td>
          `;
          tbody.appendChild(row);
        });

        document.getElementById('message').textContent = 'Đơn hàng gần đây của bạn';
      } catch (err) {
        console.error('Lỗi tải đơn hàng:', err);
        document.getElementById('orderList').innerHTML = '<tr><td colspan="4">Lỗi khi tải dữ liệu</td></tr>';
      }
    }