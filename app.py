import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import os
import time
from io import StringIO

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
from datetime import datetime

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
        'OWNER_FILE': f'{username}_owner_data.csv'  # Add owner data file
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
        initialize_users()  # Initialize with default users if file is missing

# Initialize new users if user_data.csv does not exist or is empty
def initialize_users():
    new_users = pd.DataFrame({
        "Username": ["mira", "yono", "tini"],
        "Password": ["123oke", "456", "789"],
        "Role": ["user", "user", "user"]
    })
    new_users.to_csv(USER_DATA_FILE, index=False)

# Function to manage stock items
def manage_stok_barang(username):
    st.title("Manajemen Stok Barang")
    
    # Load stock data if available
    file_path = get_user_file_paths(username)['STOK_BARANG_FILE']
    if os.path.exists(file_path):
        st.session_state.stok_barang = pd.read_csv(file_path)
    else:
        st.session_state.stok_barang = pd.DataFrame(columns=['Nama Barang', 'Merk', 'Ukuran/Kemasan', 'Jumlah', 'Harga', 'Waktu Input'])

    if 'stok_barang' in st.session_state:
        st.dataframe(st.session_state.stok_barang)
    
    st.subheader("Tambah/Update Stok Barang")
    
    with st.form("stock_form"):
        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        ukuran_kemasan = st.text_input("Ukuran/Kemasan")
        jumlah = st.number_input("Jumlah", min_value=0)
        harga = st.number_input("Harga", min_value=0.0)
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_stock = pd.DataFrame({
                'Nama Barang': [nama_barang],
                'Merk': [merk],
                'Ukuran/Kemasan': [ukuran_kemasan],
                'Jumlah': [jumlah],
                'Harga': [harga],
                'Waktu Input': [datetime.now()]
            })
            
            if 'stok_barang' in st.session_state:
                st.session_state.stok_barang = pd.concat([st.session_state.stok_barang, new_stock], ignore_index=True)
            else:
                st.session_state.stok_barang = new_stock
            
            st.session_state.stok_barang.to_csv(file_path, index=False)
            st.success("Stok barang berhasil diperbarui.")

# Function to manage sales
def manage_penjualan(username):
    st.title("Manajemen Penjualan")
    
    # Load sales data if available
    file_path = get_user_file_paths(username)['PENJUALAN_FILE']
    if os.path.exists(file_path):
        st.session_state.penjualan = pd.read_csv(file_path)
    else:
        st.session_state.penjualan = pd.DataFrame(columns=['Nama Pelanggan', 'Nomor Telepon', 'Alamat', 'Nama Barang', 'Jumlah', 'Harga Jual', 'Total Harga', 'Waktu'])

    if 'penjualan' in st.session_state:
        st.dataframe(st.session_state.penjualan)
    
    st.subheader("Tambah Penjualan")
    
    with st.form("sales_form"):
        nama_pelanggan = st.text_input("Nama Pelanggan")
        nomor_telepon = st.text_input("Nomor Telepon")
        alamat = st.text_input("Alamat")
        nama_barang = st.text_input("Nama Barang")
        jumlah = st.number_input("Jumlah", min_value=1)
        harga_jual = st.number_input("Harga Jual", min_value=0.0)
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            total_harga = jumlah * harga_jual
            new_sale = pd.DataFrame({
                'Nama Pelanggan': [nama_pelanggan],
                'Nomor Telepon': [nomor_telepon],
                'Alamat': [alamat],
                'Nama Barang': [nama_barang],
                'Jumlah': [jumlah],
                'Harga Jual': [harga_jual],
                'Total Harga': [total_harga],
                'Waktu': [datetime.now()]
            })
            
            if 'penjualan' in st.session_state:
                st.session_state.penjualan = pd.concat([st.session_state.penjualan, new_sale], ignore_index=True)
            else:
                st.session_state.penjualan = new_sale
            
            st.session_state.penjualan.to_csv(file_path, index=False)
            st.success("Penjualan berhasil diperbarui.")

# Function to manage suppliers
def manage_supplier(username):
    st.title("Manajemen Supplier")
    
    # Load supplier data if available
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
            
            if 'supplier' in st.session_state:
                st.session_state.supplier = pd.concat([st.session_state.supplier, new_supplier], ignore_index=True)
            else:
                st.session_state.supplier = new_supplier
            
            st.session_state.supplier.to_csv(file_path, index=False)
            st.success("Supplier berhasil diperbarui.")

# Function to manage consumer debts
def manage_piutang_konsum(username):
    st.title("Manajemen Piutang Konsumen")
    
    # Load consumer debt data if available
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
            
            if 'piutang_konsum' in st.session_state:
                st.session_state.piutang_konsum = pd.concat([st.session_state.piutang_konsum, new_piutang], ignore_index=True)
            else:
                st.session_state.piutang_konsum = new_piutang
            
            st.session_state.piutang_konsum.to_csv(file_path, index=False)
            st.success("Piutang konsumen berhasil diperbarui.")

# Function to manage expenses
def manage_pengeluaran(username):
    st.title("Manajemen Pengeluaran")
    
    # Load expense data if available
    file_path = get_user_file_paths(username)['PENGELUARAN_FILE']
    if os.path.exists(file_path):
        st.session_state.pengeluaran = pd.read_csv(file_path)
    else:
        st.session_state.pengeluaran = pd.DataFrame(columns=['Nama Pengeluaran', 'Jumlah', 'Tanggal', 'Waktu Input'])

    if 'pengeluaran' in st.session_state:
        st.dataframe(st.session_state.pengeluaran)
    
    st.subheader("Tambah Pengeluaran")
    
    with st.form("expense_form"):
        nama_pengeluaran = st.text_input("Nama Pengeluaran")
        jumlah = st.number_input("Jumlah", min_value=0.0)
        tanggal = st.date_input("Tanggal", value=datetime.now())
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_expense = pd.DataFrame({
                'Nama Pengeluaran': [nama_pengeluaran],
                'Jumlah': [jumlah],
                'Tanggal': [tanggal],
                'Waktu Input': [datetime.now()]
            })
            
            if 'pengeluaran' in st.session_state:
                st.session_state.pengeluaran = pd.concat([st.session_state.pengeluaran, new_expense], ignore_index=True)
            else:
                st.session_state.pengeluaran = new_expense
            
            st.session_state.pengeluaran.to_csv(file_path, index=False)
            st.success("Pengeluaran berhasil diperbarui.")

# Function to update historical financial data
def update_historical_data(username):
    st.title("Laporan Keuangan")
    
    # Load financial data
    historical_file = get_user_file_paths(username)['HISTORIS_KEUANGAN_FILE']
    if os.path.exists(historical_file):
        st.session_state.historical_data = pd.read_csv(historical_file)
    else:
        st.session_state.historical_data = pd.DataFrame(columns=['Bulan', 'Total Penjualan', 'Total Pengeluaran', 'Laba Bersih'])

    if 'historical_data' in st.session_state:
        st.dataframe(st.session_state.historical_data)
    
    st.subheader("Tambahkan Laporan Keuangan Bulanan")
    
    with st.form("financial_report_form"):
        bulan = st.selectbox("Pilih Bulan", [datetime(2023, m, 1).strftime('%B') for m in range(1, 13)])
        total_penjualan = st.number_input("Total Penjualan", min_value=0.0)
        total_pengeluaran = st.number_input("Total Pengeluaran", min_value=0.0)
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            laba_bersih = total_penjualan - total_pengeluaran
            new_report = pd.DataFrame({
                'Bulan': [bulan],
                'Total Penjualan': [total_penjualan],
                'Total Pengeluaran': [total_pengeluaran],
                'Laba Bersih': [laba_bersih]
            })
            
            st.session_state.historical_data = pd.concat([st.session_state.historical_data, new_report], ignore_index=True)
            st.session_state.historical_data.to_csv(historical_file, index=False)
            st.success("Laporan keuangan berhasil diperbarui.")

# Function to manage owner information
def manage_owner(username):
    st.title("Manajemen Pemilik")
    
    # Load owner data if available
    file_path = get_user_file_paths(username)['OWNER_FILE']
    if os.path.exists(file_path):
        st.session_state.owner_data = pd.read_csv(file_path)
    else:
        st.session_state.owner_data = pd.DataFrame(columns=['Nama Pemilik', 'Alamat', 'Kontak', 'Waktu Input'])

    if 'owner_data' in st.session_state:
        st.dataframe(st.session_state.owner_data)
    
    st.subheader("Tambah Pemilik")
    
    with st.form("owner_form"):
        nama_pemilik = st.text_input("Nama Pemilik")
        alamat = st.text_input("Alamat")
        kontak = st.text_input("Kontak")
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_owner = pd.DataFrame({
                'Nama Pemilik': [nama_pemilik],
                'Alamat': [alamat],
                'Kontak': [kontak],
                'Waktu Input': [datetime.now()]
            })
            
            if 'owner_data' in st.session_state:
                st.session_state.owner_data = pd.concat([st.session_state.owner_data, new_owner], ignore_index=True)
            else:
                st.session_state.owner_data = new_owner
            
            st.session_state.owner_data.to_csv(file_path, index=False)
            st.success("Data pemilik berhasil diperbarui.")

# Main application logic
def main():
    initialize_session_state()
    
    if st.session_state.logged_in_user:
        username = st.session_state.logged_in_user
        
        # Sidebar for navigation
        with st.sidebar:
            choice = option_menu("Menu", ["Manajemen Stok Barang", "Manajemen Penjualan", "Manajemen Supplier", 
                                            "Manajemen Piutang Konsumen", "Manajemen Pengeluaran", 
                                            "Laporan Keuangan", "Manajemen Pemilik"],
                                 icons=['box', 'cart', 'people', 'money', 'cash-coin', 'file-earmark-text', 'person'],
                                 menu_icon="cast", default_index=0)
        
        if choice == "Manajemen Stok Barang":
            manage_stok_barang(username)
        elif choice == "Manajemen Penjualan":
            manage_penjualan(username)
        elif choice == "Manajemen Supplier":
            manage_supplier(username)
        elif choice == "Manajemen Piutang Konsumen":
            manage_piutang_konsum(username)
        elif choice == "Manajemen Pengeluaran":
            manage_pengeluaran(username)
        elif choice == "Laporan Keuangan":
            update_historical_data(username)
        elif choice == "Manajemen Pemilik":
            manage_owner(username)
    else:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
        if st.button("Login"):
            user_data = st.session_state.user_data
            user_row = user_data[(user_data['Username'] == username) & (user_data['Password'] == password)]
            if not user_row.empty:
                st.session_state.logged_in_user = username
                st.session_state.user_role = user_row['Role'].values[0]
                st.success(f"Selamat datang, {username}!")
            else:
                st.error("Username atau password salah.")

if __name__ == "__main__":
    main()
