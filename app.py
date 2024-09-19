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
        'HISTORIS_KEUNTUNGAN_FILE': f'{username}_historis_keuntungan_bersih.csv'
    }

# File path for user data
USER_DATA_FILE = 'user_data.csv'

# Initialize session state
def initialize_session_state():
    if 'logged_in_user' not in st.session_state:
        st.session_state.logged_in_user = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None

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
        st.session_state.pengeluaran = pd.DataFrame(columns=['Nama Penerima Dana', 'Keterangan', 'Total Biaya', 'Waktu Input'])

    if 'pengeluaran' in st.session_state:
        st.dataframe(st.session_state.pengeluaran)
    
    st.subheader("Tambah Pengeluaran")
    
    with st.form("expense_form"):
        nama_penerima_dana = st.text_input("Nama Penerima Dana")
        keterangan = st.text_input("Keterangan")
        total_biaya = st.number_input("Total Biaya", min_value=0.0)
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_expense = pd.DataFrame({
                'Nama Penerima Dana': [nama_penerima_dana],
                'Keterangan': [keterangan],
                'Total Biaya': [total_biaya],
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
    
    # Load historical data if available
    file_path = get_user_file_paths(username)['HISTORIS_KEUANGAN_FILE']
    if os.path.exists(file_path):
        st.session_state.historical_data = pd.read_csv(file_path)
    else:
        st.session_state.historical_data = pd.DataFrame(columns=['Tanggal', 'Total Pemasukan', 'Total Pengeluaran'])

    if 'historical_data' in st.session_state:
        st.dataframe(st.session_state.historical_data)
    
    st.subheader("Tambah Data Keuangan")
    
    with st.form("financial_form"):
        tanggal = st.date_input("Tanggal", value=datetime.now())
        total_pemasukan = st.number_input("Total Pemasukan", min_value=0.0)
        total_pengeluaran = st.number_input("Total Pengeluaran", min_value=0.0)
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_financial_data = pd.DataFrame({
                'Tanggal': [tanggal],
                'Total Pemasukan': [total_pemasukan],
                'Total Pengeluaran': [total_pengeluaran]
            })
            
            if 'historical_data' in st.session_state:
                st.session_state.historical_data = pd.concat([st.session_state.historical_data, new_financial_data], ignore_index=True)
            else:
                st.session_state.historical_data = new_financial_data
            
            st.session_state.historical_data.to_csv(file_path, index=False)
            st.success("Data keuangan berhasil diperbarui.")

# Application
def main():
    initialize_session_state()
    load_user_data()

    # Login form
    if st.session_state.logged_in_user is None:
        st.sidebar.title("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            if username in st.session_state.user_data['Username'].values:
                user_data = st.session_state.user_data[st.session_state.user_data['Username'] == username]
                if user_data['Password'].values[0] == password:
                    st.session_state.logged_in_user = username
                    st.session_state.user_role = user_data['Role'].values[0]
                    st.sidebar.success("Login successful!")
                    st.experimental_rerun()  # Refresh the page to reflect changes
                else:
                    st.sidebar.error("Incorrect password.")
            else:
                st.sidebar.error("Username not found.")
    else:
        with st.sidebar:
            choice = option_menu(
                menu_title="Main Menu",
                options=["Manajemen Stok Barang", "Manajemen Penjualan", "Manajemen Supplier", "Manajemen Piutang Konsumen", "Manajemen Pengeluaran", "Laporan Keuangan"],
                icons=["box", "cart", "person", "credit-card", "cash", "bar-chart"],
                default_index=0
            )

        if choice == "Manajemen Stok Barang":
            manage_stok_barang(st.session_state.logged_in_user)
        elif choice == "Manajemen Penjualan":
            manage_penjualan(st.session_state.logged_in_user)
        elif choice == "Manajemen Supplier":
            manage_supplier(st.session_state.logged_in_user)
        elif choice == "Manajemen Piutang Konsumen":
            manage_piutang_konsum(st.session_state.logged_in_user)
        elif choice == "Manajemen Pengeluaran":
            manage_pengeluaran(st.session_state.logged_in_user)
        elif choice == "Laporan Keuangan":
            update_historical_data(st.session_state.logged_in_user)

if __name__ == "__main__":
    main()
