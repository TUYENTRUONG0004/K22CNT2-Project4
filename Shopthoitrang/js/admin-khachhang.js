async function fetchCustomers() {
            try {
                console.log('Gửi yêu cầu đến: http://127.0.0.1:5000/khachhang');
                const response = await fetch('http://127.0.0.1:5000/khachhang', {
                    method: 'GET',
                    mode: 'cors'
                });
                if (!response.ok) {
                    throw new Error(`Lỗi HTTP! Mã trạng thái: ${response.status} - ${response.statusText}`);
                }
                const customers = await response.json();
                console.log('Dữ liệu trả về từ API:', customers);
                const tableBody = document.getElementById('customerTableBody');
                tableBody.innerHTML = '';
                if (!Array.isArray(customers) || customers.length === 0) {
                    tableBody.innerHTML = '<tr><td colspan="6" class="py-3 px-4 text-center text-gray-500">Không có khách hàng nào.</td></tr>';
                    return;
                }
                customers.forEach(customer => {
                    const row = `
                        <tr class="hover:bg-gray-50">
                            <td class="py-3 px-4">${customer.id_khach_hang || 'N/A'}</td>
                            <td class="py-3 px-4">${customer.ten_khach_hang || 'N/A'}</td>
                            <td class="py-3 px-4">${customer.so_dien_thoai || 'N/A'}</td>
                            <td class="py-3 px-4">${customer.email || 'N/A'}</td>
                            <td class="py-3 px-4">${customer.ngay_tao ? new Date(customer.ngay_tao).toLocaleString('vi-VN') : 'N/A'}</td>
                            <td class="py-3 px-4">
                                <button class="edit-btn text-blue-500 hover:text-blue-700 mr-2" data-id="${customer.id_khach_hang || ''}">Sửa</button>
                                <button class="delete-btn text-red-500 hover:text-red-700" data-id="${customer.id_khach_hang || ''}">Xóa</button>
                            </td>
                        </tr>
                    `;
                    tableBody.innerHTML += row;
                });

                document.querySelectorAll('.edit-btn').forEach(btn => btn.addEventListener('click', editCustomer));
                document.querySelectorAll('.delete-btn').forEach(btn => btn.addEventListener('click', deleteCustomer));
            } catch (error) {
                console.error('Lỗi khi lấy danh sách khách hàng:', error);
                document.getElementById('customerTableBody').innerHTML = '<tr><td colspan="6" class="py-3 px-4 text-center text-red-500">Lỗi khi tải dữ liệu: ' + error.message + '</td></tr>';
            }
        }

        async function editCustomer(e) {
            const id = e.target.getAttribute('data-id');
            try {
                const response = await fetch(`http://127.0.0.1:5000/khachhang/${id}`, {
                    method: 'GET',
                    mode: 'cors'
                });
                if (!response.ok) {
                    throw new Error(`Lỗi HTTP! Mã trạng thái: ${response.status} - ${response.statusText}`);
                }
                const customer = await response.json();
                console.log('Dữ liệu khách hàng để chỉnh sửa:', customer);
                document.getElementById('edit-id').value = customer.id_khach_hang || '';
                document.getElementById('edit-ten').value = customer.ten_khach_hang || '';
                document.getElementById('edit-so-dien-thoai').value = customer.so_dien_thoai || '';
                document.getElementById('edit-email').value = customer.email || '';
                document.getElementById('edit-dia_chi').value = customer.dia_chi || '';
                document.getElementById('editModal').classList.remove('hidden');
            } catch (error) {
                console.error('Lỗi khi lấy thông tin khách hàng:', error);
                alert('Lỗi khi lấy thông tin khách hàng: ' + error.message);
            }
        }

        async function updateCustomer(event) {
            event.preventDefault();
            const id = document.getElementById('edit-id').value;
            const customer = {
                ten_khach_hang: document.getElementById('edit-ten').value,
                so_dien_thoai: document.getElementById('edit-so-dien-thoai').value,
                email: document.getElementById('edit-email').value,
                dia_chi: document.getElementById('edit-dia_chi').value
            };

            if (!/^[0-9]{10}$/.test(customer.so_dien_thoai)) {
                alert('Số điện thoại phải là 10 chữ số!');
                return;
            }
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(customer.email)) {
                alert('Email không hợp lệ!');
                return;
            }

            try {
                const response = await fetch(`http://127.0.0.1:5000/khachhang/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(customer)
                });
                const data = await response.json();
                if (response.ok) {
                    alert(data.message);
                    closeModal();
                    fetchCustomers();
                } else {
                    alert(data.error);
                }
            } catch (error) {
                console.error('Lỗi khi cập nhật khách hàng:', error);
                alert('Lỗi khi cập nhật khách hàng!');
            }
        }

        async function deleteCustomer(e) {
            if (confirm('Bạn có chắc muốn xóa khách hàng này?')) {
                const id = e.target.getAttribute('data-id');
                try {
                    const response = await fetch(`http://127.0.0.1:5000/khachhang/${id}`, {
                        method: 'DELETE'
                    });
                    const data = await response.json();
                    alert(data.message);
                    if (response.ok) {
                        fetchCustomers();
                    }
                } catch (error) {
                    console.error('Lỗi khi xóa khách hàng:', error);
                    alert('Lỗi khi xóa khách hàng!');
                }
            }
        }

        function closeModal() {
            document.getElementById('editModal').classList.add('hidden');
            document.getElementById('editCustomerForm').reset();
        }

        document.getElementById('editCustomerForm').addEventListener('submit', updateCustomer);
        document.addEventListener('DOMContentLoaded', fetchCustomers);