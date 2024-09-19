import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import os
import time
from io import StringIO


# Define file paths for user data
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

# Save data for the logged-in user
def save_data():
    if st.session_state.logged_in_user:
        user_files = get_user_file_paths(st.session_state.logged_in_user)
        try:
            if 'stok_barang' in st.session_state and st.session_state.stok_barang is not None:
                st.session_state.stok_barang.to_csv(user_files['STOK_BARANG_FILE'], index=False)
            if 'penjualan' in st.session_state and st.session_state.penjualan is not None:
                st.session_state.penjualan.to_csv(user_files['PENJUALAN_FILE'], index=False)
            if 'supplier' in st.session_state and st.session_state.supplier is not None:
                st.session_state.supplier.to_csv(user_files['SUPPLIER_FILE'], index=False)
            if 'piutang_konsumen' in st.session_state and st.session_state.piutang_konsumen is not None:
                st.session_state.piutang_konsumen.to_csv(user_files['PIUTANG_KONSUMEN_FILE'], index=False)
            if 'pengeluaran' in st.session_state and st.session_state.pengeluaran is not None:
                st.session_state.pengeluaran.to_csv(user_files['PENGELUARAN_FILE'], index=False)
            if 'historis_analisis_keuangan' in st.session_state and st.session_state.historis_analisis_keuangan is not None:
                st.session_state.historis_analisis_keuangan.to_csv(user_files['HISTORIS_KEUANGAN_FILE'], index=False)
            if 'historis_keuntungan_bersih' in st.session_state and st.session_state.historis_keuntungan_bersih is not None:
                st.session_state.historis_keuntungan_bersih.to_csv(user_files['HISTORIS_KEUNTUNGAN_FILE'], index=False)
            st.success("Data berhasil disimpan!")
        except Exception as e:
            st.error(f"Error saving data: {e}")

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

# Load data for the logged-in user
def load_data(username):
    user_files = get_user_file_paths(username)
    
    # Load stock barang
    try:
        if os.path.exists(user_files['STOK_BARANG_FILE']):
            st.session_state.stok_barang = pd.read_csv(user_files['STOK_BARANG_FILE'])
            if 'Waktu Input' in st.session_state.stok_barang.columns:
                st.session_state.stok_barang['Waktu Input'] = pd.to_datetime(st.session_state.stok_barang['Waktu Input'])
    except Exception as e:
        st.error(f"Error loading {user_files['STOK_BARANG_FILE']}: {e}")

    # Load penjualan
    try:
        if os.path.exists(user_files['PENJUALAN_FILE']):
            st.session_state.penjualan = pd.read_csv(user_files['PENJUALAN_FILE'])
            if 'Waktu' in st.session_state.penjualan.columns:
                st.session_state.penjualan['Waktu'] = pd.to_datetime(st.session_state.penjualan['Waktu'])
    except Exception as e:
        st.error(f"Error loading {user_files['PENJUALAN_FILE']}: {e}")

    # Load supplier
    try:
        if os.path.exists(user_files['SUPPLIER_FILE']):
            st.session_state.supplier = pd.read_csv(user_files['SUPPLIER_FILE'])
            if 'Waktu' in st.session_state.supplier.columns:
                st.session_state.supplier['Waktu'] = pd.to_datetime(st.session_state.supplier['Waktu'])
    except Exception as e:
        st.error(f"Error loading {user_files['SUPPLIER_FILE']}: {e}")

    # Load piutang_konsumen
    try:
        if os.path.exists(user_files['PIUTANG_KONSUMEN_FILE']):
            st.session_state.piutang_konsumen = pd.read_csv(user_files['PIUTANG_KONSUMEN_FILE'])
    except Exception as e:
        st.error(f"Error loading {user_files['PIUTANG_KONSUMEN_FILE']}: {e}")

    # Load pengeluaran
    try:
        if os.path.exists(user_files['PENGELUARAN_FILE']):
            st.session_state.pengeluaran = pd.read_csv(user_files['PENGELUARAN_FILE'])
    except Exception as e:
        st.error(f"Error loading {user_files['PENGELUARAN_FILE']}: {e}")

    # Load historis_analisis_keuangan
    try:
        if os.path.exists(user_files['HISTORIS_KEUANGAN_FILE']):
            st.session_state.historis_analisis_keuangan = pd.read_csv(user_files['HISTORIS_KEUANGAN_FILE'])
    except Exception as e:
        st.error(f"Error loading {user_files['HISTORIS_KEUANGAN_FILE']}: {e}")

    # Load historis_keuntungan_bersih
    try:
        if os.path.exists(user_files['HISTORIS_KEUNTUNGAN_FILE']):
            st.session_state.historis_keuntungan_bersih = pd.read_csv(user_files['HISTORIS_KEUNTUNGAN_FILE'])
    except Exception as e:
        st.error(f"Error loading {user_files['HISTORIS_KEUNTUNGAN_FILE']}: {e}")

# Function to save DataFrame to CSV
def save_to_csv(data, file_path):
    try:
        data.to_csv(file_path, index=False)
        st.success(f"Data saved successfully to {file_path}")
    except Exception as e:
        st.error(f"Error saving data to {file_path}: {e}")

# Function to load or initialize CSV file
def load_or_initialize_csv(file_path, columns):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=columns)

# Function to handle STOK_BARANG_FILE
def manage_stok_barang(username, data=None):
    file_path = get_user_file_paths(username)['STOK_BARANG_FILE']
    columns = ["Nama Barang", "Merk", "Ukuran/Kemasan", "Kode Warna/Base", "Jumlah", "Waktu Input"]
    
    if data is not None:
        save_to_csv(data, file_path)
    else:
        return load_or_initialize_csv(file_path, columns)

# Function to handle PENJUALAN_FILE
def manage_penjualan(username, data=None):
    file_path = get_user_file_paths(username)['PENJUALAN_FILE']
    columns = ["ID", "Nama Pelanggan", "Nomor Telepon", "Alamat", "Nama Barang", "Ukuran/Kemasan", "Merk", 
               "Kode Warna", "Jumlah", "Total Harga", "Keuntungan", "Waktu"]

    if data is not None:
        save_to_csv(data, file_path)
    else:
        return load_or_initialize_csv(file_path, columns)

# Function to handle SUPPLIER_FILE
def manage_supplier(username, data=None):
    file_path = get_user_file_paths(username)['SUPPLIER_FILE']
    columns = ["Nama Barang", "Merk", "Ukuran/Kemasan", "Jumlah Barang", "Nama Supplier", "Tagihan", "Waktu"]

    if data is not None:
        save_to_csv(data, file_path)
    else:
        return load_or_initialize_csv(file_path, columns)

# Function to handle PIUTANG_KONSUMEN_FILE
def manage_piutang_konsumen(username, data=None):
    file_path = get_user_file_paths(username)['PIUTANG_KONSUMEN_FILE']
    columns = ["Nama Konsumen", "Kelas", "Jumlah Piutang", "Waktu"]

    if data is not None:
        save_to_csv(data, file_path)
    else:
        return load_or_initialize_csv(file_path, columns)

# Function to handle PENGELUARAN_FILE
def manage_pengeluaran(username, data=None):
    file_path = get_user_file_paths(username)['PENGELUARAN_FILE']
    columns = ["Nama Penerima Dana", "Keterangan", "Total Biaya", "Waktu"]

    if data is not None:
        save_to_csv(data, file_path)
    else:
        return load_or_initialize_csv(file_path, columns)

# Function to handle HISTORIS_KEUANGAN_FILE
def manage_historis_keuangan(username, data=None):
    file_path = get_user_file_paths(username)['HISTORIS_KEUANGAN_FILE']
    columns = ["Tanggal", "Total Pendapatan", "Total Pengeluaran", "Keuntungan Bersih"]

    if data is not None:
        save_to_csv(data, file_path)
    else:
        return load_or_initialize_csv(file_path, columns)

# Function to handle HISTORIS_KEUNTUNGAN_FILE
def manage_historis_keuntungan(username, data=None):
    file_path = get_user_file_paths(username)['HISTORIS_KEUNTUNGAN_FILE']
    columns = ["Tanggal", "Keuntungan Bersih"]

    if data is not None:
        save_to_csv(data, file_path)
    else:
        return load_or_initialize_csv(file_path, columns)
