import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import os
import time
from io import StringIO

# Define file paths for user-specific data
def get_user_file_paths(username):
    return {
        'STOK_BARANG_FILE': f'{username}_stok_barang.csv',
        'PENJUALAN_FILE': f'{username}_penjualan.csv',
        'SUPPLIER_FILE': f'{username}_supplier.csv',
        'PIUTANG_KONSUMEN_FILE': f'{username}_piutang_konsum.csv',
        'PENGELUARAN_FILE': f'{username}_pengeluaran.csv',
        'HISTORIS_KEUANGAN_FILE': f'{username}_historis_analisis_keuangan.csv',
        'HISTORIS_KEUNTUNGAN_FILE': f'{username}_historis_keuntungan_bersih.csv',
        'OWNER_DATA_FILE': f'{username}_owner_data.csv'  # Owner data file
    }

# File path for user data
USER_DATA_FILE = 'user_data.csv'

def initialize_session_state():
    if 'logged_in_user' not in st.session_state:
        st.session_state.logged_in_user = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_data' not in st.session_state:
        load_user_data()

# Load user data from CSV
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        st.session_state.user_data = pd.read_csv(USER_DATA_FILE)
    else:
        st.session_state.user_data = pd.DataFrame(columns=["Username", "Password", "Role"])
        initialize_users()

def initialize_users():
    new_users = pd.DataFrame({
        "Username": ["mira", "yono", "tini"],
        "Password": ["123oke", "456", "789"],
        "Role": ["user", "user", "admin"]  # Example: one admin user
    })
    new_users.to_csv(USER_DATA_FILE, index=False)

# Function to manage stock items
def manage_stok_barang(username):
    st.title("Manajemen Stok Barang")
    
    file_path = get_user_file_paths(username)['STOK_BARANG_FILE']
    if os.path.exists(file_path):
        st.session_state.stok_barang = pd.read_csv(file_path)
    else:
        st.session_state.stok_barang = pd.DataFrame(columns=['Nama Barang', 'Merk', 'Ukuran/Kemasan', 'Jumlah', 'Harga', 'Kode Warna/Base', 'Waktu Input'])

    if 'stok_barang' in st.session_state:
        # Calculate selling price as 15% more than base price
        st.session_state.stok_barang['Harga Jual'] = st.session_state.stok_barang['Harga'] * 1.15
        # Display DataFrame excluding the 'Harga' column
        st.dataframe(st.session_state.stok_barang.drop(columns=['Harga']))

    st.subheader("Tambah/Update Stok Barang")
    
    with st.form("stock_form"):
        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        ukuran_kemasan = st.text_input("Ukuran/Kemasan")
        jumlah = st.number_input("Jumlah", min_value=0)
        harga = st.number_input("Harga", min_value=0.0)
        kode_warna_base = st.text_input("Kode Warna/Base (Opsional)")  # New field for color/base code
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_stock = pd.DataFrame({
                'Nama Barang': [nama_barang],
                'Merk': [merk],
                'Ukuran/Kemasan': [ukuran_kemasan],
                'Jumlah': [jumlah],
                'Harga': [harga],
                'Kode Warna/Base': [kode_warna_base],  # Include the new field
                'Waktu Input': [datetime.now()]
            })
            
            st.session_state.stok_barang = pd.concat([st.session_state.stok_barang, new_stock], ignore_index=True)
            # Recalculate selling price and save data
            st.session_state.stok_barang['Harga Jual'] = st.session_state.stok_barang['Harga'] * 1.15
            st.session_state.stok_barang.to_csv(file_path, index=False)
            st.success("Stok barang berhasil diperbarui.")

# Function to manage sales
def manage_penjualan(username):
    st.title("Manajemen Penjualan")
    
    file_path = get_user_file_paths(username)['PENJUALAN_FILE']
    stock_file_path = get_user_file_paths(username)['STOK_BARANG_FILE']
    
    # Load sales data
    if os.path.exists(file_path):
        st.session_state.penjualan = pd.read_csv(file_path)
    else:
        st.session_state.penjualan = pd.DataFrame(columns=['Nama Pelanggan', 'Nomor Telepon', 'Alamat', 'ID Barang', 'Nama Barang', 'Merk', 'Ukuran/Kemasan', 'Kode Warna/Base', 'Jumlah', 'Harga Jual', 'Total Harga', 'Waktu'])

    # Load stock data
    if os.path.exists(stock_file_path):
        st.session_state.stok_barang = pd.read_csv(stock_file_path)
    else:
        st.session_state.stok_barang = pd.DataFrame(columns=['ID Barang', 'Nama Barang', 'Merk', 'Ukuran/Kemasan', 'Jumlah', 'Kode Warna/Base', 'Harga Jual', 'Waktu Input'])
    
    # Display sales data
    if 'penjualan' in st.session_state:
        st.subheader("Daftar Penjualan")
        st.dataframe(st.session_state.penjualan)
    
    st.subheader("Tambah Penjualan")
    
    with st.form("sales_form"):
        # Customer information
        nama_pelanggan = st.text_input("Nama Pelanggan")
        nomor_telepon = st.text_input("Nomor Telepon")
        alamat = st.text_input("Alamat")
        
        # Search for stock items
        search_stock = st.text_input("Cari Stok Barang")
        
        # Filter stock items based on search input
        if search_stock:
            filtered_stock = st.session_state.stok_barang[st.session_state.stok_barang['Nama Barang'].str.contains(search_stock, case=False)]
        else:
            filtered_stock = st.session_state.stok_barang
            
        # Check if there are any items to select
        if not filtered_stock.empty:
            id_barang = st.selectbox("ID Barang", filtered_stock['ID Barang'].unique())
            selected_stock = filtered_stock[filtered_stock['ID Barang'] == id_barang]
            
            # Get selected stock details
            if not selected_stock.empty:
                selected_stock = selected_stock.iloc[0]
                nama_barang = selected_stock['Nama Barang']
                merk = selected_stock['Merk']
                ukuran_kemasan = selected_stock['Ukuran/Kemasan']
                kode_warna_base = selected_stock['Kode Warna/Base']
                max_jumlah = selected_stock['Jumlah']
                harga_jual = selected_stock['Harga Jual']
            else:
                st.error("Barang tidak ditemukan.")
                return
        else:
            st.error("Tidak ada barang yang ditemukan.")
            return

        jumlah = st.number_input("Jumlah", min_value=1, max_value=max_jumlah)

        # Calculate total price based on quantity
        total_harga = jumlah * harga_jual
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            # Validate stock before making the sale
            if jumlah <= max_jumlah:
                # Create a new sale entry
                new_sale = pd.DataFrame({
                    'Nama Pelanggan': [nama_pelanggan],
                    'Nomor Telepon': [nomor_telepon],
                    'Alamat': [alamat],
                    'ID Barang': [id_barang],
                    'Nama Barang': [nama_barang],
                    'Merk': [merk],
                    'Ukuran/Kemasan': [ukuran_kemasan],
                    'Kode Warna/Base': [kode_warna_base],
                    'Jumlah': [jumlah],
                    'Harga Jual': [harga_jual],
                    'Total Harga': [total_harga],
                    'Waktu': [datetime.now()]
                })
                
                # Update sales data
                st.session_state.penjualan = pd.concat([st.session_state.penjualan, new_sale], ignore_index=True)
                st.session_state.penjualan.to_csv(file_path, index=False)
                st.success("Penjualan berhasil diperbarui.")
                
                # Update stock quantity
                st.session_state.stok_barang.loc[st.session_state.stok_barang['ID Barang'] == id_barang, 'Jumlah'] -= jumlah
                st.session_state.stok_barang.to_csv(stock_file_path, index=False)
            else:
                st.error("Jumlah melebihi stok yang tersedia.")

    # Display stock table without the 'Harga Jual' column
    st.subheader("Tabel Stok Barang")
    if 'stok_barang' in st.session_state:
        st.dataframe(st.session_state.stok_barang.drop(columns=['Harga Jual'], errors='ignore'))



# Function to manage suppliers
def manage_supplier(username):
    st.title("Manajemen Supplier")
    
    file_path = get_user_file_paths(username)['SUPPLIER_FILE']
    if os.path.exists(file_path):
        st.session_state.supplier = pd.read_csv(file_path)
    else:
        st.session_state.supplier = pd.DataFrame(columns=['Nama Supplier', 'Alamat', 'Kontak', 'Waktu Input'])

    if 'supplier' in st.session_state:
        st.dataframe(st.session_state.supplier)
    
    st.subheader("Tambah Supplier")
    
    with st.form("supplier_form"):
        nama_supplier = st.text_input("Nama Supplier")
        alamat = st.text_input("Alamat")
        kontak = st.text_input("Kontak")
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_supplier = pd.DataFrame({
                'Nama Supplier': [nama_supplier],
                'Alamat': [alamat],
                'Kontak': [kontak],
                'Waktu Input': [datetime.now()]
            })
            
            st.session_state.supplier = pd.concat([st.session_state.supplier, new_supplier], ignore_index=True)
            st.session_state.supplier.to_csv(file_path, index=False)
            st.success("Supplier berhasil diperbarui.")

# Function to manage consumer debts
def manage_piutang_konsum(username):
    st.title("Manajemen Piutang Konsumen")
    
    file_path = get_user_file_paths(username)['PIUTANG_KONSUMEN_FILE']
    if os.path.exists(file_path):
        st.session_state.piutang_konsum = pd.read_csv(file_path)
    else:
        st.session_state.piutang_konsum = pd.DataFrame(columns=['Nama Konsumen', 'Jumlah Piutang', 'Tanggal', 'Waktu Input'])

    if 'piutang_konsum' in st.session_state:
        st.dataframe(st.session_state.piutang_konsum)
    
    st.subheader("Tambah Piutang Konsumen")
    
    with st.form("piutang_form"):
        nama_konsumen = st.text_input("Nama Konsumen")
        jumlah_piutang = st.number_input("Jumlah Piutang", min_value=0.0)
        tanggal = st.date_input("Tanggal", value=datetime.now())
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_piutang = pd.DataFrame({
                'Nama Konsumen': [nama_konsumen],
                'Jumlah Piutang': [jumlah_piutang],
                'Tanggal': [tanggal],
                'Waktu Input': [datetime.now()]
            })
            
            st.session_state.piutang_konsum = pd.concat([st.session_state.piutang_konsum, new_piutang], ignore_index=True)
            st.session_state.piutang_konsum.to_csv(file_path, index=False)
            st.success("Piutang konsumen berhasil diperbarui.")

# Function to manage expenses
def manage_pengeluaran(username):
    st.title("Manajemen Pengeluaran")
    
    file_path = get_user_file_paths(username)['PENGELUARAN_FILE']
    if os.path.exists(file_path):
        st.session_state.pengeluaran = pd.read_csv(file_path)
    else:
        st.session_state.pengeluaran = pd.DataFrame(columns=['Nama Penerima Dana', 'Keterangan', 'Total Biaya', 'Waktu Input'])

    if 'pengeluaran' in st.session_state:
        st.dataframe(st.session_state.pengeluaran)
    
    st.subheader("Tambah Pengeluaran")
    
    with st.form("pengeluaran_form"):
        nama_penerima = st.text_input("Nama Penerima Dana")
        keterangan = st.text_input("Keterangan")
        total_biaya = st.number_input("Total Biaya", min_value=0.0)
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_pengeluaran = pd.DataFrame({
                'Nama Penerima Dana': [nama_penerima],
                'Keterangan': [keterangan],
                'Total Biaya': [total_biaya],
                'Waktu Input': [datetime.now()]
            })
            
            st.session_state.pengeluaran = pd.concat([st.session_state.pengeluaran, new_pengeluaran], ignore_index=True)
            st.session_state.pengeluaran.to_csv(file_path, index=False)
            st.success("Pengeluaran berhasil diperbarui.")

# Financial report function
def financial_report(username):
    st.title("Laporan Keuangan")
    
    file_paths = get_user_file_paths(username)
    
    # Load and display financial data
    try:
        penjualan = pd.read_csv(file_paths['PENJUALAN_FILE'])
        pengeluaran = pd.read_csv(file_paths['PENGELUARAN_FILE'])
        
        total_pendapatan = penjualan['Total Harga'].sum()
        total_pengeluaran = pengeluaran['Total Biaya'].sum()
        laba_bersih = total_pendapatan - total_pengeluaran
        
        st.subheader("Total Pendapatan: {}".format(total_pendapatan))
        st.subheader("Total Pengeluaran: {}".format(total_pengeluaran))
        st.subheader("Laba Bersih: {}".format(laba_bersih))
        
    except Exception as e:
        st.error("Error loading financial data: {}".format(e))

# Owner management function
def manage_owner():
    st.title("Manajemen Pemilik")
    
    password = st.text_input("Masukkan Password untuk Akses Halaman Pemilik", type="password")
    
    if st.button("Masuk Halaman"):
        if password == "9999":
            st.success("Akses diterima!")
            # Load data from all sources
            file_paths = get_user_file_paths(st.session_state.logged_in_user)
            all_data = {}
            for key in file_paths.keys():
                if os.path.exists(file_paths[key]):
                    all_data[key] = pd.read_csv(file_paths[key])
                else:
                    all_data[key] = pd.DataFrame(columns=['Data'])  # Placeholder for no data
            
            # Displaying all data tables
            st.subheader("Data Stok Barang")
            st.dataframe(all_data['STOK_BARANG_FILE'])
            st.subheader("Data Penjualan")
            st.dataframe(all_data['PENJUALAN_FILE'])
            st.subheader("Data Supplier")
            st.dataframe(all_data['SUPPLIER_FILE'])
            st.subheader("Data Piutang Konsumen")
            st.dataframe(all_data['PIUTANG_KONSUMEN_FILE'])
            st.subheader("Data Pengeluaran")
            st.dataframe(all_data['PENGELUARAN_FILE'])
            
            # Financial Report
            st.subheader("Laporan Keuangan")
            try:
                penjualan = pd.read_csv(file_paths['PENJUALAN_FILE'])
                pengeluaran = pd.read_csv(file_paths['PENGELUARAN_FILE'])
                
                total_pendapatan = penjualan['Total Harga'].sum()
                total_pengeluaran = pengeluaran['Total Biaya'].sum()
                laba_bersih = total_pendapatan - total_pengeluaran
                
                # Create a DataFrame for the financial report
                financial_report_data = pd.DataFrame({
                    'Keterangan': ['Total Pendapatan', 'Total Pengeluaran', 'Laba Bersih'],
                    'Jumlah': [total_pendapatan, total_pengeluaran, laba_bersih]
                })
                
                st.dataframe(financial_report_data)
                
            except Exception as e:
                st.error("Error loading financial data: {}".format(e))
            
            # Export option
            if st.button("Ekspor Semua Data ke Excel"):
                for key in file_paths.keys():
                    if os.path.exists(file_paths[key]):
                        df = pd.read_csv(file_paths[key])
                        df.to_excel(f"{key.replace('_FILE', '')}.xlsx", index=False)
                st.success("Data berhasil diekspor ke Excel.")
        else:
            st.error("Password salah.")

# Authentication function
def login(username, password):
    user = st.session_state.user_data[st.session_state.user_data['Username'] == username]
    if not user.empty and user['Password'].values[0] == password:
        st.session_state.logged_in_user = username
        st.session_state.user_role = user['Role'].values[0]
        return True
    return False

# Main app logic
def main():
    initialize_session_state()
    
    if st.session_state.logged_in_user:
        st.sidebar.title(f"Hello, {st.session_state.logged_in_user}")
        selected = option_menu("Menu", ["Manajemen Stok Barang", "Manajemen Penjualan", "Manajemen Supplier", "Manajemen Piutang Konsumen", "Manajemen Pengeluaran", "Laporan Keuangan", "Manajemen Pemilik"],
                               icons=['box', 'cash-coin', 'person-check', 'wallet', 'arrow-down-circle', 'bar-chart-line', 'shield-lock'], 
                               menu_icon="cast", default_index=0)

        if selected == "Manajemen Stok Barang":
            manage_stok_barang(st.session_state.logged_in_user)
        elif selected == "Manajemen Penjualan":
            manage_penjualan(st.session_state.logged_in_user)
        elif selected == "Manajemen Supplier":
            manage_supplier(st.session_state.logged_in_user)
        elif selected == "Manajemen Piutang Konsumen":
            manage_piutang_konsum(st.session_state.logged_in_user)
        elif selected == "Manajemen Pengeluaran":
            manage_pengeluaran(st.session_state.logged_in_user)
        elif selected == "Laporan Keuangan":
            financial_report(st.session_state.logged_in_user)
        elif selected == "Manajemen Pemilik":
            manage_owner()
    else:
        st.sidebar.title("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Login"):
            if login(username, password):
                st.success("Login berhasil!")
            else:
                st.error("Login gagal. Username atau password salah.")

if __name__ == "__main__":
    main()
