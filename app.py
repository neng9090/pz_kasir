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

# Load or initialize CSV file
def load_or_initialize_csv(file_path, columns):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=columns)

# Form for STOK_BARANG_FILE
def form_stok_barang():
    st.subheader("Input Stok Barang")
    with st.form(key='stok_barang_form'):
        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        ukuran_kemasan = st.text_input("Ukuran/Kemasan")
        kode_warna = st.text_input("Kode Warna/Base")
        jumlah = st.number_input("Jumlah", min_value=0)
        waktu_input = st.date_input("Waktu Input", value=pd.to_datetime("today"))

        submit_button = st.form_submit_button(label='Simpan Stok Barang')

        if submit_button:
            new_data = pd.DataFrame([{
                "Nama Barang": nama_barang,
                "Merk": merk,
                "Ukuran/Kemasan": ukuran_kemasan,
                "Kode Warna/Base": kode_warna,
                "Jumlah": jumlah,
                "Waktu Input": waktu_input
            }])
            if 'stok_barang' not in st.session_state:
                st.session_state.stok_barang = pd.DataFrame(columns=[
                    "Nama Barang", "Merk", "Ukuran/Kemasan", "Kode Warna/Base", "Jumlah", "Waktu Input"])
            st.session_state.stok_barang = pd.concat([st.session_state.stok_barang, new_data], ignore_index=True)
            save_data()

# Form for PENJUALAN_FILE
def form_penjualan():
    st.subheader("Input Penjualan")
    with st.form(key='penjualan_form'):
        id = st.text_input("ID")
        nama_pelanggan = st.text_input("Nama Pelanggan")
        nomor_telepon = st.text_input("Nomor Telepon")
        alamat = st.text_input("Alamat")
        nama_barang = st.text_input("Nama Barang")
        ukuran_kemasan = st.text_input("Ukuran/Kemasan")
        merk = st.text_input("Merk")
        kode_warna = st.text_input("Kode Warna")
        jumlah = st.number_input("Jumlah", min_value=0)
        total_harga = st.number_input("Total Harga", min_value=0.0)
        keuntungan = st.number_input("Keuntungan", min_value=0.0)
        waktu = st.date_input("Waktu", value=pd.to_datetime("today"))

        submit_button = st.form_submit_button(label='Simpan Penjualan')

        if submit_button:
            new_data = pd.DataFrame([{
                "ID": id,
                "Nama Pelanggan": nama_pelanggan,
                "Nomor Telepon": nomor_telepon,
                "Alamat": alamat,
                "Nama Barang": nama_barang,
                "Ukuran/Kemasan": ukuran_kemasan,
                "Merk": merk,
                "Kode Warna": kode_warna,
                "Jumlah": jumlah,
                "Total Harga": total_harga,
                "Keuntungan": keuntungan,
                "Waktu": waktu
            }])
            if 'penjualan' not in st.session_state:
                st.session_state.penjualan = pd.DataFrame(columns=[
                    "ID", "Nama Pelanggan", "Nomor Telepon", "Alamat", "Nama Barang", "Ukuran/Kemasan",
                    "Merk", "Kode Warna", "Jumlah", "Total Harga", "Keuntungan", "Waktu"])
            st.session_state.penjualan = pd.concat([st.session_state.penjualan, new_data], ignore_index=True)
            save_data()

# Form for SUPPLIER_FILE
def form_supplier():
    st.subheader("Input Supplier")
    with st.form(key='supplier_form'):
        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        ukuran_kemasan = st.text_input("Ukuran/Kemasan")
        jumlah_barang = st.number_input("Jumlah Barang", min_value=0)
        nama_supplier = st.text_input("Nama Supplier")
        tagihan = st.number_input("Tagihan", min_value=0.0)
        waktu = st.date_input("Waktu", value=pd.to_datetime("today"))

        submit_button = st.form_submit_button(label='Simpan Supplier')

        if submit_button:
            new_data = pd.DataFrame([{
                "Nama Barang": nama_barang,
                "Merk": merk,
                "Ukuran/Kemasan": ukuran_kemasan,
                "Jumlah Barang": jumlah_barang,
                "Nama Supplier": nama_supplier,
                "Tagihan": tagihan,
                "Waktu": waktu
            }])
            if 'supplier' not in st.session_state:
                st.session_state.supplier = pd.DataFrame(columns=[
                    "Nama Barang", "Merk", "Ukuran/Kemasan", "Jumlah Barang", "Nama Supplier", "Tagihan", "Waktu"])
            st.session_state.supplier = pd.concat([st.session_state.supplier, new_data], ignore_index=True)
            save_data()

# Form for PIUTANG_KONSUMEN_FILE
def form_piutang_konsumen():
    st.subheader("Input Piutang Konsumen")
    with st.form(key='piutang_konsumen_form'):
        nama_konsumen = st.text_input("Nama Konsumen")
        jumlah_piutang = st.number_input("Jumlah Piutang", min_value=0.0)
        tanggal = st.date_input("Tanggal", value=pd.to_datetime("today"))

        submit_button = st.form_submit_button(label='Simpan Piutang Konsumen')

        if submit_button:
            new_data = pd.DataFrame([{
                "Nama Konsumen": nama_konsumen,
                "Jumlah Piutang": jumlah_piutang,
                "Tanggal": tanggal
            }])
            if 'piutang_konsumen' not in st.session_state:
                st.session_state.piutang_konsumen = pd.DataFrame(columns=[
                    "Nama Konsumen", "Jumlah Piutang", "Tanggal"])
            st.session_state.piutang_konsumen = pd.concat([st.session_state.piutang_konsumen, new_data], ignore_index=True)
            save_data()

# Form for PENGELUARAN_FILE
def form_pengeluaran():
    st.subheader("Input Pengeluaran")
    with st.form(key='pengeluaran_form'):
        nama_penerima_dana = st.text_input("Nama Penerima Dana")
        keterangan = st.text_input("Keterangan")
        total_biaya = st.number_input("Total Biaya", min_value=0.0)
        tanggal = st.date_input("Tanggal", value=pd.to_datetime("today"))

        submit_button = st.form_submit_button(label='Simpan Pengeluaran')

        if submit_button:
            new_data = pd.DataFrame([{
                "Nama Penerima Dana": nama_penerima_dana,
                "Keterangan": keterangan,
                "Total Biaya": total_biaya,
                "Tanggal": tanggal
            }])
            if 'pengeluaran' not in st.session_state:
                st.session_state.pengeluaran = pd.DataFrame(columns=[
                    "Nama Penerima Dana", "Keterangan", "Total Biaya", "Tanggal"])
            st.session_state.pengeluaran = pd.concat([st.session_state.pengeluaran, new_data], ignore_index=True)
            save_data()

# Form for HISTORIS_KEUANGAN_FILE
def form_historis_analisis_keuangan():
    st.subheader("Input Historis Analisis Keuangan")
    with st.form(key='historis_analisis_keuangan_form'):
        bulan = st.text_input("Bulan")
        total_pendapatan = st.number_input("Total Pendapatan", min_value=0.0)
        total_pengeluaran = st.number_input("Total Pengeluaran", min_value=0.0)
        saldo = st.number_input("Saldo", min_value=0.0)

        submit_button = st.form_submit_button(label='Simpan Analisis Keuangan')

        if submit_button:
            new_data = pd.DataFrame([{
                "Bulan": bulan,
                "Total Pendapatan": total_pendapatan,
                "Total Pengeluaran": total_pengeluaran,
                "Saldo": saldo
            }])
            if 'historis_analisis_keuangan' not in st.session_state:
                st.session_state.historis_analisis_keuangan = pd.DataFrame(columns=[
                    "Bulan", "Total Pendapatan", "Total Pengeluaran", "Saldo"])
            st.session_state.historis_analisis_keuangan = pd.concat([st.session_state.historis_analisis_keuangan, new_data], ignore_index=True)
            save_data()

# Form for HISTORIS_KEUNTUNGAN_FILE
def form_historis_keuntungan_bersih():
    st.subheader("Input Historis Keuntungan Bersih")
    with st.form(key='historis_keuntungan_bersih_form'):
        bulan = st.text_input("Bulan")
        total_keuntungan = st.number_input("Total Keuntungan", min_value=0.0)

        submit_button = st.form_submit_button(label='Simpan Keuntungan Bersih')

        if submit_button:
            new_data = pd.DataFrame([{
                "Bulan": bulan,
                "Total Keuntungan": total_keuntungan
            }])
            if 'historis_keuntungan_bersih' not in st.session_state:
                st.session_state.historis_keuntungan_bersih = pd.DataFrame(columns=[
                    "Bulan", "Total Keuntungan"])
            st.session_state.historis_keuntungan_bersih = pd.concat([st.session_state.historis_keuntungan_bersih, new_data], ignore_index=True)
            save_data()

# Main Streamlit app
def main():
    st.title("Aplikasi Manajemen Data")

    # Initialize session state
    initialize_session_state()
    load_user_data()
    initialize_users()

    # Login form
    if st.session_state.logged_in_user is None:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        login_button = st.button("Login")

        if login_button:
            if login(username, password):
                load_data(username)
    else:
        st.sidebar.title(f"Welcome {st.session_state.logged_in_user}")
        st.sidebar.button("Logout", on_click=lambda: st.session_state.update({'logged_in_user': None, 'user_role': None}))

        st.subheader("Forms")
        
        # Display forms
        form_stok_barang()
        form_penjualan()
        form_supplier()
        form_piutang_konsumen()
        form_pengeluaran()
        form_historis_analisis_keuangan()
        form_historis_keuntungan_bersih()

if __name__ == "__main__":
    main()
