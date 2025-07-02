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
    id_khach_hang INT IDENTITY(1,1) PRIMARY KEY,
    ten_khach_hang NVARCHAR(255) NOT NULL,
    so_dien_thoai NVARCHAR(20) NOT NULL,
    email NVARCHAR(255),
    dia_chi NVARCHAR(255),
    ngay_tao DATETIME NOT NULL
);
GO

-- Bảng giỏ hàng
CREATE TABLE GioHang (
    id_gio_hang INT IDENTITY(1,1) PRIMARY KEY,
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
    id_don_hang INT IDENTITY(1,1) PRIMARY KEY,
    ngay_dat DATETIME NOT NULL,
    id_khach_hang INT NOT NULL,
    tong_tien DECIMAL(10,2) NOT NULL,
    trang_thai NVARCHAR(50) NOT NULL,
    CONSTRAINT FK_DonHang_KhachHang FOREIGN KEY (id_khach_hang)
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
INSERT INTO KhachHang (ten_khach_hang, so_dien_thoai, email, dia_chi, ngay_tao) VALUES 
(N'Nguyễn Thị Hồng', N'0912345678', N'hongnguyen@gmail.com', N'Quận 1, TP.HCM', GETDATE()),
(N'Lê Minh Tuấn', N'0938765432', N'tuanle@yahoo.com', N'Cầu Giấy, Hà Nội', GETDATE()),
(N'Phạm Thảo Vy', N'0909123123', N'vypham@gmail.com', N'Hải Châu, Đà Nẵng', GETDATE());

-- Bảng GioHang
INSERT INTO GioHang (id_khach_hang, id_san_pham, so_luong, ngay_them) VALUES 
(1, 1, 2, GETDATE()),
(2, 2, 1, GETDATE()); 

-- Bảng DonHang
INSERT INTO DonHang (ngay_dat, id_khach_hang, tong_tien, trang_thai) VALUES 
(GETDATE(), 1, 398000, N'Đang xử lý'),
(GETDATE(), 2, 359000, N'Đã giao'),
(GETDATE(), 3, 387000, N'Đang giao');


-- Bảng ChiTietDonHang
INSERT INTO ChiTietDonHang VALUES 
(1, 1, 1, 2, 199000),
(2, 2, 2, 1, 359000),
(3, 3, 3, 3, 129000);


select * from QuanTri;
select * from ChiTietDonHang;
select * from GioHang;
select * from KhachHang;
select * from SanPham;
select * from DanhMuc;
select * from DonHang;

drop table QuanTri
Drop table ChiTietDonHang
drop table GioHang
Drop table KhachHang
Drop table SanPham
drop table DanhMuc
drop table DonHang