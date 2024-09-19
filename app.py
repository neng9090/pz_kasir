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
    if 'user_data' not in st.session_state:
        load_user_data()

# Load user data from CSV
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        st.session_state.user_data = pd.read_csv(USER_DATA_FILE)
    else:
        initialize_users()

# Initialize new users if user_data.csv does not exist
def initialize_users():
    new_users = pd.DataFrame({
        "Username": ["andi", "budi", "cici"],  # Updated usernames
        "Password": ["pass123", "mypassword", "secret"],  # Updated passwords
        "Role": ["user", "user", "user"]
    })
    new_users.to_csv(USER_DATA_FILE, index=False)

# Login function
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username == "" or password == "":
            st.sidebar.error("Username and Password cannot be empty.")
            return
        
        user_data = st.session_state.user_data[st.session_state.user_data['Username'] == username]
        
        if user_data.empty:
            st.sidebar.error("Username not found.")
        else:
            if user_data['Password'].values[0] == password:
                st.session_state.logged_in_user = username
                st.session_state.user_role = user_data['Role'].values[0]
                st.sidebar.success("Login successful!")
                st.experimental_rerun()  # Refresh the page to reflect changes
            else:
                st.sidebar.error("Incorrect password.")

# Generic function to manage data
def manage_data(username, file_key, columns, title, additional_inputs=None):
    st.title(title)

    # Load existing data
    file_path = get_user_file_paths(username)[file_key]
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
    else:
        data = pd.DataFrame(columns=columns)

    st.dataframe(data)

    st.subheader(f"Tambah/Update {title}")
    
    with st.form(f"{file_key}_form"):
        inputs = {col: st.text_input(col) if col != 'Jumlah' else st.number_input(col, min_value=0)
                  for col in columns}

        if additional_inputs:
            for input_name, input_func in additional_inputs.items():
                inputs[input_name] = input_func()

        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_data = pd.DataFrame([inputs])
            data = pd.concat([data, new_data], ignore_index=True)
            data.to_csv(file_path, index=False)
            st.success(f"{title} berhasil diperbarui.")

# Function to manage stock items
def manage_stok_barang(username):
    manage_data(username, 
                'STOK_BARANG_FILE', 
                ['Nama Barang', 'Merk', 'Ukuran/Kemasan', 'Jumlah', 'Harga', 'Waktu Input'], 
                "Stok Barang")

# Function to manage sales
def manage_penjualan(username):
    manage_data(username, 
                'PENJUALAN_FILE', 
                ['Nama Pelanggan', 'Nomor Telepon', 'Alamat', 'Nama Barang', 'Jumlah', 'Harga Jual', 'Total Harga', 'Waktu'], 
                "Penjualan", 
                {'Total Harga': lambda: st.number_input("Total Harga", min_value=0.0)})

# Function to manage suppliers
def manage_supplier(username):
    manage_data(username, 
                'SUPPLIER_FILE', 
                ['Nama Supplier', 'Alamat', 'Kontak', 'Waktu Input'], 
                "Supplier")

# Function to manage consumer debts
def manage_piutang_konsum(username):
    manage_data(username, 
                'PIUTANG_KONSUMEN_FILE', 
                ['Nama Konsumen', 'Jumlah Piutang', 'Tanggal', 'Waktu Input'], 
                "Piutang Konsumen", 
                {'Tanggal': lambda: st.date_input("Tanggal", value=datetime.now())})

# Function to manage expenses
def manage_pengeluaran(username):
    manage_data(username, 
                'PENGELUARAN_FILE', 
                ['Nama Penerima Dana', 'Keterangan', 'Total Biaya', 'Waktu Input'], 
                "Pengeluaran")

# Function to update historical financial data
def update_historical_data(username):
    manage_data(username, 
                'HISTORIS_KEUANGAN_FILE', 
                ['Tanggal', 'Total Pemasukan', 'Total Pengeluaran'], 
                "Laporan Keuangan", 
                {'Tanggal': lambda: st.date_input("Tanggal", value=datetime.now())})

# Application
def main():
    initialize_session_state()

    if st.session_state.logged_in_user is None:
        login()
    else:
        with st.sidebar:
            choice = option_menu(
                menu_title="Main Menu",
                options=["Manajemen Stok Barang", "Manajemen Penjualan", 
                         "Manajemen Supplier", "Manajemen Piutang Konsumen", 
                         "Manajemen Pengeluaran", "Laporan Keuangan"],
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
