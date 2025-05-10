-- Tạo cơ sở dữ liệu và sử dụng
CREATE DATABASE K22CNT2_TTCD_Project4;
GO
USE K22CNT2_TTCD_Project4;
GO

-- Bảng quản trị
CREATE TABLE QuanTri (
    id_quan_tri INT PRIMARY KEY,
    Tai_khoan NVARCHAR(50) NOT NULL,
    Mat_khau NVARCHAR(50) NOT NULL,
    Trang_thai NVARCHAR(20) NOT NULL
);
GO

-- Bảng danh mục sản phẩm
CREATE TABLE DanhMuc (
    id_danh_muc INT PRIMARY KEY,
    ten_danh_muc NVARCHAR(255) NOT NULL
);
GO

-- Bảng sản phẩm
CREATE TABLE SanPham (
    id_san_pham INT PRIMARY KEY,
    ten_san_pham NVARCHAR(255) NOT NULL,
    gia DECIMAL(10,2) NOT NULL,
    so_luong INT NOT NULL,
    hinh_anh NVARCHAR(255),
    id_danh_muc INT NOT NULL,
    CONSTRAINT FK_SanPham_DanhMuc FOREIGN KEY (id_danh_muc)
        REFERENCES DanhMuc(id_danh_muc)
);
GO

-- Bảng khách hàng
CREATE TABLE KhachHang (
    id_khach_hang INT PRIMARY KEY,
    ten_khach_hang NVARCHAR(255) NOT NULL,
    so_dien_thoai NVARCHAR(20) NOT NULL,
    email NVARCHAR(255),
    dia_chi NVARCHAR(255),
    ngay_tao DATETIME NOT NULL
);
GO

-- Bảng giỏ hàng
CREATE TABLE GioHang (
    id_gio_hang INT PRIMARY KEY,
    id_khach_hang INT NOT NULL,
    id_san_pham INT NOT NULL,
    so_luong INT DEFAULT 1,
    ngay_them DATETIME NOT NULL,
    CONSTRAINT FK_GioHang_KhachHang FOREIGN KEY (id_khach_hang)
        REFERENCES KhachHang(id_khach_hang),
    CONSTRAINT FK_GioHang_SanPham FOREIGN KEY (id_san_pham)
        REFERENCES SanPham(id_san_pham)
);
GO

-- Bảng đơn hàng
CREATE TABLE DonHang (
    id_don_hang INT PRIMARY KEY,
    ngay_dat DATETIME NOT NULL,
    id_khach_hang INT NOT NULL,
    tong_tien DECIMAL(10,2) NOT NULL,
    trang_thai NVARCHAR(50) NOT NULL,
    CONSTRAINT FK_DonHang_KhachHang FOREIGN KEY (id_khach_hang)
        REFERENCES KhachHang(id_khach_hang)
);
GO

-- Bảng thanh toán
CREATE TABLE ThanhToan (
    id_thanh_toan INT PRIMARY KEY,
    id_don_hang INT NOT NULL,
    id_khach_hang INT NOT NULL,
    tong_tien DECIMAL(10,2) NOT NULL,
    phuong_thuc NVARCHAR(50) NOT NULL,
    trang_thai NVARCHAR(50) NOT NULL,
    thoi_gian DATETIME NOT NULL,
    CONSTRAINT FK_ThanhToan_DonHang FOREIGN KEY (id_don_hang)
        REFERENCES DonHang(id_don_hang),
    CONSTRAINT FK_ThanhToan_KhachHang FOREIGN KEY (id_khach_hang)
        REFERENCES KhachHang(id_khach_hang)
);
GO

-- Bảng chi tiết đơn hàng
CREATE TABLE ChiTietDonHang (
    id_chi_tiet INT PRIMARY KEY,
    id_don_hang INT NOT NULL,
    id_san_pham INT NOT NULL,
    so_luong INT NOT NULL,
    don_gia DECIMAL(10,2) NOT NULL,
    CONSTRAINT FK_ChiTietDH_DonHang FOREIGN KEY (id_don_hang)
        REFERENCES DonHang(id_don_hang),
    CONSTRAINT FK_ChiTietDH_SanPham FOREIGN KEY (id_san_pham)
        REFERENCES SanPham(id_san_pham)
);
GO

-- Bảng nhân viên
CREATE TABLE NhanVien (
    id_nhan_vien INT PRIMARY KEY,
    ten_nhan_vien NVARCHAR(255) NOT NULL,
    so_dien_thoai NVARCHAR(20) NOT NULL,
    chuc_vu NVARCHAR(100) NOT NULL
);
GO

-- Bảng QuanTri
INSERT INTO QuanTri VALUES 
(1, N'admin_fashion', N'admin123', N'Hoạt động'),
(2, N'manager1', N'pass456', N'Hoạt động'),
(3, N'testuser', N'test789', N'Đã khóa');

-- Bảng DanhMuc
INSERT INTO DanhMuc VALUES 
(1, N'Áo nam'),
(2, N'Váy nữ'),
(3, N'Phụ kiện thời trang');

-- Bảng SanPham
INSERT INTO SanPham VALUES 
(1, N'Áo thun nam trơn', 199000, 50, N'ao_thun_nam.jpg', 1),
(2, N'Váy xòe công sở', 359000, 30, N'vay_cong_so.jpg', 2),
(3, N'Mũ bucket thời trang', 129000, 70, N'mu_bucket.jpg', 3);

-- Bảng KhachHang
INSERT INTO KhachHang VALUES 
(1, N'Nguyễn Thị Hồng', N'0912345678', N'hongnguyen@gmail.com', N'Quận 1, TP.HCM', GETDATE()),
(2, N'Lê Minh Tuấn', N'0938765432', N'tuanle@yahoo.com', N'Cầu Giấy, Hà Nội', GETDATE()),
(3, N'Phạm Thảo Vy', N'0909123123', N'vypham@gmail.com', N'Hải Châu, Đà Nẵng', GETDATE());

-- Bảng GioHang
INSERT INTO GioHang VALUES 
(1, 1, 1, 2, GETDATE()),
(2, 2, 2, 1, GETDATE()),
(3, 3, 3, 3, GETDATE());

-- Bảng DonHang
INSERT INTO DonHang VALUES 
(1, GETDATE(), 1, 398000, N'Đang xử lý'),
(2, GETDATE(), 2, 359000, N'Đã giao'),
(3, GETDATE(), 3, 387000, N'Đang giao');

-- Bảng ThanhToan
INSERT INTO ThanhToan VALUES 
(1, 1, 1, 398000, N'Thanh toán khi nhận hàng', N'Chưa thanh toán', GETDATE()),
(2, 2, 2, 359000, N'VNPay', N'Thành công', GETDATE()),
(3, 3, 3, 387000, N'Momo', N'Thành công', GETDATE());

-- Bảng ChiTietDonHang
INSERT INTO ChiTietDonHang VALUES 
(1, 1, 1, 2, 199000),
(2, 2, 2, 1, 359000),
(3, 3, 3, 3, 129000);

-- Bảng NhanVien
INSERT INTO NhanVien VALUES 
(1, N'Lý Hoàng Nam', N'0967123456', N'Tư vấn bán hàng'),
(2, N'Trịnh Thị Hoa', N'0948123987', N'Quản lý đơn hàng'),
(3, N'Vũ Đức Long', N'0987654321', N'Nhân viên kho');

select * from QuanTri;
select * from NhanVien;
select * from ChiTietDonHang;
select * from ThanhToan; 
select * from GioHang;
select * from KhachHang;
select * from SanPham;
select * from DanhMuc;
select * from DonHang;

drop table QuanTri
drop  table NhanVien
Drop table ChiTietDonHang
drop table ThanhToan
drop table GioHang
Drop table KhachHang
Drop table SanPham
drop table DanhMuc
drop table DonHang