import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import io 
import time
from io import StringIO
from io import BytesIO
from fpdf import FPDF
import openpyxl
import os
import streamlit as st

# Define file paths for user-specific data
def get_user_file_paths(username):
    return {
        'STOK_BARANG_FILE': f'{username}_stok_barang.csv',
        'PENJUALAN_FILE': f'{username}_penjualan.csv',
        'SUPPLIER_FILE': f'{username}_supplier.csv',
        'PIUTANG_KONSUMEN_FILE': f"{username}_piutang_konsumen.csv",
        'PENGELUARAN_FILE': f'{username}_pengeluaran.csv',
        'HISTORIS_KEUANGAN_FILE': f'{username}_historis_analisis_keuangan.csv',
        'HISTORIS_KEUNTUNGAN_FILE': f'{username}_historis_keuntungan_bersih.csv',
        'EXPENSES_FILE': f"{username}_expenses.csv",
        'PROFIT_REPORT_FILE': f"{username}_profit_report.csv",
        'PENJUALAN_TANPA_STOK_FILE': f"{username}_penjualan_tanpa_stok.csv"
    }

import streamlit as st
import pandas as pd
import sqlite3
import os

# Database file path
DB_FILE = 'user_data.db'

# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize default users if the database is empty
def initialize_users():
    default_users = [
        ("rin", "123", "user"),
        ("userB34@2", "T1m3t0Sh!ne", "user"),
        ("userC56#3", "C0mpl3x#Pass", "user"),
        ("userD78$4", "S3cur3P@ssw0rd", "user"),
        ("userE90%5", "Str0ngP@ss2!", "user"),
        ("userF11^6", "D0nTGu3ssMe!", "user"),
        ("userG22&7", "Unbr3akable$", "user"),
        ("userH33*8", "1NeverGues$", "user"),
        ("userI44(9", "H@rd2Crack99", "user"),
        ("userJ55)10", "M4keItH@rd!", "user"),
        ("userK66_11", "N3wP@ssw0rd1!", "user"),
        ("userL77+12", "S3cur3N0t4U!", "user"),
        ("userM88=13", "G00dLuckN0w@", "user"),
        ("userN99{14", "D3f3atTheH@ck3r!", "user"),
        ("userO00}15", "K33pThisSecret$", "user"),
        ("userP01[16", "D0nTEv3nTry!", "user"),
        ("userQ02]17", "P@ssW0rdA1@", "user"),
        ("userR03;18", "Cr@ckMeN0t$!", "user"),
        ("userS04:19", "Y0uW1llN0tGues$", "user"),
        ("userT05'20", "Th1sIsS3cure!", "user"),
        ("userU06\"21", "N0W4Y2F1ndMe", "user"),
        ("userV07<22", "Unbr34kablePass!", "user"),
        ("userW08>23", "N0tY0urP@ss!", "user"),
        ("userX09,24", "1C4n'tB3C@ught!", "user"),
        ("userY10.25", "ThisIsHard2Crack", "user"),
        ("userZ11/26", "U$eP@ssAtY0urRisk", "user"),
        ("userAAA12|27", "G00dLuck2U!", "user"),
        ("userBBB13`28", "V3ryDifficult$", "user"),
        ("userCCC14~29", "S3cur3C0mbin@tion", "user"),
        ("userDDD15?30", "1Tr1ckYPass!", "user"),
        ("userEEE16!31", "NoM0reE@sy@", "user"),
        ("userFFF17@32", "W0n'tEasilyF1nd!", "user"),
        ("userGGG18#33", "KeepItSecret@", "user"),
        ("userHHH19$34", "L0cked4U!", "user"),
        ("userIII20%35", "IAmHard2Find!", "user"),
        ("userJJJ21^36", "C4ntGuessMyPass$", "user"),
        ("userKKK22&37", "Sh4llN0tG1veU!", "user"),
        ("userLLL23*38", "F0rg3tAb0utIt!", "user"),
        ("userMMM24(39", "1t'sN0t4WeakPass", "user"),
        ("userNNN25)40", "ImUntouch@ble", "user"),
        ("userOOO26_41", "G00dTryBuddy!", "user"),
        ("userPPP27+42", "Y0uW0n'tFind!", "user"),
        ("userQQQ28=43", "Unb3liev@bleP@ss", "user"),
        ("userRRR29{44", "ShallNotEnter@", "user"),
        ("userSSS30}45", "P@ssW0rd123!", "user"),
        ("userTTT31]46", "S@feAndSecure!", "user"),
        ("userUUU32^47", "12345QWERT!", "user"),
        ("userVVV33&48", "AbcD3fgh!", "user"),
        ("userWWW34*49", "Passw0rd!", "user"),
        ("userXXX35(50", "HelloWorld123!", "user"),
        ("userYYY36)51", "Password123!", "user"),
        ("userZZZ37_52", "MySuperSecurePass!", "user"),
        ("userAAAA38+53", "BestPasswordEver!", "user"),
        ("userBBBB39=54", "StrongPassw0rd!", "user"),
        ("userCCCC40{55", "UserPassword1!", "user"),
        ("userDDDD41}56", "VerySecretPassword!", "user"),
        ("userEEEE42[57", "HiddenPass123!", "user"),
        ("userFFFF43]58", "Secure1234!", "user"),
        ("userGGGG44;59", "UniquePassWord!", "user"),
        ("userHHHH45:60", "ExtraStrongPass!", "user"),
        ("userIIII46'61", "ComplexP@ssword!", "user"),
        ("userJJJJ47\"62", "SpecialChar$Pass!", "user"),
        ("userKKKK48<63", "Easy2RememberPass!", "user"),
        ("userLLLL49>64", "AnotherSecretPass!", "user"),
        ("userMMMM50,65", "RandomPassword1!", "user"),
        ("userNNNN51.66", "LongerPassword@123!", "user"),
        ("userOOOO52/67", "UseAtYourOwnRisk!", "user"),
        ("userPPPP53|68", "AlmostForgottenPass!", "user"),
        ("userQQQQ54`69", "MustNotTellAnyone!", "user"),
        ("userRRRR55~70", "UnbreakablePassword!", "user"),
        ("userSSSS56?71", "VeryStrongPassword!", "user"),
        ("userTTTT57!72", "PasswordWithSymbols!", "user"),
        ("userUUUU58@73", "SecuredPassWord!", "user"),
        ("userVVVV59#74", "ToughToCrack123!", "user"),
        ("userWWWW60$75", "NotYourAveragePassword!", "user"),
        ("userXXXX61%76", "PasswordWithDigits2!", "user"),
        ("userYYYY62^77", "PasswordThatIsSecure!", "user"),
        ("userZZZZ63&78", "A1SecurePassword!", "user"),
        ("userAAAA64*79", "YourPasswordIsSafe!", "user"),
        ("userBBBB65(80", "OnlyForYourEyes!", "user"),
        ("userCCCC66)81", "TopSecretPass1!", "user"),
        ("userDDDD67_82", "UseWithCaution!", "user"),
        ("userEEEE68+83", "ComplexityIsKey!", "user"),
        ("userFFFF69=84", "SecurityIsImportant!", "user"),
        ("userGGGG70{85", "SafeguardYourPassword!", "user"),
        ("userHHHH71}86", "NotEasyToGuess!", "user"),
        ("userIIII72[87", "VeryConfidential!", "user"),
        ("userJJJJ73]88", "KeepItToYourself!", "user"),
        ("userKKKK74;89", "HighlyConfidentialPass!", "user"),
        ("userLLLL75:90", "PasswordForTheWin!", "user"),
        ("userMMMM76'91", "StrongButMemorable!", "user"),
        ("userNNNN77\"92", "JustForYouPassword!", "user"),
        ("userOOOO78<93", "MySecretKey!", "user"),
        ("userPPPP79>94", "UnlockTheWorldPass!", "user"),
        ("userQQQQ80,95", "PasswordProtected1!", "user"),
        ("userRRRR81.96", "PasswordSafeForYou!", "user"),
        ("userSSSS82/97", "MakeItHardToGuess!", "user"),
        ("userTTTT83|98", "KeepItInMindPass!", "user"),
        ("userUUUU84`99", "SecurePassWithFun!", "user"),
        ("userVVVV85~100", "LifeIsGoodPassword!", "user")
    ]

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for username, password, role in default_users:
        try:
            cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        except sqlite3.IntegrityError:
            continue  # Skip if user already exists

    conn.commit()
    conn.close()

# Load user data from the database
def load_user_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT username, password, role FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

# Initialize session state variables
def initialize_session_state():
    if 'logged_in_user' not in st.session_state:
        st.session_state.logged_in_user = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None

# Main application logic
def main():
    init_db()
    
    if not os.path.exists(DB_FILE):
        initialize_users()
    
    initialize_session_state()

    # Handle login and logout
    if st.session_state.logged_in_user is None:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            user_data = load_user_data()
            for user in user_data:
                if username == user[0] and password == user[1]:
                    st.session_state.logged_in_user = username
                    st.session_state.user_role = user[2]
                    st.success("Login successful!")
                    break
            else:
                st.error("Invalid username or password.")
    else:
        st.title(f"Welcome, {st.session_state.logged_in_user}!")
        
        # Add a logout button
        if st.button("Logout"):
            st.session_state.logged_in_user = None
            st.session_state.user_role = None
            st.success("You have been logged out.")

if __name__ == "__main__":
    main()

        
def get_user_file_paths(username):
    return {
        'STOK_BARANG_FILE': f"{username}_stok_barang.csv"
    }

def manage_stok_barang(username):
    st.title("Manajemen Stok Barang")
    
    file_path = get_user_file_paths(username)['STOK_BARANG_FILE']
    
    # Load or initialize stock data
    if os.path.exists(file_path):
        stok_barang = pd.read_csv(file_path)
    else:
        stok_barang = pd.DataFrame(columns=['ID Barang', 'Nama Barang', 'Merk', 'Ukuran/Kemasan', 'Jumlah', 'Harga', 'Kode Warna/Base', 'Brand/Supplier', 'Waktu Input'])
    
    # Ensure 'ID Barang' exists
    if 'ID Barang' not in stok_barang.columns:
        stok_barang['ID Barang'] = range(1, len(stok_barang) + 1)

    # Check if 'Brand/Supplier' column exists
    if 'Brand/Supplier' not in stok_barang.columns:
        stok_barang['Brand/Supplier'] = ""

    next_id = stok_barang['ID Barang'].max() + 1 if not stok_barang.empty else 1

    st.session_state.stok_barang = stok_barang

    if not stok_barang.empty:
        stok_barang['Harga Jual'] = stok_barang['Harga'] * 1.15
        st.dataframe(stok_barang.drop(columns=['Harga']))  # Hide 'Harga' column

    st.subheader("Tambah/Update Stok Barang")
    
    with st.form("stock_form"):
        id_barang_options = stok_barang["ID Barang"].tolist() + ["Non"]
        selected_id_barang = st.selectbox("Pilih ID Barang untuk Diperbarui (Jika ada)", id_barang_options)

        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        ukuran_kemasan = st.text_input("Ukuran/Kemasan")
        jumlah = st.number_input("Jumlah", min_value=0)
        harga = st.number_input("Harga", min_value=0.0)
        kode_warna_base = st.text_input("Kode Warna/Base (Opsional)")
        brand = st.text_input("Brand/Supplier")

        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            if selected_id_barang != "Non":
                # Update the existing stock
                matching_stock = stok_barang[stok_barang['ID Barang'] == selected_id_barang]
                if not matching_stock.empty:
                    stok_barang.loc[stok_barang['ID Barang'] == selected_id_barang, 'Jumlah'] += jumlah
                    st.success("Stok barang berhasil diperbarui.")
            else:
                # Add new stock
                new_stock = pd.DataFrame({
                    'ID Barang': [next_id],
                    'Nama Barang': [nama_barang],
                    'Merk': [merk],
                    'Ukuran/Kemasan': [ukuran_kemasan],
                    'Jumlah': [jumlah],
                    'Harga': [harga],
                    'Kode Warna/Base': [kode_warna_base],
                    'Brand/Supplier': [brand],
                    'Waktu Input': [datetime.now()]
                })
                st.session_state.stok_barang = pd.concat([stok_barang, new_stock], ignore_index=True)
                st.success("Stok barang baru berhasil ditambahkan.")

            # Save updated stock data
            st.session_state.stok_barang.to_csv(file_path, index=False)
            
def get_user_file_paths(username):
    return {
        'PENJUALAN_FILE': f"{username}_penjualan.csv",
        'STOK_BARANG_FILE': f"{username}_stok_barang.csv"
    }

def manage_penjualan(username):
    st.title("Manajemen Penjualan")

    # Load sales data
    file_path = get_user_file_paths(username)['PENJUALAN_FILE']
    
    if 'penjualan' not in st.session_state:
        st.session_state.penjualan = pd.DataFrame(columns=[
            'ID Penjualan', 'Nama Pelanggan', 'Nomor Telepon', 'Alamat', 
            'Nama Barang', 'Merk', 'Ukuran/Kemasan', 
            'Jumlah', 'Harga Jual', 'Total Harga', 'Kode Warna/Base', 'Waktu', 'ID Barang'
        ])

    if os.path.exists(file_path):
        try:
            st.session_state.penjualan = pd.read_csv(file_path)
            if 'ID Penjualan' not in st.session_state.penjualan.columns:
                st.session_state.penjualan['ID Penjualan'] = range(1, len(st.session_state.penjualan) + 1)
                st.session_state.penjualan.to_csv(file_path, index=False)
                st.success("Kolom 'ID Penjualan' berhasil ditambahkan.")
        except Exception as e:
            st.error(f"Error loading penjualan file: {str(e)}")
            return
    else:
        st.warning("Tidak ada data penjualan yang ditemukan, menginisialisasi data penjualan kosong.")

    new_sale_id = st.session_state.penjualan['ID Penjualan'].max() + 1 if not st.session_state.penjualan.empty else 1

    # Customer search functionality
    st.subheader("Cari Pelanggan")
    search_customer = st.text_input("Nama Pelanggan")
    if search_customer:
        filtered_penjualan = st.session_state.penjualan[st.session_state.penjualan['Nama Pelanggan'].str.contains(search_customer, case=False)]
        if filtered_penjualan.empty:
            st.warning(f"Pelanggan dengan nama '{search_customer}' tidak ditemukan.")
        else:
            st.dataframe(filtered_penjualan)

    # Display current sales data
    st.subheader("Data Penjualan Saat Ini")
    st.session_state.penjualan['Nomor Telepon'] = st.session_state.penjualan['Nomor Telepon'].astype(str)
    st.dataframe(st.session_state.penjualan.drop(columns=['Harga Jual'], errors='ignore'))

    # Load stock data
    stok_barang_path = get_user_file_paths(username)['STOK_BARANG_FILE']
    if os.path.exists(stok_barang_path):
        try:
            st.session_state.stok_barang = pd.read_csv(stok_barang_path)
        except Exception as e:
            st.error(f"Error loading stok_barang file: {str(e)}")
            return
    else:
        st.session_state.stok_barang = pd.DataFrame(columns=[
            'ID Barang', 'Nama Barang', 'Merk', 'Ukuran/Kemasan', 
            'Jumlah', 'Harga Jual', 'Kode Warna/Base'
        ])
        st.warning("Tidak ada data stok barang yang ditemukan, menginisialisasi data stok kosong.")

    # Stock item search functionality
    st.subheader("Cari Stok Barang")
    search_item = st.text_input("Cari Barang")
    filtered_stok_barang = st.session_state.stok_barang
    if search_item:
        filtered_stok_barang = filtered_stok_barang[filtered_stok_barang['Nama Barang'].str.contains(search_item, case=False)]

    st.dataframe(filtered_stok_barang[['ID Barang', 'Nama Barang', 'Merk', 'Ukuran/Kemasan', 'Jumlah', 'Harga Jual']])

    # Form for adding/editing sales
    st.subheader("Tambah/Edit Penjualan")

    id_penjualan = st.selectbox("Pilih ID Penjualan untuk Diedit", st.session_state.penjualan["ID Penjualan"].tolist() + ["Tambah Baru"])

    if id_penjualan != "Tambah Baru":
        penjualan_edit = st.session_state.penjualan[st.session_state.penjualan["ID Penjualan"] == id_penjualan].iloc[0]
        default_values = {
            "Nama Pelanggan": penjualan_edit["Nama Pelanggan"],
            "Nomor Telepon": penjualan_edit["Nomor Telepon"],
            "Alamat": penjualan_edit["Alamat"],
            "Nama Barang": penjualan_edit["Nama Barang"],
            "Ukuran/Kemasan": penjualan_edit["Ukuran/Kemasan"],
            "Merk": penjualan_edit["Merk"],
            "Jumlah": penjualan_edit["Jumlah"],
            "Kode Warna/Base": penjualan_edit.get("Kode Warna/Base", ""),
            "ID Barang": penjualan_edit.get("ID Barang", "")
        }
    else:
        default_values = {
            "Nama Pelanggan": "",
            "Nomor Telepon": "",
            "Alamat": "",
            "Nama Barang": st.session_state.stok_barang["Nama Barang"].tolist()[0] if not st.session_state.stok_barang.empty else "",
            "Ukuran/Kemasan": st.session_state.stok_barang["Ukuran/Kemasan"].tolist()[0] if not st.session_state.stok_barang.empty else "",
            "Merk": "N/A",
            "Jumlah": 1,
            "Kode Warna/Base": "",
            "ID Barang": ""
        }

    with st.form("input_penjualan"):
        nama_pelanggan = st.text_input("Nama Pelanggan", value=default_values["Nama Pelanggan"])
        nomor_telpon = st.text_input("Nomor Telepon", value=default_values["Nomor Telepon"])
        alamat = st.text_area("Alamat", value=default_values["Alamat"])
        
        # Flexible input for item names
        nama_barang = st.text_input("Nama Barang", value=default_values["Nama Barang"])
        ukuran = st.text_input("Ukuran/Kemasan", value=default_values["Ukuran/Kemasan"])
        merk = st.text_input("Merk", value=default_values["Merk"])
        kode_warna_base = st.text_input("Kode Warna/Base", value=default_values["Kode Warna/Base"])
        
        # Select ID Barang from stock or leave empty
        id_barang_options = st.session_state.stok_barang["ID Barang"].tolist() + ["Non"]
        id_barang = st.selectbox("ID Barang", id_barang_options)

        jumlah = st.number_input("Jumlah Orderan", min_value=1, value=int(default_values["Jumlah"]))
        
        # Calculate the total price based on stock data
        selected_item = st.session_state.stok_barang[st.session_state.stok_barang['ID Barang'] == id_barang]
        total_harga = 0
        discounted_total = 0
        harga_jual = 0

        if id_barang != "Non" and not selected_item.empty:
            custom_harga_jual = st.number_input("Harga Jual (Custom, jika ada)", min_value=0.0, value=selected_item['Harga Jual'].values[0] if not selected_item.empty else 0.0)
            harga_jual = custom_harga_jual if custom_harga_jual else selected_item['Harga Jual'].values[0]
            total_harga = jumlah * harga_jual

        discount_value = st.number_input("Potongan Harga (Amount)", min_value=0.0, value=0.0)
        
        if st.form_submit_button("Cek Perhitungan"):
            discounted_total = total_harga - discount_value
            if discounted_total < 0:
                st.warning("Potongan harga lebih besar dari total harga!")
            else:
                st.write(f"Total Harga: {total_harga}")
                st.write(f"Total Setelah Potongan: {discounted_total}")
        
        submit = st.form_submit_button("Simpan Penjualan")

        if submit:
            if discount_value > total_harga:
                st.error("Potongan harga tidak boleh lebih besar dari total harga.")
            else:
                discounted_total = total_harga - discount_value

                new_sale = {
                    'ID Penjualan': new_sale_id if id_penjualan == "Tambah Baru" else id_penjualan,
                    'Nama Pelanggan': nama_pelanggan,
                    'Nomor Telepon': nomor_telpon,
                    'Alamat': alamat,
                    'Nama Barang': nama_barang,
                    'Merk': merk,
                    'Ukuran/Kemasan': ukuran,
                    'Jumlah': jumlah,
                    'Harga Jual': harga_jual,
                    'Total Harga': discounted_total,
                    'Kode Warna/Base': kode_warna_base,
                    'Waktu': pd.Timestamp.now(),
                    'ID Barang': id_barang
                }

                original_quantity = 0
                if id_penjualan != "Tambah Baru":
                    original_quantity = st.session_state.penjualan.loc[st.session_state.penjualan['ID Penjualan'] == id_penjualan, 'Jumlah'].values[0]

                if id_penjualan == "Tambah Baru":
                    st.session_state.penjualan = pd.concat([st.session_state.penjualan, pd.DataFrame([new_sale])], ignore_index=True)
                    # Reduce stock
                    if id_barang != "Non":
                        stok_barang_index = st.session_state.stok_barang[st.session_state.stok_barang['ID Barang'] == id_barang].index
                        if not stok_barang_index.empty:
                            st.session_state.stok_barang.loc[stok_barang_index[0], 'Jumlah'] -= jumlah
                else:
                    for key, value in new_sale.items():
                        st.session_state.penjualan.loc[st.session_state.penjualan['ID Penjualan'] == id_penjualan, key] = value
                    
                    # Adjust stock based on the difference in quantity
                    if id_barang != "Non":
                        stok_barang_index = st.session_state.stok_barang[st.session_state.stok_barang['ID Barang'] == id_barang].index
                        if not stok_barang_index.empty:
                            selisih = jumlah - original_quantity
                            st.session_state.stok_barang.loc[stok_barang_index[0], 'Jumlah'] -= selisih

                # Save updated sales and stock data
                st.session_state.penjualan.to_csv(file_path, index=False)
                st.session_state.stok_barang.to_csv(stok_barang_path, index=False)
                st.success("Data penjualan dan stok berhasil disimpan.")
                
    # Sales receipt generation section
    st.subheader("Download Struk Penjualan")
    receipt_header = st.text_input("Judul Struk", "STRUK PENJUALAN")
    thank_you_message = st.text_area("Pesan Terima Kasih", "Terima Kasih atas Pembelian Anda!")
    
    # Check if sales data exists before allowing ID selection
    if not st.session_state.penjualan.empty:
        sale_id_to_download = st.selectbox("Pilih ID Penjualan untuk Struk", st.session_state.penjualan['ID Penjualan'].unique())
        
    # Adjusted code for receipt formatting
    if st.button("Download Struk") and sale_id_to_download:
        if not st.session_state.penjualan.empty:
            try:
                selected_sale = st.session_state.penjualan[st.session_state.penjualan['ID Penjualan'] == sale_id_to_download]
                
                if selected_sale.empty:
                    st.error(f"Penjualan dengan ID {sale_id_to_download} tidak ditemukan.")
                else:
                    selected_sale = selected_sale.iloc[0]
    
                    # Function to safely access values
                    def get_safe_value(value, default='Tidak Diketahui'):
                        if pd.isna(value):
                            return default
                        elif isinstance(value, float):
                            return str(int(value)) if value.is_integer() else str(value)
                        else:
                            return str(value)
    
                    # Retrieve values
                    nama_pelanggan = get_safe_value(selected_sale.get('Nama Pelanggan'))
                    nomor_telepon = get_safe_value(selected_sale.get('Nomor Telepon'))
                    alamat = get_safe_value(selected_sale.get('Alamat'))
                    nama_barang = get_safe_value(selected_sale.get('Nama Barang'))
                    merk = get_safe_value(selected_sale.get('Merk'))
                    ukuran = get_safe_value(selected_sale.get('Ukuran/Kemasan'))
                    warna = get_safe_value(selected_sale.get('Kode Warna/Base'))
                    jumlah = get_safe_value(selected_sale.get('Jumlah'))
                    harga_jual = get_safe_value(selected_sale.get('Harga Jual'))
                    total_harga = get_safe_value(selected_sale.get('Total Harga'))
                    waktu = get_safe_value(selected_sale.get('Waktu'))
    
                    # Format receipt text for thermal printer
                    receipt_text = (
                        f"{'=' * 32}\n"
                        f"{receipt_header.center(32)}\n"
                        f"{'=' * 32}\n"
                        f"Nama Pelanggan : {nama_pelanggan[:20].ljust(20)}\n"
                        f"Telepon        : {nomor_telepon[:15].ljust(15)}\n"
                        f"Alamat         : {alamat[:30].ljust(30)}\n"
                        f"Nama Barang    : {nama_barang[:20].ljust(20)}\n"
                        f"Merk           : {merk[:15].ljust(15)}\n"
                        f"Ukuran         : {ukuran[:15].ljust(15)}\n"
                        f"Warna          : {warna[:15].ljust(15)}\n"
                        f"Jumlah         : {jumlah}\n"
                        f"Harga Jual     : {harga_jual}\n"
                        f"Total Harga    : {total_harga}\n"
                        f"Waktu          : {waktu}\n"
                        f"{'=' * 32}\n"
                        f"{thank_you_message.center(32)}\n"
                        f"{'=' * 32}\n"
                    )
    
                    # Display and download receipt
                    st.text(receipt_text)
                    st.download_button("Download Struk", data=receipt_text, file_name=f"struk_penjualan_{sale_id_to_download}.txt")

            except Exception as e:
                st.error(f"Error while downloading receipt: {str(e)}")
        else:
            st.warning("Data penjualan tidak tersedia untuk download.")

                
# Function to manage suppliers
def manage_supplier(username):
    st.title("Manajemen Supplier")
    
    # Load supplier data if available
    file_path = get_user_file_paths(username)['SUPPLIER_FILE']
    if os.path.exists(file_path):
        st.session_state.supplier = pd.read_csv(file_path)
    else:
        st.session_state.supplier = pd.DataFrame(columns=[
            'Nama Barang', 'Merk', 'Ukuran/Kemasan', 
            'Kode Warna/Base', 'Jumlah Barang', 
            'Nama Supplier', 'Total Tagihan', 
            'Waktu Input', 'Jatuh Tempo Tagihan'
        ])

    if 'supplier' in st.session_state:
        st.dataframe(st.session_state.supplier)

    st.subheader("Tambah Supplier")
    
    with st.form("supplier_form"):
        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        ukuran_kemasan = st.text_input("Ukuran/Kemasan")
        kode_warna = st.text_input("Kode Warna/Base")
        jumlah_barang = st.number_input("Jumlah Barang", min_value=0)
        nama_supplier = st.text_input("Nama Supplier")
        total_tagihan = st.number_input("Total Tagihan", min_value=0.0, format="%.2f")
        jatuh_tempo_tagihan = st.date_input("Jatuh Tempo Tagihan")
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_supplier = pd.DataFrame({
                'Nama Barang': [nama_barang],
                'Merk': [merk],
                'Ukuran/Kemasan': [ukuran_kemasan],
                'Kode Warna/Base': [kode_warna],
                'Jumlah Barang': [jumlah_barang],
                'Nama Supplier': [nama_supplier],
                'Total Tagihan': [total_tagihan],
                'Waktu Input': [datetime.now()],
                'Jatuh Tempo Tagihan': [jatuh_tempo_tagihan]
            })
            
            if 'supplier' in st.session_state:
                st.session_state.supplier = pd.concat([st.session_state.supplier, new_supplier], ignore_index=True)
            else:
                st.session_state.supplier = new_supplier
            
            st.session_state.supplier.to_csv(file_path, index=False)
            st.success("Supplier berhasil diperbarui.")

    st.subheader("Cari Supplier")
    search_term = st.text_input("Masukkan Nama Supplier untuk mencari")
    
    if search_term:
        filtered_suppliers = st.session_state.supplier[st.session_state.supplier['Nama Supplier'].str.contains(search_term, case=False)]
        if not filtered_suppliers.empty:
            st.dataframe(filtered_suppliers)
        else:
            st.warning("Tidak ada supplier yang ditemukan.")

# Function to manage consumer debts
def manage_piutang_konsum(username):
    st.title("Manajemen Piutang Konsumen")

    
    # Load consumer debt data if available
    file_path = get_user_file_paths(username)['PIUTANG_KONSUMEN_FILE']
    if os.path.exists(file_path):
        st.session_state.piutang_konsum = pd.read_csv(file_path)
    else:
        st.session_state.piutang_konsum = pd.DataFrame(columns=[
            'Nama Pelanggan', 'Alamat', 'Nomor Telepon',
            'Nama Barang', 'Merk', 'Ukuran/Kemasan',
            'Kode Warna/Base', 'Jumlah', 'Total Tagihan',
            'Tagihan yang Dibayar', 'Sisa Tagihan',
            'Tanggal Janji Bayar', 'Waktu Input'
        ])

    if 'piutang_konsum' in st.session_state:
        st.dataframe(st.session_state.piutang_konsum)
    
    st.subheader("Tambah Piutang Konsumen")
    
    with st.form("piutang_form"):
        nama_pelanggan = st.text_input("Nama Pelanggan")
        alamat = st.text_input("Alamat")
        nomor_telepon = st.text_input("Nomor Telepon")
        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        ukuran_kemasan = st.text_input("Ukuran/Kemasan")
        kode_warna = st.text_input("Kode Warna/Base (bila ada)")
        jumlah = st.number_input("Jumlah", min_value=0)
        total_tagihan = st.number_input("Total Tagihan", min_value=0.0)
        tagihan_dibayar = st.number_input("Tagihan yang Dibayar", min_value=0.0)
        tanggal_janji_bayar = st.date_input("Tanggal Janji Bayar", value=datetime.now())
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            sisa_tagihan = total_tagihan - tagihan_dibayar
            
            new_piutang = pd.DataFrame({
                'Nama Pelanggan': [nama_pelanggan],
                'Alamat': [alamat],
                'Nomor Telepon': [nomor_telepon],
                'Nama Barang': [nama_barang],
                'Merk': [merk],
                'Ukuran/Kemasan': [ukuran_kemasan],
                'Kode Warna/Base': [kode_warna],
                'Jumlah': [jumlah],
                'Total Tagihan': [total_tagihan],
                'Tagihan yang Dibayar': [tagihan_dibayar],
                'Sisa Tagihan': [sisa_tagihan],
                'Tanggal Janji Bayar': [tanggal_janji_bayar],
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
        st.session_state.pengeluaran = pd.DataFrame(columns=[
            'Biaya Gaji', 'Keterangan Gaji', 
            'Operasional', 'Keterangan Operasional', 
            'Biaya Lainnya', 'Keterangan Lainnya', 
            'Tanggal Input'
        ])

    if 'pengeluaran' in st.session_state:
        st.dataframe(st.session_state.pengeluaran)
    
    st.subheader("Tambah Pengeluaran")
    
    with st.form("expense_form"):
        biaya_gaji = st.number_input("Biaya Gaji", min_value=0.0)
        keterangan_gaji = st.text_input("Keterangan Gaji")
        operasional = st.number_input("Operasional", min_value=0.0)
        keterangan_operasional = st.text_input("Keterangan Operasional")
        biaya_lainnya = st.number_input("Biaya Lainnya", min_value=0.0)
        keterangan_lainnya = st.text_input("Keterangan Lainnya")
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_expense = pd.DataFrame({
                'Biaya Gaji': [biaya_gaji],
                'Keterangan Gaji': [keterangan_gaji],
                'Operasional': [operasional],
                'Keterangan Operasional': [keterangan_operasional],
                'Biaya Lainnya': [biaya_lainnya],
                'Keterangan Lainnya': [keterangan_lainnya],
                'Tanggal Input': [datetime.now().strftime('%Y-%m-%d')]
            })
            
            if 'pengeluaran' in st.session_state:
                st.session_state.pengeluaran = pd.concat([st.session_state.pengeluaran, new_expense], ignore_index=True)
            else:
                st.session_state.pengeluaran = new_expense
            
            st.session_state.pengeluaran.to_csv(file_path, index=False)
            st.success("Pengeluaran berhasil diperbarui.")
    
    # Display monthly expense history
    st.subheader("Historis Pengeluaran Bulanan")
    
    if 'pengeluaran' in st.session_state and not st.session_state.pengeluaran.empty:
        # Convert 'Tanggal Input' to datetime for filtering
        st.session_state.pengeluaran['Tanggal Input'] = pd.to_datetime(st.session_state.pengeluaran['Tanggal Input'])
        
        # Group by month and year
        monthly_expenses = st.session_state.pengeluaran.groupby(st.session_state.pengeluaran['Tanggal Input'].dt.to_period("M")).sum(numeric_only=True).reset_index()
        monthly_expenses['Tanggal Input'] = monthly_expenses['Tanggal Input'].dt.to_timestamp()
        
        st.dataframe(monthly_expenses)

# Function to get user-specific file paths
def get_user_file_paths(username):
    return {
        'STOK_BARANG_FILE': f"{username}_stok_barang.csv",
        'PENJUALAN_FILE': f"{username}_penjualan.csv",
        'HISTORIS_LAPORAN_PENJUALAN_FILE': f"{username}_historis_laporan_penjualan.csv",
        'SUPPLIER_FILE': f"{username}_supplier.csv",
        'PIUTANG_KONSUMEN_FILE': f"{username}_piutang_konsumen.csv",  # Ensure this key exists
        'PENGELUARAN_FILE': f"{username}_pengeluaran.csv"
    }
        
def update_historical_data(username):
    st.title("Laporan Keuangan")

    # Password protection
    correct_password = "Okedeh"  # Set your secure password here
    entered_password = st.text_input("Masukkan Password", type="password")

    if entered_password != correct_password:
        st.error("Password salah. Silakan coba lagi.")
        return  # Exit if password is incorrect
    
    # File paths
    file_paths = get_user_file_paths(username)
    stock_file_path = file_paths['STOK_BARANG_FILE']
    sales_file_path = file_paths['PENJUALAN_FILE']
    report_file_path = file_paths.get('HISTORIS_LAPORAN_PENJUALAN_FILE', 'historis_laporan_penjualan.csv')

    # Load stock data
    if os.path.exists(stock_file_path):
        stok_barang = pd.read_csv(stock_file_path)
    else:
        stok_barang = pd.DataFrame(columns=['ID Barang', 'Nama Barang', 'Merk', 'Ukuran/Kemasan', 'Jumlah', 'Harga', 'Harga Jual', 'Kode Warna/Base', 'Waktu Input'])

    # Load sales data
    if os.path.exists(sales_file_path):
        sales_data = pd.read_csv(sales_file_path)
    else:
        sales_data = pd.DataFrame(columns=['ID Penjualan', 'Nama Barang', 'Jumlah', 'Total Harga', 'Waktu Penjualan'])

    st.subheader("Manajemen Penjualan")

    # Display the sales management table
    if sales_file_path and os.path.exists(sales_file_path):
        sales_data = pd.read_csv(sales_file_path)

        # Calculate Profit (Keuntungan)
        if 'Total Harga' in sales_data.columns and 'Jumlah' in sales_data.columns:
            cost_price = 100  # Example cost price per item, replace with your actual logic
            sales_data['Keuntungan'] = sales_data['Total Harga'] - (sales_data['Jumlah'] * cost_price)

        st.dataframe(sales_data)
    else:
        st.warning("Data Penjualan tidak ditemukan.")

    # Calculate total sales and total profit for the report
    if not sales_data.empty:
        total_sales = sales_data['Total Harga'].sum()
        total_profit = sales_data['Keuntungan'].sum()

        # Display the report
        st.subheader("Laporan Penjualan")
        st.write(f"Total Penjualan: Rp {total_sales:,.0f}")
        st.write(f"Total Keuntungan: Rp {total_profit:,.0f}")
    else:
        st.warning("Data Penjualan tidak ditemukan untuk laporan.")

    # Display stock table
    if not stok_barang.empty:
        st.dataframe(stok_barang.drop(columns=['Harga']))  # Hide 'Harga' column

    # Ensure 'ID Barang' exists
    if 'ID Barang' not in stok_barang.columns:
        stok_barang['ID Barang'] = range(1, len(stok_barang) + 1)

    next_id = stok_barang['ID Barang'].max() + 1 if not stok_barang.empty else 1
    st.session_state.stok_barang = stok_barang

    # Refresh the stock data after modifications
    if 'stok_barang' in st.session_state:
        stok_barang = st.session_state.stok_barang

    st.subheader("Tambah Stok Barang")
    
    with st.form("stock_form"):
        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        ukuran_kemasan = st.text_input("Ukuran/Kemasan")
        jumlah = st.number_input("Jumlah", min_value=0)
        harga = st.number_input("Harga", min_value=0.0)
        harga_jual = st.number_input("Harga Jual", min_value=0.0)  # Manual input for selling price
        kode_warna_base = st.text_input("Kode Warna/Base (Opsional)")

        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            # Add new stock item
            new_stock = pd.DataFrame({
                'ID Barang': [next_id],
                'Nama Barang': [nama_barang],
                'Merk': [merk],
                'Ukuran/Kemasan': [ukuran_kemasan],
                'Jumlah': [jumlah],
                'Harga': [harga],
                'Harga Jual': [harga_jual],  # Manual input for selling price
                'Kode Warna/Base': [kode_warna_base],
                'Waktu Input': [datetime.now()]
            })
            st.session_state.stok_barang = pd.concat([stok_barang, new_stock], ignore_index=True)
            st.session_state.stok_barang.to_csv(stock_file_path, index=False)
            st.success("Stok barang berhasil ditambahkan.")

    # Edit stock section
    st.subheader("Edit Stok Barang")
    if not stok_barang.empty:
        id_edit = st.selectbox("Pilih ID Barang untuk di-edit", options=stok_barang['ID Barang'].tolist(), index=0)
        selected_item = stok_barang[stok_barang['ID Barang'] == id_edit].iloc[0]

        with st.form("edit_stock_form"):
            new_nama_barang = st.text_input("Nama Barang", value=selected_item['Nama Barang'])
            new_merk = st.text_input("Merk", value=selected_item['Merk'])
            new_ukuran_kemasan = st.text_input("Ukuran/Kemasan", value=selected_item['Ukuran/Kemasan'])
            new_jumlah = st.number_input("Jumlah", min_value=0, value=int(selected_item['Jumlah']))
            new_harga = st.number_input("Harga", min_value=0.0, value=selected_item['Harga'])
            new_harga_jual = st.number_input("Harga Jual", min_value=0.0, value=selected_item['Harga Jual'])  # Manual input for selling price
            new_kode_warna_base = st.text_input("Kode Warna/Base", value=selected_item.get('Kode Warna/Base', ''))

            edit_submitted = st.form_submit_button("Simpan Perubahan")

            if edit_submitted:
                # Update stock item
                stok_barang.loc[stok_barang['ID Barang'] == id_edit, 'Nama Barang'] = new_nama_barang
                stok_barang.loc[stok_barang['ID Barang'] == id_edit, 'Merk'] = new_merk
                stok_barang.loc[stok_barang['ID Barang'] == id_edit, 'Ukuran/Kemasan'] = new_ukuran_kemasan
                stok_barang.loc[stok_barang['ID Barang'] == id_edit, 'Jumlah'] = new_jumlah
                stok_barang.loc[stok_barang['ID Barang'] == id_edit, 'Harga'] = new_harga
                stok_barang.loc[stok_barang['ID Barang'] == id_edit, 'Harga Jual'] = new_harga_jual  # Manual input for selling price
                stok_barang.loc[stok_barang['ID Barang'] == id_edit, 'Kode Warna/Base'] = new_kode_warna_base

                # Save updated stock data to CSV
                stok_barang.to_csv(stock_file_path, index=False)
                st.success(f"Stok barang ID {id_edit} berhasil di-update.")
                st.session_state.stok_barang = stok_barang  # Update session state after editing

    # Add profit setting section
    st.subheader("Pengaturan Keuntungan Per Barang")
    if not stok_barang.empty:
        id_profit = st.selectbox("Pilih ID Barang untuk diatur persentase keuntungannya", options=stok_barang['ID Barang'].tolist(), index=0)
        selected_item_profit = stok_barang[stok_barang['ID Barang'] == id_profit].iloc[0]

        with st.form("profit_form"):
            persentase_keuntungan = st.number_input("Persentase Keuntungan (%)", min_value=0.0, max_value=100.0, value=15.0)  # Default to 15%

            profit_submitted = st.form_submit_button("Terapkan Keuntungan")

            if profit_submitted:
                # Update selling price (Harga Jual) based on the profit percentage
                harga_jual_baru = selected_item_profit['Harga'] + (selected_item_profit['Harga'] * (persentase_keuntungan / 100))
                stok_barang.loc[stok_barang['ID Barang'] == id_profit, 'Harga Jual'] = harga_jual_baru

                # Save updated stock data to CSV
                stok_barang.to_csv(stock_file_path, index=False)
                st.success(f"Persentase keuntungan sebesar {persentase_keuntungan}% berhasil diterapkan ke barang ID {id_profit}. Harga Jual diperbarui menjadi Rp {harga_jual_baru:,.0f}.")
                st.session_state.stok_barang = stok_barang

    # Add price setting section
    st.subheader("Pengaturan Harga Jual Per Barang")
    if not stok_barang.empty:
        id_price = st.selectbox("Pilih ID Barang untuk diatur Harga Jualnya", options=stok_barang['ID Barang'].tolist(), index=0)
        selected_item_price = stok_barang[stok_barang['ID Barang'] == id_price].iloc[0]

        with st.form("price_form"):
            new_harga_jual_manual = st.number_input("Harga Jual Baru", min_value=0.0, value=selected_item_price['Harga Jual'])  # Manual input for new selling price

            price_submitted = st.form_submit_button("Terapkan Harga Jual")

            if price_submitted:
                # Update selling price (Harga Jual) to the new manual value
                stok_barang.loc[stok_barang['ID Barang'] == id_price, 'Harga Jual'] = new_harga_jual_manual

                # Save updated stock data to CSV
                stok_barang.to_csv(stock_file_path, index=False)
                st.success(f"Harga Jual untuk barang ID {id_price} berhasil di-update menjadi Rp {new_harga_jual_manual:,.0f}.")
                st.session_state.stok_barang = stok_barang


    # Display all tables
    st.subheader("Manajemen Stok Barang")
    stock_file_path = get_user_file_paths(username).get('STOK_BARANG_FILE')
    if stock_file_path and os.path.exists(stock_file_path):
        stock_data = pd.read_csv(stock_file_path)
        st.dataframe(stock_data)
    else:
        st.warning("Data Stok Barang tidak ditemukan.")

    st.subheader("Manajemen Supplier")
    supplier_file_path = get_user_file_paths(username).get('SUPPLIER_FILE')
    if supplier_file_path and os.path.exists(supplier_file_path):
        supplier_data = pd.read_csv(supplier_file_path)
        st.dataframe(supplier_data)
    else:
        st.warning("Data Supplier tidak ditemukan.")

    st.subheader("Manajemen Piutang Konsumen")
    debt_file_path = get_user_file_paths(username).get('PIUTANG_FILE')
    if debt_file_path and os.path.exists(debt_file_path):
        debt_data = pd.read_csv(debt_file_path)
        st.dataframe(debt_data)
    else:
        st.warning("Data Piutang Konsumen tidak ditemukan.")

    st.subheader("Manajemen Pengeluaran")
    expense_file_path = get_user_file_paths(username).get('PENGELUARAN_FILE')
    if expense_file_path and os.path.exists(expense_file_path):
        expense_data = pd.read_csv(expense_file_path)
        st.dataframe(expense_data)
    else:
        st.warning("Data Pengeluaran tidak ditemukan.")

    # File paths
    file_paths = get_user_file_paths(username)
    stock_file_path = file_paths['STOK_BARANG_FILE']
    sales_file_path = file_paths['PENJUALAN_FILE']
    expenses_file_path = file_paths.get('EXPENSES_FILE', 'expenses.csv')
    profit_report_file_path = file_paths.get('PROFIT_REPORT_FILE', 'profit_report.csv')

    # Load stock data
    if os.path.exists(stock_file_path):
        stok_barang = pd.read_csv(stock_file_path)
    else:
        stok_barang = pd.DataFrame(columns=['ID Barang', 'Nama Barang', 'Merk', 'Ukuran/Kemasan', 'Jumlah', 'Harga', 'Harga Jual', 'Kode Warna/Base', 'Waktu Input'])

    # Load sales data
    if os.path.exists(sales_file_path):
        sales_data = pd.read_csv(sales_file_path)
    else:
        sales_data = pd.DataFrame(columns=['ID Penjualan', 'Nama Barang', 'Jumlah', 'Total Harga', 'Waktu Penjualan'])

    # Load expenses data
    if os.path.exists(expenses_file_path):
        expenses_data = pd.read_csv(expenses_file_path)
    else:
        expenses_data = pd.DataFrame(columns=['ID Pengeluaran', 'Keterangan', 'Jumlah', 'Waktu Pengeluaran'])

    st.subheader("Manajemen Penjualan")
    
    # Display the sales management table
    if not sales_data.empty:
        # Calculate Profit (Keuntungan)
        if 'Total Harga' in sales_data.columns and 'Jumlah' in sales_data.columns:
            cost_price = 100  # Example cost price per item, replace with your actual logic
            sales_data['Keuntungan'] = sales_data['Total Harga'] - (sales_data['Jumlah'] * cost_price)
        
        st.dataframe(sales_data)
    else:
        st.warning("Data Penjualan tidak ditemukan.")

    # Calculate total sales, total profit, and total expenses
    total_sales = sales_data['Total Harga'].sum() if not sales_data.empty else 0
    total_profit = sales_data['Keuntungan'].sum() if 'Keuntungan' in sales_data.columns else 0
    total_expenses = expenses_data['Jumlah'].sum() if not expenses_data.empty else 0

    # Calculate net profit
    net_profit = total_profit - total_expenses

    # Display the profit report
    st.subheader("Laporan Keuntungan Bersih")
    st.write(f"Total Penjualan: Rp {total_sales:,.0f}")
    st.write(f"Total Keuntungan: Rp {total_profit:,.0f}")
    st.write(f"Total Pengeluaran: Rp {total_expenses:,.0f}")
    st.write(f"Keuntungan Bersih: Rp {net_profit:,.0f}")

    # Add historical profit report
    current_month = datetime.now().strftime("%Y-%m")
    profit_report_data = pd.DataFrame(columns=['Bulan', 'Total Keuntungan', 'Total Pengeluaran', 'Keuntungan Bersih'])

    if os.path.exists(profit_report_file_path):
        profit_report_data = pd.read_csv(profit_report_file_path)

    # Check if the current month already exists in the report
    if current_month in profit_report_data['Bulan'].values:
        # Update existing entry
        profit_report_data.loc[profit_report_data['Bulan'] == current_month, 'Total Keuntungan'] = total_profit
        profit_report_data.loc[profit_report_data['Bulan'] == current_month, 'Total Pengeluaran'] = total_expenses
        profit_report_data.loc[profit_report_data['Bulan'] == current_month, 'Keuntungan Bersih'] = net_profit
    else:
        # Append new entry
        new_entry = pd.DataFrame({
            'Bulan': [current_month],
            'Total Keuntungan': [total_profit],
            'Total Pengeluaran': [total_expenses],
            'Keuntungan Bersih': [net_profit]
        })
        profit_report_data = pd.concat([profit_report_data, new_entry], ignore_index=True)

    # Save updated profit report to CSV
    profit_report_data.to_csv(profit_report_file_path, index=False)

    # Display the historical profit report
    st.subheader("Tabel Historis Keuntungan Bersih")
    st.dataframe(profit_report_data)
    
    # Function to download all data
    def download_all_data(username):
        file_paths = get_user_file_paths(username)
        with pd.ExcelWriter(f"{username}_all_data.xlsx", engine='openpyxl') as writer:
            for table_name, path in file_paths.items():
                if path and os.path.exists(path):
                    data = pd.read_csv(path)
                    sheet_name = table_name.split('_FILE')[0].replace('_', ' ').title()
                    data.to_excel(writer, sheet_name=sheet_name, index=False)
    
            # Add the historical profit report
            profit_report_data.to_excel(writer, sheet_name='Laporan Keuntungan Bersih', index=False)
    
        return f"{username}_all_data.xlsx"
    
    # Button to export all data
    if st.button("Export All Data"):
        excel_file_path = download_all_data(username)
        with open(excel_file_path, "rb") as f:
            st.download_button("Download All Data as Excel", f, file_name=excel_file_path, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    


            
# Main application function
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
        # Add a logout button
        if st.button("Keluar Aplikasi"):
            st.session_state.logged_in_user = None
            st.session_state.user_role = None
            st.success("You have been logged out.")
            st.experimental_rerun()

        # Horizontal Navigation Menu using option_menu
        selected = option_menu(
            menu_title=None,  # Hide the menu title
            options=["Manajemen Stok Barang", "Manajemen Penjualan", "Manajemen Supplier", 
                     "Manajemen Piutang Konsumen", "Manajemen Pengeluaran", "Laporan Keuangan"],
            icons=["box", "cart", "person", "credit-card", "cash", "bar-chart"],
            menu_icon="cast",  # Optional icon for the menu
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "02ab21"},
                "icon": {"color": "blue", "font-size": "25px"}, 
                "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "02ab21"},
            }
        )

        # Call appropriate function based on user selection
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
            update_historical_data(st.session_state.logged_in_user)

# In your main app, call the main function
if __name__ == "__main__":
    main()
