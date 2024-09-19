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
        all_users = pd.concat([existing_users, new_users], ignore_index=True)
        all_users.to_csv(USER_DATA_FILE, index=False)

# Log in a user
def login(username, password):
    if 'user_data' not in st.session_state:
        st.error("Data pengguna tidak ditemukan.")
        return False

    user_data = st.session_state.user_data
    user = user_data[(user_data['Username'] == username) & (user_data['Password'] == password)]
    if not user.empty:
        st.session_state.logged_in_user = username
        st.session_state.user_role = user['Role'].values[0]
        st.success(f"Selamat datang, {username}!")
        return True
    else:
        st.error("Username atau password salah.")
        return False

# Initialize and load data
initialize_session_state()
load_user_data()
initialize_users()

# Login form
if st.session_state.logged_in_user is None:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.experimental_rerun()  # Reload the app to show the dashboard
else:
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

    # Load user data
    def load_data(username):
        user_files = get_user_file_paths(username)
        
        try:
            if os.path.exists(user_files['STOK_BARANG_FILE']):
                st.session_state.stok_barang = pd.read_csv(user_files['STOK_BARANG_FILE'])
                if 'Waktu Input' in st.session_state.stok_barang.columns:
                    st.session_state.stok_barang['Waktu Input'] = pd.to_datetime(st.session_state.stok_barang['Waktu Input'])
        except Exception as e:
            st.error(f"Error loading stock data: {e}")

        try:
            if os.path.exists(user_files['PENJUALAN_FILE']):
                st.session_state.penjualan = pd.read_csv(user_files['PENJUALAN_FILE'])
                if 'Waktu' in st.session_state.penjualan.columns:
                    st.session_state.penjualan['Waktu'] = pd.to_datetime(st.session_state.penjualan['Waktu'])
        except Exception as e:
            st.error(f"Error loading sales data: {e}")

        try:
            if os.path.exists(user_files['SUPPLIER_FILE']):
                st.session_state.supplier = pd.read_csv(user_files['SUPPLIER_FILE'])
                if 'Waktu' in st.session_state.supplier.columns:
                    st.session_state.supplier['Waktu'] = pd.to_datetime(st.session_state.supplier['Waktu'])
        except Exception as e:
            st.error(f"Error loading supplier data: {e}")

        try:
            if os.path.exists(user_files['PIUTANG_KONSUMEN_FILE']):
                st.session_state.piutang_konsumen = pd.read_csv(user_files['PIUTANG_KONSUMEN_FILE'])
        except Exception as e:
            st.error(f"Error loading consumer debt data: {e}")

        try:
            if os.path.exists(user_files['PENGELUARAN_FILE']):
                st.session_state.pengeluaran = pd.read_csv(user_files['PENGELUARAN_FILE'])
        except Exception as e:
            st.error(f"Error loading expenses data: {e}")

        try:
            if os.path.exists(user_files['HISTORIS_KEUANGAN_FILE']):
                st.session_state.historis_analisis_keuangan = pd.read_csv(user_files['HISTORIS_KEUANGAN_FILE'])
        except Exception as e:
            st.error(f"Error loading financial history data: {e}")

        try:
            if os.path.exists(user_files['HISTORIS_KEUNTUNGAN_FILE']):
                st.session_state.historis_keuntungan_bersih = pd.read_csv(user_files['HISTORIS_KEUNTUNGAN_FILE'])
        except Exception as e:
            st.error(f"Error loading profit history data: {e}")

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
def manage_stok_barang(username):
    st.title("Manajemen Stok Barang")
    
    # Display existing stock
    if 'stok_barang' in st.session_state:
        st.dataframe(st.session_state.stok_barang)
    
    # Add or update stock items
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
            
            st.session_state.stok_barang.to_csv(get_user_file_paths(username)['STOK_BARANG_FILE'], index=False)
            st.success("Stok barang berhasil diperbarui.")

def manage_penjualan(username):
    st.title("Manajemen Penjualan")
    
    # Display existing sales
    if 'penjualan' in st.session_state:
        st.dataframe(st.session_state.penjualan)
    
    # Add new sales
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
            
            st.session_state.penjualan.to_csv(get_user_file_paths(username)['PENJUALAN_FILE'], index=False)
            st.success("Penjualan berhasil diperbarui.")

def manage_supplier(username):
    st.title("Manajemen Supplier")
    
    # Display existing suppliers
    if 'supplier' in st.session_state:
        st.dataframe(st.session_state.supplier)
    
    # Add new supplier
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
                'Waktu': [datetime.now()]
            })
            
            if 'supplier' in st.session_state:
                st.session_state.supplier = pd.concat([st.session_state.supplier, new_supplier], ignore_index=True)
            else:
                st.session_state.supplier = new_supplier
            
            st.session_state.supplier.to_csv(get_user_file_paths(username)['SUPPLIER_FILE'], index=False)
            st.success("Supplier berhasil diperbarui.")

def manage_piutang_konsum(username):
    st.title("Manajemen Piutang Konsumen")
    
    # Display existing consumer debts
    if 'piutang_konsumen' in st.session_state:
        st.dataframe(st.session_state.piutang_konsumen)
    
    # Add new debt entry
    st.subheader("Tambah Piutang Konsumen")
    
    with st.form("piutang_form"):
        nama_konsumen = st.text_input("Nama Konsumen")
        jumlah_piutang = st.number_input("Jumlah Piutang", min_value=0.0)
        tanggal = st.date_input("Tanggal")
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_debt = pd.DataFrame({
                'Nama Konsumen': [nama_konsumen],
                'Jumlah Piutang': [jumlah_piutang],
                'Tanggal': [tanggal]
            })
            
            if 'piutang_konsumen' in st.session_state:
                st.session_state.piutang_konsumen = pd.concat([st.session_state.piutang_konsumen, new_debt], ignore_index=True)
            else:
                st.session_state.piutang_konsumen = new_debt
            
            st.session_state.piutang_konsumen.to_csv(get_user_file_paths(username)['PIUTANG_KONSUMEN_FILE'], index=False)
            st.success("Piutang konsumen berhasil diperbarui.")

def manage_pengeluaran(username):
    st.title("Manajemen Pengeluaran")
    
    # Display existing expenses
    if 'pengeluaran' in st.session_state:
        st.dataframe(st.session_state.pengeluaran)
    
    # Add new expense
    st.subheader("Tambah Pengeluaran")
    
    with st.form("expense_form"):
        keterangan = st.text_input("Keterangan")
        total_biaya = st.number_input("Total Biaya", min_value=0.0)
        tanggal = st.date_input("Tanggal")
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_expense = pd.DataFrame({
                'Keterangan': [keterangan],
                'Total Biaya': [total_biaya],
                'Tanggal': [tanggal]
            })
            
            if 'pengeluaran' in st.session_state:
                st.session_state.pengeluaran = pd.concat([st.session_state.pengeluaran, new_expense], ignore_index=True)
            else:
                st.session_state.pengeluaran = new_expense
            
            st.session_state.pengeluaran.to_csv(get_user_file_paths(username)['PENGELUARAN_FILE'], index=False)
            st.success("Pengeluaran berhasil diperbarui.")


# Function to calculate and save historical financial data
def update_historical_data(username):
    user_files = get_user_file_paths(username)
    
    # Load data
    try:
        stok_barang = pd.read_csv(user_files['STOK_BARANG_FILE'])
        penjualan = pd.read_csv(user_files['PENJUALAN_FILE'])
        pengeluaran = pd.read_csv(user_files['PENGELUARAN_FILE'])
    except Exception as e:
        st.error(f"Error loading data for financial report: {e}")
        return

    # Calculate historical data
    # (Example calculations, modify as needed)
    monthly_sales = penjualan.groupby(penjualan['Waktu'].dt.to_period('M')).agg({'Total Harga': 'sum'}).reset_index()
    monthly_expenses = pengeluaran.groupby(pengeluaran['Tanggal'].dt.to_period('M')).agg({'Total Biaya': 'sum'}).reset_index()

    # Save historical data
    try:
        if not os.path.exists(user_files['HISTORIS_KEUANGAN_FILE']):
            pd.DataFrame(columns=["Bulan", "Total Penjualan", "Total Pengeluaran"]).to_csv(user_files['HISTORIS_KEUANGAN_FILE'], index=False)
        historical_financials = pd.read_csv(user_files['HISTORIS_KEUANGAN_FILE'])
        updated_financials = pd.concat([historical_financials, pd.merge(monthly_sales, monthly_expenses, left_on='Waktu', right_on='Tanggal')], ignore_index=True)
        updated_financials.to_csv(user_files['HISTORIS_KEUANGAN_FILE'], index=False)
    except Exception as e:
        st.error(f"Error saving historical financial data: {e}")

    st.success("Laporan keuangan berhasil diperbarui.")

def manage_stok_barang(username):
    st.title("Manajemen Stok Barang")
    # Add functionality for managing stock items here

def manage_penjualan(username):
    st.title("Manajemen Penjualan")
    # Add functionality for managing sales here

def manage_supplier(username):
    st.title("Manajemen Supplier")
    # Add functionality for managing suppliers here

def manage_piutang_konsum(username):
    st.title("Manajemen Piutang Konsumen")
    # Add functionality for managing consumer debts here

def manage_pengeluaran(username):
    st.title("Manajemen Pengeluaran")
    # Add functionality for managing expenses here


