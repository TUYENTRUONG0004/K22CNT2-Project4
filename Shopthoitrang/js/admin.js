let allOrders = []; // Lưu trữ tất cả đơn hàng để lọc

    async function fetchOverview() {
      try {
        const productsResponse = await fetch('http://127.0.0.1:5000/sanpham');
        const products = await productsResponse.json();
        document.getElementById('totalProducts').innerHTML = `
          <h3 class="text-lg font-semibold text-gray-600 mb-2">Tổng sản phẩm</h3>
          <p class="text-4xl font-bold text-indigo-600">${products.length}</p>
        `;

        const ordersResponse = await fetch('http://127.0.0.1:5000/donhang');
        const orders = await ordersResponse.json();
        document.getElementById('totalOrders').innerHTML = `
          <h3 class="text-lg font-semibold text-gray-600 mb-2">Tổng đơn hàng</h3>
          <p class="text-4xl font-bold text-indigo-600">${orders.length}</p>
        `;

        const customersResponse = await fetch('http://127.0.0.1:5000/khachhang');
        const customers = await customersResponse.json();
        document.getElementById('totalCustomers').innerHTML = `
          <h3 class="text-lg font-semibold text-gray-600 mb-2">Tổng khách hàng</h3>
          <p class="text-4xl font-bold text-indigo-600">${customers.length}</p>
        `;

        const totalRevenue = orders.reduce((sum, order) => sum + order.tong_tien, 0);
        const revenueByStatus = {};
        orders.forEach(order => {
          const status = order.trang_thai;
          revenueByStatus[status] = (revenueByStatus[status] || 0) + order.tong_tien;
        });

        document.getElementById('totalRevenue').innerHTML = `
          <h3 class="text-lg font-semibold text-gray-600 mb-2">Tổng doanh thu</h3>
          <p class="text-4xl font-bold text-indigo-600">${totalRevenue.toLocaleString('vi-VN')} VNĐ</p>
          <button id="refreshRevenue" class="mt-2 text-sm text-blue-500 hover:text-blue-700 underline cursor-pointer">Làm mới</button>
          <div class="absolute hidden group-hover:block bg-gray-800 text-white text-sm rounded-lg p-4 w-64 z-10 -top-2 left-1/2 transform -translate-x-1/2 translate-y-[-100%] shadow-lg">
            <h4 class="font-semibold mb-2">Chi tiết doanh thu</h4>
            <ul id="revenueBreakdown" class="text-left">
              ${Object.entries(revenueByStatus).map(([status, amount]) => `
                <li class="mb-1">${status}: ${amount.toLocaleString('vi-VN')} VNĐ</li>
              `).join('')}
            </ul>
          </div>
        `;

        document.getElementById('refreshRevenue').addEventListener('click', fetchOverview);
      } catch (error) {
        console.error('Lỗi khi lấy dữ liệu tổng quan:', error);
        document.getElementById('totalRevenue').innerHTML = `
          <h3 class="text-lg font-semibold text-gray-600 mb-2">Tổng doanh thu</h3>
          <p class="text-4xl font-bold text-red-600">Lỗi</p>
          <button id="refreshRevenue" class="mt-2 text-sm text-blue-500 hover:text-blue-700 underline cursor-pointer">Làm mới</button>
        `;
      }
    }

    async function fetchOrders() {
      try {
        const response = await fetch('http://127.0.0.1:5000/donhang');
        allOrders = await response.json();
        const customersResponse = await fetch('http://127.0.0.1:5000/khachhang');
        const customers = await customersResponse.json();
        const customerMap = customers.reduce((map, cust) => {
          map[cust.id_khach_hang] = cust.ten_khach_hang;
          return map;
        }, {});
        renderOrders(allOrders, customerMap);
      } catch (error) {
        console.error('Lỗi khi lấy danh sách đơn hàng:', error);
        document.getElementById('orderTableBody').innerHTML = '<tr><td colspan="6" class="py-3 px-4 text-center text-red-600">Lỗi khi tải dữ liệu</td></tr>';
      }
    }

    function renderOrders(orders, customerMap) {
      const tableBody = document.getElementById('orderTableBody');
      tableBody.innerHTML = '';
      orders.forEach(order => {
        const statusClass = order.trang_thai === 'Đang xử lý' ? 'bg-yellow-200' :
                           order.trang_thai === 'Đã giao' ? 'bg-green-200' :
                           order.trang_thai === 'Đang giao' ? 'bg-orange-200' : '';
        const row = `
          <tr class="hover:bg-gray-50">
            <td class="py-3 px-4">${order.id_don_hang}</td>
            <td class="py-3 px-4">${new Date(order.ngay_dat).toLocaleString('vi-VN')}</td>
            <td class="py-3 px-4">${customerMap[order.id_khach_hang] || 'N/A'}</td>
            <td class="py-3 px-4">${order.tong_tien.toLocaleString('vi-VN')} VNĐ</td>
            <td class="py-3 px-4"><span class="inline-block px-2 py-1 rounded ${statusClass}">${order.trang_thai}</span></td>
            <td class="py-3 px-4">
              <button class="view-order-btn text-green-500 hover:text-green-700 mr-2" data-id="${order.id_don_hang}">Xem</button>
              <button class="edit-order-btn text-blue-500 hover:text-blue-700 mr-2" data-id="${order.id_don_hang}">Sửa</button>
              <button class="delete-order-btn text-red-500 hover:text-red-700" data-id="${order.id_don_hang}">Xóa</button>
            </td>
          </tr>
        `;
        tableBody.innerHTML += row;
      });

      document.querySelectorAll('.view-order-btn').forEach(btn => {
        btn.addEventListener('click', viewOrderDetails);
      });
      document.querySelectorAll('.edit-order-btn').forEach(btn => {
        btn.addEventListener('click', editOrder);
      });
      document.querySelectorAll('.delete-order-btn').forEach(btn => {
        btn.addEventListener('click', deleteOrder);
      });
    }

    async function viewOrderDetails(e) {
      const id = e.target.getAttribute('data-id');
      try {
        const response = await fetch(`http://127.0.0.1:5000/chitietdonhang/${id}`);
        const details = await response.json();
        const productsResponse = await fetch('http://127.0.0.1:5000/sanpham');
        const products = await productsResponse.json();
        const productMap = products.reduce((map, prod) => {
          map[prod.id_san_pham] = prod.ten_san_pham;
          return map;
        }, {});

        const modalContent = document.getElementById('orderDetailContent');
        modalContent.innerHTML = `
          <p class="mb-2"><strong>Mã đơn hàng:</strong> ${id}</p>
          <table class="min-w-full text-left text-sm border-t">
            <thead class="bg-gray-100">
              <tr>
                <th class="py-2 px-4">Sản phẩm</th>
                <th class="py-2 px-4">Số lượng</th>
                <th class="py-2 px-4">Đơn giá</th>
                <th class="py-2 px-4">Thành tiền</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              ${details.map(detail => `
                <tr>
                  <td class="py-2 px-4">${productMap[detail.id_san_pham] || 'N/A'}</td>
                  <td class="py-2 px-4">${detail.so_luong}</td>
                  <td class="py-2 px-4">${detail.don_gia.toLocaleString('vi-VN')} VNĐ</td>
                  <td class="py-2 px-4">${(detail.so_luong * detail.don_gia).toLocaleString('vi-VN')} VNĐ</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        `;

        const modal = document.getElementById('orderDetailModal');
        modal.classList.remove('hidden');
        document.getElementById('closeModal').addEventListener('click', () => {
          modal.classList.add('hidden');
        });
      } catch (error) {
        console.error('Lỗi khi lấy chi tiết đơn hàng:', error);
        document.getElementById('orderDetailContent').innerHTML = '<p class="text-red-600">Lỗi khi tải chi tiết đơn hàng</p>';
      }
    }

    async function editOrder(e) {
      const id = e.target.getAttribute('data-id');
      const response = await fetch(`http://127.0.0.1:5000/donhang/${id}`);
      const order = await response.json();
      if (order) {
        alert(`Chỉnh sửa đơn hàng ${order.id_don_hang}. Thêm form chỉnh sửa nếu cần.`);
      }
    }

    async function deleteOrder(e) {
      if (confirm('Bạn có chắc muốn xóa đơn hàng này?')) {
        const id = e.target.getAttribute('data-id');
        const response = await fetch(`http://127.0.0.1:5000/donhang/${id}`, {
          method: 'DELETE'
        });
        const data = await response.json();
        alert(data.message);
        if (response.ok) {
          fetchOrders();
          fetchOverview();
        }
      }
    }

    // Hiển thị danh sách đơn hàng khi nhấp vào "Quản lý đơn hàng"
    document.getElementById('manageOrdersLink').addEventListener('click', (e) => {
      e.preventDefault();
      document.querySelector('h2').textContent = 'Danh sách đơn hàng';
      document.getElementById('ordersSection').classList.remove('hidden');
      fetchOrders();
    });

    // Lọc đơn hàng theo trạng thái
    document.getElementById('statusFilter').addEventListener('change', (e) => {
      const status = e.target.value;
      const filteredOrders = status ? allOrders.filter(order => order.trang_thai === status) : allOrders;
      const customersResponse = fetch('http://127.0.0.1:5000/khachhang')
        .then(res => res.json())
        .then(customers => {
          const customerMap = customers.reduce((map, cust) => {
            map[cust.id_khach_hang] = cust.ten_khach_hang;
            return map;
          }, {});
          renderOrders(filteredOrders, customerMap);
        });
    });

    document.addEventListener('DOMContentLoaded', () => {
      fetchOverview();
      fetchOrders(); // Tự động tải danh sách đơn hàng khi trang mở
    });