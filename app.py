import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import os
import time
from io import StringIO

# File paths for user data
USER_DATA_FILE = 'user_data.csv'

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

# Initialize new users if user_data.csv does not exist or is empty
def initialize_users():
    new_users = pd.DataFrame({
        "Username": ["mira", "yono", "tini"],
        "Password": ["123", "456", "789"],
        "Role": ["user", "user", "user"]
    })

    if not os.path.exists(USER_DATA_FILE) or pd.read_csv(USER_DATA_FILE).empty:
        new_users.to_csv(USER_DATA_FILE, index=False)
    else:
        existing_users = pd.read_csv(USER_DATA_FILE)
        all_users = pd.concat([existing_users, new_users], ignore_index=True).drop_duplicates()
        all_users.to_csv(USER_DATA_FILE, index=False)

# Initialize session state variables if they are not already set
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'login_success' not in st.session_state:
    st.session_state.login_success = False

def login(username, password):
    # Dummy authentication for demonstration
    # Replace with actual authentication logic
    if username == "admin" and password == "password":
        st.session_state.logged_in_user = username
        return True
    return False

def load_data(user):
    # Function to load user-specific data
    st.write(f"Loading data for {user}")

def manage_stok_barang(user):
    st.write(f"Managing Stok Barang for {user}")

def manage_penjualan(user):
    st.write(f"Managing Penjualan for {user}")

def manage_supplier(user):
    st.write(f"Managing Supplier for {user}")

def manage_piutang_konsum(user):
    st.write(f"Managing Piutang Konsumen for {user}")

def manage_pengeluaran(user):
    st.write(f"Managing Pengeluaran for {user}")

def update_historical_data(user):
    st.write(f"Updating historical data for {user}")

# Login page
if st.session_state.logged_in_user is None:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state.login_success = True
            st.experimental_rerun()  # Reload the app to show the dashboard
        else:
            st.error("Invalid credentials, please try again.")
else:
    st.session_state.login_success = True

    # Sidebar for navigation
    with st.sidebar:
        st.title("Dashboard")
        st.write(f"**Logged in as:** {st.session_state.logged_in_user}")

        # Navigation menu
        option = option_menu(
            menu_title=None,
            options=["Stok Barang", "Penjualan", "Supplier", "Piutang Konsumen", "Pengeluaran", "Laporan Keuangan"],
            icons=["box", "cart", "person", "credit-card", "receipt", "file-text"], 
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#f0f0f0"},
                "icon": {"color": "black", "font-size": "16px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px", "--hover-color": "#ddd"},
                "nav-link-selected": {"background-color": "#007bff"},
            }
        )

    # Load user-specific data
    load_data(st.session_state.logged_in_user)

    # Dashboard based on the selected menu option
    if option == "Stok Barang":
        manage_stok_barang(st.session_state.logged_in_user)
    elif option == "Penjualan":
        manage_penjualan(st.session_state.logged_in_user)
    elif option == "Supplier":
        manage_supplier(st.session_state.logged_in_user)
    elif option == "Piutang Konsumen":
        manage_piutang_konsum(st.session_state.logged_in_user)
    elif option == "Pengeluaran":
        manage_pengeluaran(st.session_state.logged_in_user)
    elif option == "Laporan Keuangan":
        update_historical_data(st.session_state.logged_in_user)
# Function definitions
def manage_stok_barang(username):
    st.title("Manajemen Stok Barang")
    
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
            
            file_path = get_user_file_paths(username)['STOK_BARANG_FILE']
            st.session_state.stok_barang.to_csv(file_path, index=False)
            st.success("Stok barang berhasil diperbarui.")

def manage_penjualan(username):
    st.title("Manajemen Penjualan")
    
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
            
            file_path = get_user_file_paths(username)['PENJUALAN_FILE']
            st.session_state.penjualan.to_csv(file_path, index=False)
            st.success("Penjualan berhasil diperbarui.")

def manage_supplier(username):
    st.title("Manajemen Supplier")
    
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
            
            file_path = get_user_file_paths(username)['SUPPLIER_FILE']
            st.session_state.supplier.to_csv(file_path, index=False)
            st.success("Supplier berhasil diperbarui.")

def manage_piutang_konsum(username):
    st.title("Manajemen Piutang Konsumen")
    
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
            
            file_path = get_user_file_paths(username)['PIUTANG_KONSUMEN_FILE']
            st.session_state.piutang_konsum.to_csv(file_path, index=False)
            st.success("Piutang konsumen berhasil diperbarui.")

def manage_pengeluaran(username):
    st.title("Manajemen Pengeluaran")
    
    if 'pengeluaran' in st.session_state:
        st.dataframe(st.session_state.pengeluaran)
    
    st.subheader("Tambah Pengeluaran")
    
    with st.form("pengeluaran_form"):
        nama_penerima_dana = st.text_input("Nama Penerima Dana")
        keterangan = st.text_input("Keterangan")
        total_biaya = st.number_input("Total Biaya", min_value=0.0)
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_pengeluaran = pd.DataFrame({
                'Nama Penerima Dana': [nama_penerima_dana],
                'Keterangan': [keterangan],
                'Total Biaya': [total_biaya],
                'Waktu Input': [datetime.now()]
            })
            
            if 'pengeluaran' in st.session_state:
                st.session_state.pengeluaran = pd.concat([st.session_state.pengeluaran, new_pengeluaran], ignore_index=True)
            else:
                st.session_state.pengeluaran = new_pengeluaran
            
            file_path = get_user_file_paths(username)['PENGELUARAN_FILE']
            st.session_state.pengeluaran.to_csv(file_path, index=False)
            st.success("Pengeluaran berhasil diperbarui.")

def update_historical_data(username):
    st.title("Laporan Keuangan")
    
    # Aggregate and display historical data here
    st.write("Fitur ini sedang dalam pengembangan.")

# Placeholder functions for user roles, permissions, and other features
def user_role_permissions():
    st.write("Pengaturan hak akses pengguna dan fitur lainnya akan ditambahkan di sini.")
