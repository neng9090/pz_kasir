import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Path to data files
STOK_BARANG_FILE = "stok_barang.csv"
PENJUALAN_FILE = "penjualan.csv"
SUPPLIER_FILE = "supplier.csv"
PENGELUARAN_FILE = "laporan_pengeluaran.csv"

# CSS styles for a professional look
st.markdown("""
    <style>
    .header-image {
        width: 100%;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        padding-top: 20px;
    }
    .sidebar .sidebar-content h2 {
        font-family: 'Arial', sans-serif;
        color: #333;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content .radio {
        margin-top: 10px;
    }
    .main-content {
        padding: 20px;
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        background-color: #28a745;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Display the header image
image_path = "/mnt/data/A_professional_dashboard_design_for_a_cashier_appl.png"
if os.path.exists(image_path):
    st.image(image_path, use_column_width=True, class_="header-image")
else:
    st.error("Gambar tidak ditemukan!")

# Load data from CSV files
def load_data():
    if os.path.exists(STOK_BARANG_FILE):
        st.session_state.stok_barang = pd.read_csv(STOK_BARANG_FILE, parse_dates=["Waktu Input"])
    else:
        st.session_state.stok_barang = pd.DataFrame(columns=[
            "ID", "Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Jumlah", "Persentase Keuntungan", "Waktu Input"
        ])

    if os.path.exists(PENJUALAN_FILE):
        st.session_state.penjualan = pd.read_csv(PENJUALAN_FILE, parse_dates=["Waktu"])
    else:
        st.session_state.penjualan = pd.DataFrame(columns=[
            "ID", "Nama Pelanggan", "Nomor Telepon", "Alamat", "Nama Barang", "Ukuran/Kemasan", "Merk", "Jumlah", "Total Harga", "Keuntungan", "Waktu"
        ])

    if os.path.exists(SUPPLIER_FILE):
        st.session_state.supplier = pd.read_csv(SUPPLIER_FILE, parse_dates=["Waktu"])
    else:
        st.session_state.supplier = pd.DataFrame(columns=[
            "ID", "Nama Barang", "Merk", "Ukuran/Kemasan", "Jumlah Barang", "Nama Supplier", "Tagihan", "Waktu"
        ])

# Save data to CSV files
def save_data():
    st.session_state.stok_barang.to_csv(STOK_BARANG_FILE, index=False)
    st.session_state.penjualan.to_csv(PENJUALAN_FILE, index=False)
    st.session_state.supplier.to_csv(SUPPLIER_FILE, index=False)

# Initialize data
if 'stok_barang' not in st.session_state:
    load_data()

# Sidebar menu
menu = st.sidebar.radio("Pilih Menu", ["Stock Barang", "Penjualan", "Supplier", "Owner"])

# Main content area
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Fungsi untuk menyimpan data secara otomatis
def save_data(df=None, filename='data_stock_barang.csv'):
    if df is not None:
        df.to_csv(filename, index=False)
        st.success(f"Data berhasil disimpan sebagai {filename}")
    else:
        st.info("Tidak ada data untuk disimpan.")

# Fungsi untuk halaman stok barang
def halaman_stock_barang():
    st.header("Stock Barang")
    
    # Cek apakah data stok barang sudah ada di session state
    if 'stok_barang' not in st.session_state:
        st.session_state.stok_barang = pd.DataFrame(columns=[
            "ID", "Nama Barang", "Merk", "Ukuran/Kemasan", 
            "Harga", "Jumlah", "Persentase Keuntungan", "Waktu Input"
        ])

    # Form input barang baru
    with st.form("input_barang"):
        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        ukuran = st.text_input("Ukuran/Kemasan")
        harga = st.number_input("Harga", min_value=0)
        jumlah = st.number_input("Jumlah", min_value=0)
        submit = st.form_submit_button("Tambah Barang")
        
        if submit:
            # Ambil data stok barang
            stok_barang = st.session_state.stok_barang
            
            # Cari apakah kombinasi Nama Barang, Merk, dan Ukuran/Kemasan sudah ada
            existing_item = stok_barang[
                (stok_barang['Nama Barang'] == nama_barang) & 
                (stok_barang['Merk'] == merk) & 
                (stok_barang['Ukuran/Kemasan'] == ukuran)
            ]
            
            if not existing_item.empty:
                # Jika barang sudah ada, update jumlah
                idx = existing_item.index[0]
                st.session_state.stok_barang.at[idx, 'Jumlah'] += jumlah
                st.success(f"Jumlah barang '{nama_barang}' berhasil ditambahkan!")
            else:
                # Jika barang belum ada, tambahkan data baru
                new_id = stok_barang["ID"].max() + 1 if not stok_barang.empty else 1
                new_data = pd.DataFrame({
                    "ID": [new_id],
                    "Nama Barang": [nama_barang],
                    "Merk": [merk],
                    "Ukuran/Kemasan": [ukuran],
                    "Harga": [harga],
                    "Jumlah": [jumlah],
                    "Persentase Keuntungan": [20],  # Nilai default (tidak ditampilkan di form)
                    "Waktu Input": [datetime.now()]  # Menambahkan waktu input barang
                })
                st.session_state.stok_barang = pd.concat([st.session_state.stok_barang, new_data], ignore_index=True)
                st.success("Barang baru berhasil ditambahkan!")
            
            save_data(st.session_state.stok_barang)  # Save data after adding new item

    # Tabel stok barang
    st.subheader("Daftar Stok Barang")
    df_stok_barang = st.session_state.stok_barang.copy()
    
    # Tampilkan kolom "Jumlah" dan hilangkan kolom lainnya jika diperlukan
    if "Jumlah" in df_stok_barang.columns:
        # Menghilangkan kolom "Persentase Keuntungan" jika ada
        if "Persentase Keuntungan" in df_stok_barang.columns:
            df_stok_barang = df_stok_barang.drop(columns=["Persentase Keuntungan"])
        
        # Menampilkan kolom yang relevan
        st.dataframe(df_stok_barang)
    else:
        st.info("Tidak ada data stok barang yang tersedia.")


# Fungsi untuk halaman Penjualan
def halaman_penjualan():
    st.header("Penjualan")
    
    with st.form("input_penjualan"):
        nama_pelanggan = st.text_input("Nama Pelanggan")
        nomor_telpon = st.text_input("Nomor Telepon")
        alamat = st.text_area("Alamat")
        nama_barang = st.selectbox("Pilih Barang", st.session_state.stok_barang["Nama Barang"])
        ukuran = st.selectbox("Ukuran/Kemasan", st.session_state.stok_barang["Ukuran/Kemasan"])
        merk = st.selectbox("Merk", st.session_state.stok_barang["Merk"])
        jumlah = st.number_input("Jumlah", min_value=1)
        submit = st.form_submit_button("Simpan Penjualan")
        
        if submit:
            harga_barang = st.session_state.stok_barang[
                (st.session_state.stok_barang["Nama Barang"] == nama_barang) &
                (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran)
            ]["Harga"].values[0]
            persentase_keuntungan = st.session_state.stok_barang[
                (st.session_state.stok_barang["Nama Barang"] == nama_barang) &
                (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran)
            ]["Persentase Keuntungan"].values[0]
            total_harga = harga_barang * jumlah
            keuntungan = total_harga * (persentase_keuntungan / 100)
            waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Mendapatkan waktu saat ini
            
            new_penjualan = pd.DataFrame({
                "ID": [st.session_state.penjualan["ID"].max() + 1 if not st.session_state.penjualan.empty else 1],
                "Nama Pelanggan": [nama_pelanggan],
                "Nomor Telepon": [nomor_telpon],
                "Alamat": [alamat],
                "Nama Barang": [nama_barang],
                "Ukuran/Kemasan": [ukuran],
                "Merk": [merk],
                "Jumlah": [jumlah],
                "Total Harga": [total_harga],
                "Keuntungan": [keuntungan],  # Menyimpan keuntungan
                "Waktu": [waktu]  # Menyimpan waktu penjualan
            })
            st.session_state.penjualan = pd.concat([st.session_state.penjualan, new_penjualan], ignore_index=True)
            
            # Update stok barang
            st.session_state.stok_barang.loc[
                (st.session_state.stok_barang["Nama Barang"] == nama_barang) &
                (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran),
                "Jumlah"
            ] -= jumlah
            
            st.success(f"Penjualan untuk {nama_pelanggan} berhasil disimpan!")
            save_data()  # Save data after sale


    # Tabel stok barang terupdate
    st.subheader("Stok Barang Terupdate")
    df_stok_barang = st.session_state.stok_barang.copy()
    if "Persentase Keuntungan" in df_stok_barang.columns:
        df_stok_barang = df_stok_barang.drop(columns=["Persentase Keuntungan"])  # Menghapus kolom Persentase Keuntungan jika ada
    st.dataframe(df_stok_barang)

    # Tombol pencarian stok barang
    search_barang = st.text_input("Cari Barang")
    if search_barang:
        hasil_pencarian = st.session_state.stok_barang[st.session_state.stok_barang["Nama Barang"].str.contains(search_barang, case=False)]
        st.write("Hasil Pencarian:")
        if "Persentase Keuntungan" in hasil_pencarian.columns:
            hasil_pencarian = hasil_pencarian.drop(columns=["Persentase Keuntungan"])  # Menghapus kolom Persentase Keuntungan jika ada
        st.dataframe(hasil_pencarian)

    # Tombol untuk mendownload laporan penjualan
    if st.button("Download Laporan Penjualan (CSV)"):
        csv = st.session_state.penjualan.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name="laporan_penjualan.csv", mime="text/csv")

    # Tombol untuk print struk
    if st.button("Print Struk Terakhir"):
        from io import StringIO
        struk = StringIO()
        struk.write("=== STRUK PENJUALAN ===\n")
        for idx, row in st.session_state.penjualan.tail(1).iterrows():
            struk.write(f"Nama Pelanggan: {row['Nama Pelanggan']}\n")
            struk.write(f"Nomor Telepon: {row['Nomor Telepon']}\n")
            struk.write(f"Alamat: {row['Alamat']}\n")
            struk.write(f"Nama Barang: {row['Nama Barang']}\n")
            struk.write(f"Ukuran/Kemasan: {row['Ukuran/Kemasan']}\n")
            struk.write(f"Merk: {row['Merk']}\n")
            struk.write(f"Jumlah: {row['Jumlah']}\n")
            struk.write(f"Total Harga: {row['Total Harga']}\n")
            struk.write(f"Waktu: {row['Waktu']}\n")
        struk.write("=========================\n")
        
        # Tulis ke file dan simpan untuk print
        with open('struk_pembelian.txt', 'w') as f:
            f.write(struk.getvalue())
        
        st.success("Struk berhasil dicetak!")
    
    import io

    # Tombol untuk mendownload struk pembelian
    if st.button("Download Struk Terakhir (TXT)"):
        struk = io.StringIO()
        struk.write("=== STRUK PENJUALAN ===\n")
        for idx, row in st.session_state.penjualan.tail(1).iterrows():
            struk.write(f"Nama Pelanggan: {row['Nama Pelanggan']}\n")
            struk.write(f"Nomor Telepon: {row['Nomor Telepon']}\n")
            struk.write(f"Alamat: {row['Alamat']}\n")
            struk.write(f"Nama Barang: {row['Nama Barang']}\n")
            struk.write(f"Ukuran/Kemasan: {row['Ukuran/Kemasan']}\n")
            struk.write(f"Merk: {row['Merk']}\n")
            struk.write(f"Jumlah: {row['Jumlah']}\n")
            struk.write(f"Total Harga: {row['Total Harga']}\n")
            struk.write(f"Waktu: {row['Waktu']}\n")
        struk.write("=========================\n")
        
        # Menggunakan tombol download dari Streamlit
        st.download_button(
            label="Download TXT",
            data=struk.getvalue(),
            file_name="struk_pembelian.txt",
            mime="text/plain"
        )

import pandas as pd
import streamlit as st
from datetime import datetime

# Fungsi untuk menyimpan data secara otomatis
def save_data(df=None, filename='data_supplier.csv'):
    if df is not None:
        df.to_csv(filename, index=False)
        st.success(f"Data berhasil disimpan sebagai {filename}")
    else:
        st.info("Tidak ada data untuk disimpan.")

# Fungsi untuk menggabungkan jumlah barang jika ada duplikat
def merge_supplier_data(df):
    return df.groupby(["ID", "Nama Barang", "Merk", "Ukuran/Kemasan", "Nama Supplier", "Tagihan", "Waktu"], as_index=False).agg({
        "Jumlah Barang": "sum"
    })

# Fungsi untuk halaman supplier
def halaman_supplier():
    st.header("Data Supplier")

    # Cek apakah data supplier sudah ada di session state
    if 'supplier' not in st.session_state:
        st.session_state.supplier = pd.DataFrame(columns=[
            "ID", "Nama Barang", "Merk", "Ukuran/Kemasan", 
            "Jumlah Barang", "Nama Supplier", "Tagihan", "Waktu"
        ])

    # Form untuk menambahkan data supplier baru
    with st.form("input_supplier"):
        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        ukuran = st.text_input("Ukuran/Kemasan")
        jumlah_barang = st.number_input("Jumlah Barang", min_value=0)
        nama_supplier = st.text_input("Nama Supplier")
        tagihan = st.number_input("Tagihan", min_value=0)
        submit = st.form_submit_button("Tambah Data Supplier")
        
        if submit:
            new_id = st.session_state.supplier["ID"].max() + 1 if not st.session_state.supplier.empty else 1
            new_data = pd.DataFrame({
                "ID": [new_id],
                "Nama Barang": [nama_barang],
                "Merk": [merk],
                "Ukuran/Kemasan": [ukuran],
                "Jumlah Barang": [jumlah_barang],
                "Nama Supplier": [nama_supplier],
                "Tagihan": [tagihan],
                "Waktu": [datetime.now()]  # Menambahkan waktu input data supplier
            })
            st.session_state.supplier = pd.concat([st.session_state.supplier, new_data], ignore_index=True)
            st.session_state.supplier = merge_supplier_data(st.session_state.supplier)  # Merge data to handle duplicates
            st.success("Data supplier berhasil ditambahkan!")
            save_data(st.session_state.supplier)  # Save data after adding supplier data

    # Menampilkan tabel data supplier
    st.subheader("Tabel Data Supplier")
    supplier_data = st.session_state.supplier.copy()

    # Edit dan hapus data
    if not supplier_data.empty:
        # Pilih ID untuk edit atau hapus
        selected_id = st.selectbox("Pilih ID Supplier", supplier_data["ID"])
        selected_data = supplier_data[supplier_data["ID"] == selected_id]

        if not selected_data.empty:
            with st.expander("Edit Data Supplier"):
                with st.form("edit_supplier"):
                    new_nama_barang = st.text_input("Nama Barang", value=selected_data["Nama Barang"].values[0])
                    new_merk = st.text_input("Merk", value=selected_data["Merk"].values[0])
                    new_ukuran = st.text_input("Ukuran/Kemasan", value=selected_data["Ukuran/Kemasan"].values[0])
                    new_jumlah_barang = st.number_input("Jumlah Barang", value=selected_data["Jumlah Barang"].values[0])
                    new_nama_supplier = st.text_input("Nama Supplier", value=selected_data["Nama Supplier"].values[0])
                    new_tagihan = st.number_input("Tagihan", value=selected_data["Tagihan"].values[0])
                    submit_edit = st.form_submit_button("Simpan Perubahan")
                    
                    if submit_edit:
                        st.session_state.supplier.loc[
                            st.session_state.supplier["ID"] == selected_id, 
                            ["Nama Barang", "Merk", "Ukuran/Kemasan", "Jumlah Barang", "Nama Supplier", "Tagihan"]
                        ] = [new_nama_barang, new_merk, new_ukuran, new_jumlah_barang, new_nama_supplier, new_tagihan]
                        st.session_state.supplier = merge_supplier_data(st.session_state.supplier)  # Merge data to handle duplicates
                        st.success("Data supplier berhasil diperbarui!")
                        save_data(st.session_state.supplier)  # Save data after editing supplier data

            with st.expander("Hapus Data Supplier"):
                if st.button("Hapus Data Supplier"):
                    st.session_state.supplier = st.session_state.supplier[st.session_state.supplier["ID"] != selected_id]
                    st.success("Data supplier berhasil dihapus!")
                    save_data(st.session_state.supplier)  # Save data after deleting supplier data

    # Menampilkan tabel data supplier
    st.subheader("Daftar Data Supplier")
    st.dataframe(st.session_state.supplier)


# Initialize session state if not already
if 'stok_barang' not in st.session_state:
    st.session_state.stok_barang = pd.DataFrame(columns=["ID", "Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Jumlah", "Persentase Keuntungan"])

if 'penjualan' not in st.session_state:
    st.session_state.penjualan = pd.DataFrame(columns=["ID", "Nama Pelanggan", "Nama Barang", "Jumlah", "Total Harga", "Keuntungan", "Waktu"])

if 'supplier' not in st.session_state:
    st.session_state.supplier = pd.DataFrame(columns=["ID", "Nama Barang", "Merk", "Ukuran/Kemasan", "Jumlah", "Nama Supplier", "Tagihan", "Waktu"])

if 'laporan_pengeluaran' not in st.session_state:
    st.session_state.laporan_pengeluaran = pd.DataFrame(columns=["Gaji Karyawan", "Biaya Operasional", "Biaya Lainnya", "Total Pengeluaran", "Bulan"])

import pandas as pd
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt

# Fungsi untuk menyimpan data secara otomatis
def save_data():
    # Implementasikan penyimpanan data jika diperlukan
    pass

def auto_save():
    if 'data_saved' not in st.session_state:
        st.session_state.data_saved = {
            'stok_barang': pd.DataFrame(),
            'supplier': pd.DataFrame(),
            'Total Pengeluaran': pd.DataFrame(),
            'penjualan': pd.DataFrame()
        }
    st.session_state.data_saved['stok_barang'] = st.session_state.stok_barang
    st.session_state.data_saved['supplier'] = st.session_state.supplier
    st.session_state.data_saved['penjualan'] = st.session_state.penjualan

def halaman_owner():
    st.header("Halaman Owner - Analisa Keuangan")

    # Login form
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.form("login_form"):
            password = st.text_input("Masukkan Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit and password == "password123":  # Ganti dengan password yang Anda inginkan
                st.session_state.authenticated = True
                st.success("Login berhasil!")
            elif submit:
                st.error("Password salah!")
        return

    # Tabel stok barang dengan fitur edit dan hapus
    st.subheader("Stok Barang")
    df_stok_barang = st.session_state.stok_barang.drop(columns=["Stok"], errors='ignore')  # Menghilangkan kolom "Stok" jika ada
    st.dataframe(df_stok_barang)
    
    if not st.session_state.stok_barang.empty:
        selected_row = st.selectbox("Pilih ID Barang untuk Diedit", st.session_state.stok_barang["ID"])

        with st.form("edit_barang"):
            barang_dipilih = st.session_state.stok_barang[st.session_state.stok_barang["ID"] == selected_row]
            nama_barang = st.text_input("Nama Barang", value=barang_dipilih["Nama Barang"].values[0])
            merk = st.text_input("Merk", value=barang_dipilih["Merk"].values[0])
            ukuran = st.text_input("Ukuran/Kemasan", value=barang_dipilih["Ukuran/Kemasan"].values[0])
            harga = st.number_input("Harga", min_value=0, value=int(barang_dipilih["Harga"].values[0]))
            jumlah = st.number_input("Jumlah", min_value=0, value=int(barang_dipilih["Jumlah"].values[0]))
            persentase_keuntungan = st.number_input("Persentase Keuntungan (%)", min_value=0, max_value=100, value=int(barang_dipilih["Persentase Keuntungan"].values[0]))
            submit = st.form_submit_button("Update Barang")
            
            if submit:
                st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"] == selected_row, ["Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Jumlah", "Persentase Keuntungan"]] = [nama_barang, merk, ukuran, harga, jumlah, persentase_keuntungan]
                st.success("Barang berhasil diupdate!")
                save_data()  # Save data after updating item
        
        # Tombol untuk hapus barang
        if st.button("Hapus Barang"):
            confirm = st.radio("Apakah Anda yakin ingin menghapus barang ini?", ["Ya", "Tidak"])
            if confirm == "Ya":
                st.session_state.stok_barang = st.session_state.stok_barang[st.session_state.stok_barang["ID"] != selected_row]
                st.success("Barang berhasil dihapus!")
                save_data()  # Save data after deleting item

    # Tabel Laporan Penjualan dengan fitur edit dan hapus
    st.subheader("Laporan Penjualan")
    st.dataframe(st.session_state.penjualan)

    if not st.session_state.penjualan.empty:
        selected_penjualan_row = st.selectbox("Pilih ID Penjualan untuk Diedit", st.session_state.penjualan["ID"])

        with st.form("edit_penjualan"):
            penjualan_dipilih = st.session_state.penjualan[st.session_state.penjualan["ID"] == selected_penjualan_row]
            nama_pelanggan = st.text_input("Nama Pelanggan", value=penjualan_dipilih["Nama Pelanggan"].values[0])
            nama_barang = st.text_input("Nama Barang", value=penjualan_dipilih["Nama Barang"].values[0])
            jumlah = st.number_input("Jumlah", min_value=1, value=int(penjualan_dipilih["Jumlah"].values[0]))
            total_harga = st.number_input("Total Harga", min_value=0, value=int(penjualan_dipilih["Total Harga"].values[0]))
            keuntungan = st.number_input("Keuntungan", min_value=0, value=int(penjualan_dipilih["Keuntungan"].values[0]))
            submit_penjualan = st.form_submit_button("Update Penjualan")
            
            if submit_penjualan:
                if nama_pelanggan and nama_barang:  # Validasi input
                    st.session_state.penjualan.loc[st.session_state.penjualan["ID"] == selected_penjualan_row, 
                                                   ["Nama Pelanggan", "Nama Barang", "Jumlah", "Total Harga", "Keuntungan"]] = [nama_pelanggan, nama_barang, jumlah, total_harga, keuntungan]
                    st.success("Penjualan berhasil diupdate!")
                    save_data()  # Save data after updating item
                else:
                    st.error("Mohon lengkapi semua field!")

        # Tombol untuk hapus penjualan dengan konfirmasi
        if st.button("Hapus Penjualan"):
            confirm = st.radio("Apakah Anda yakin ingin menghapus data penjualan ini?", ["Ya", "Tidak"])
            if confirm == "Ya":
                st.session_state.penjualan = st.session_state.penjualan[st.session_state.penjualan["ID"] != selected_penjualan_row]
                st.success("Penjualan berhasil dihapus!")
                save_data()  # Save data after deleting item
        else:
            st.info("Tidak ada data penjualan untuk diedit atau dihapus.")

    # Fungsi untuk menyimpan data
    def save_data(df=None, filename='data_supplier.csv'):
        if df is not None:
            if df.empty and os.path.exists(filename):
                os.remove(filename)  # Hapus file jika DataFrame kosong
            else:
                df.to_csv(filename, index=False)
            st.success(f"Data berhasil disimpan sebagai {filename}")
        else:
            st.info("Tidak ada data untuk disimpan.")

    # Fungsi untuk halaman supplier
    def halaman_supplier():
        st.header("Data Supplier")
        
        # Cek apakah data supplier sudah ada di session state
        if 'supplier' not in st.session_state:
            if os.path.exists('data_supplier.csv'):
                st.session_state.supplier = pd.read_csv('data_supplier.csv')
            else:
                st.session_state.supplier = pd.DataFrame(columns=[
                    "ID", "Nama Barang", "Merk", "Ukuran/Kemasan", 
                    "Jumlah Barang", "Nama Supplier", "Tagihan", "Waktu"
                ])
        
        # Form untuk menambahkan data supplier baru
        with st.form("input_supplier"):
            nama_barang = st.text_input("Nama Barang")
            merk = st.text_input("Merk")
            ukuran = st.text_input("Ukuran/Kemasan")
            jumlah_barang = st.number_input("Jumlah Barang", min_value=0)
            nama_supplier = st.text_input("Nama Supplier")
            tagihan = st.number_input("Tagihan", min_value=0)
            submit = st.form_submit_button("Tambah Data Supplier")
            
            if submit:
                new_id = st.session_state.supplier["ID"].max() + 1 if not st.session_state.supplier.empty else 1
                new_data = pd.DataFrame({
                    "ID": [new_id],
                    "Nama Barang": [nama_barang],
                    "Merk": [merk],
                    "Ukuran/Kemasan": [ukuran],
                    "Jumlah Barang": [jumlah_barang],
                    "Nama Supplier": [nama_supplier],
                    "Tagihan": [tagihan],
                    "Waktu": [datetime.now()]  # Menambahkan waktu input data supplier
                })
                st.session_state.supplier = pd.concat([st.session_state.supplier, new_data], ignore_index=True)
                st.success("Data supplier berhasil ditambahkan!")
                save_data(st.session_state.supplier)  # Save data after adding supplier data

        # Button to clear all supplier data
        if st.button("Hapus Semua Data Supplier"):
            if st.session_state.supplier.empty:
                st.info("Tidak ada data supplier untuk dihapus.")
            else:
                confirm = st.radio("Apakah Anda yakin ingin menghapus semua data supplier?", ["Ya", "Tidak"])
                if confirm == "Ya":
                    st.session_state.supplier = pd.DataFrame(columns=[
                        "ID", "Nama Barang", "Merk", "Ukuran/Kemasan", 
                        "Jumlah Barang", "Nama Supplier", "Tagihan", "Waktu"
                    ])
                    save_data(st.session_state.supplier)  # Save after clearing data
                    st.success("Semua data supplier telah dihapus.")
        
        # Edit Supplier Data
        st.subheader("Edit Data Supplier")
        if not st.session_state.supplier.empty:
            supplier_id = st.selectbox("Pilih ID Supplier untuk Diedit", st.session_state.supplier["ID"])
            
            supplier_data = st.session_state.supplier[st.session_state.supplier["ID"] == supplier_id]
            
            if not supplier_data.empty:
                with st.form("edit_supplier"):
                    nama_barang = st.text_input("Nama Barang", value=supplier_data["Nama Barang"].values[0])
                    merk = st.text_input("Merk", value=supplier_data["Merk"].values[0])
                    ukuran = st.text_input("Ukuran/Kemasan", value=supplier_data["Ukuran/Kemasan"].values[0])
                    jumlah_barang = st.number_input("Jumlah Barang", value=supplier_data["Jumlah Barang"].values[0])
                    nama_supplier = st.text_input("Nama Supplier", value=supplier_data["Nama Supplier"].values[0])
                    tagihan = st.number_input("Tagihan", value=supplier_data["Tagihan"].values[0])
                    submit_edit = st.form_submit_button("Simpan Perubahan")
                    
                    if submit_edit:
                        st.session_state.supplier.loc[
                            st.session_state.supplier["ID"] == supplier_id, ["Nama Barang", "Merk", "Ukuran/Kemasan", "Jumlah Barang", "Nama Supplier", "Tagihan"]
                        ] = [nama_barang, merk, ukuran, jumlah_barang, nama_supplier, tagihan]
                        st.success("Data supplier berhasil diperbarui!")
                        save_data(st.session_state.supplier)  # Save data after editing supplier data
        else:
            st.warning("Tidak ada data supplier untuk diedit.")
        
        # Tabel data supplier
        st.subheader("Daftar Data Supplier")
        # Menghilangkan kolom "Jumlah Barang" dari tampilan
        df_to_display = st.session_state.supplier.drop(columns=["Jumlah Barang"], errors='ignore')
        st.dataframe(df_to_display)

    # Analisa keuangan
    st.subheader("Analisa Keuangan")
    total_penjualan = st.session_state.penjualan["Total Harga"].sum()
    st.write(f"Total Penjualan: Rp {total_penjualan}")
    
    total_keuntungan = st.session_state.penjualan["Keuntungan"].sum()
    st.write(f"Total Keuntungan: Rp {total_keuntungan}")

    # Input pengeluaran bulanan
    st.subheader("Pengeluaran Per Bulan")
    with st.form("pengeluaran_bulanan"):
        gaji_karyawan = st.number_input("Gaji Karyawan", min_value=0, value=0)
        biaya_operasional = st.number_input("Biaya Operasional", min_value=0, value=0)
        biaya_lainnya = st.number_input("Biaya Lainnya", min_value=0, value=0)
        submit = st.form_submit_button("Simpan Pengeluaran")
        
        if submit:
            total_pengeluaran = gaji_karyawan + biaya_operasional + biaya_lainnya
            st.write(f"Total Pengeluaran Bulanan: Rp {total_pengeluaran}")

            # Simpan data pengeluaran ke dalam session state
            new_pengeluaran = pd.DataFrame({
                "Gaji Karyawan": [gaji_karyawan],
                "Biaya Operasional": [biaya_operasional],
                "Biaya Lainnya": [biaya_lainnya],
                "Total Pengeluaran": [total_pengeluaran],
                "Bulan": [datetime.now().strftime("%Y-%m")]
            })

            if "laporan_pengeluaran" in st.session_state:
                st.session_state.laporan_pengeluaran = pd.concat([st.session_state.laporan_pengeluaran, new_pengeluaran], ignore_index=True)
            else:
                st.session_state.laporan_pengeluaran = new_pengeluaran
            save_data()  # Fungsi untuk menyimpan data

    # Menampilkan Total Pengeluaran
    if "laporan_pengeluaran" in st.session_state:
        total_pengeluaran_all = st.session_state.laporan_pengeluaran["Total Pengeluaran"].sum()
    else:
        total_pengeluaran_all = 0
    st.write(f"Total Pengeluaran: Rp {total_pengeluaran_all}")
    save_data() 

    # Hitung total keuntungan
    if "penjualan" in st.session_state:
        total_keuntungan = st.session_state.penjualan["Keuntungan"].sum()
    else:
        total_keuntungan = 0
    st.write(f"Total Keuntungan: Rp {total_keuntungan}")

    # Perhitungan keuntungan bersih
    keuntungan_bersih = total_keuntungan - total_pengeluaran_all
    st.write(f"Keuntungan Bersih: Rp {keuntungan_bersih}")

    

    # Grafik Penjualan Bulanan
    st.subheader("Grafik Penjualan")
    if "penjualan" in st.session_state and not st.session_state.penjualan.empty:
        sales_data = st.session_state.penjualan.groupby(st.session_state.penjualan["Waktu"].dt.to_period("M")).agg({"Total Harga": "sum"}).reset_index()
        sales_data["Waktu"] = sales_data["Waktu"].astype(str)

        fig, ax = plt.subplots()
        ax.bar(sales_data["Waktu"], sales_data["Total Harga"], color='skyblue')
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Total Penjualan")
        ax.set_title("Grafik Penjualan Bulanan")
        st.pyplot(fig)
    else:
        st.info("Belum ada data penjualan untuk ditampilkan.")

    # Grafik Keuntungan Harian
    st.subheader("Grafik Keuntungan Harian")
    if "penjualan" in st.session_state and not st.session_state.penjualan.empty:
        # Kelompokkan data berdasarkan hari
        profit_data = st.session_state.penjualan.groupby(st.session_state.penjualan["Waktu"].dt.to_period("D")).agg({"Keuntungan": "sum"}).reset_index()
        profit_data["Waktu"] = profit_data["Waktu"].astype(str)

        # Plotting the graph
        fig, ax = plt.subplots()
        ax.plot(profit_data["Waktu"], profit_data["Keuntungan"], marker='o', color='lightgreen')
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Total Keuntungan")
        ax.set_title("Grafik Keuntungan Harian")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("Belum ada data keuntungan untuk ditampilkan.")

    # Grafik pemasaran berdasarkan keuntungan per produk
    st.subheader("Grafik Pemasaran")
    keuntungan_per_barang = st.session_state.penjualan.groupby("Nama Barang")["Keuntungan"].sum().reset_index()

    # Plotting the graph
    fig, ax = plt.subplots()
    ax.bar(keuntungan_per_barang["Nama Barang"], keuntungan_per_barang["Keuntungan"], color='skyblue')
    ax.set_xlabel("Nama Barang")
    ax.set_ylabel("Keuntungan (Rp)")
    ax.set_title("Keuntungan per Produk")
    st.pyplot(fig)

    st.header("Audit Stok Barang")

    # Cek apakah data sudah tersedia
    required_data = ['stok_barang', 'penjualan', 'supplier']
    if not all(hasattr(st.session_state, key) for key in required_data):
        st.warning("Data Stok Barang, Penjualan, atau Supplier belum tersedia.")
        st.stop()

    # Ambil data dari session state
    stok_barang = st.session_state.stok_barang
    penjualan = st.session_state.penjualan
    supplier = st.session_state.supplier

    # Periksa apakah data supplier ada
    if supplier.empty:
        st.warning("Data supplier tidak tersedia.")
        st.stop()

    # Gabungkan data stok barang
    audit_df = stok_barang[['ID', 'Nama Barang', 'Merk', 'Ukuran/Kemasan', 'Jumlah']].copy()

    # Menggabungkan dengan data penjualan
    penjualan_sum = penjualan.groupby(['Nama Barang', 'Ukuran/Kemasan'], as_index=False)['Jumlah'].sum()
    audit_df = pd.merge(audit_df, penjualan_sum, on=['Nama Barang', 'Ukuran/Kemasan'], how='left')
    audit_df.rename(columns={'Jumlah_x': 'Jumlah Stok', 'Jumlah_y': 'Jumlah Penjualan'}, inplace=True)
    audit_df['Jumlah Penjualan'].fillna(0, inplace=True)

    # Menggabungkan dengan data supplier
    supplier_sum = supplier.groupby(['Nama Barang', 'Ukuran/Kemasan'], as_index=False)['Jumlah Barang'].sum()
    audit_df = pd.merge(audit_df, supplier_sum, on=['Nama Barang', 'Ukuran/Kemasan'], how='left')
    audit_df.rename(columns={'Jumlah Barang': 'Jumlah Barang'}, inplace=True)
    audit_df['Jumlah Barang'].fillna(0, inplace=True)

    # Menambahkan kolom keterangan
    audit_df['Keterangan'] = audit_df.apply(
        lambda row: 'Aman' if (row['Jumlah Stok'] - row['Jumlah Penjualan']) == row['Jumlah Barang'] else 'Data Tidak Sesuai', axis=1
    )

    # Tampilkan audit_df untuk debugging
    st.write(audit_df)

    # Notifikasi status stok
    st.subheader("Notifikasi Status Stok")
    if not audit_df.empty:
        for idx, row in audit_df.iterrows():
            if (row['Jumlah Stok'] - row['Jumlah Penjualan']) == row['Jumlah Barang']:
                st.success(f"Stok untuk '{row['Nama Barang']}' aman.")
            else:
                st.warning(f"Stok untuk '{row['Nama Barang']}' harus di-audit. Stok tidak sesuai dengan jumlah barang.")
    else:
        st.warning("Audit Data Kosong.")

# Auto-save functionality to prevent data loss
    save_data()

    # Fungsi untuk menyimpan data secara otomatis
    def auto_save():
        if 'data_saved' not in st.session_state:
            st.session_state.data_saved = {
                'stok_barang': pd.DataFrame(),
                'supplier': pd.DataFrame(),
                'Total Pengeluaran': pd.DataFrame(),
                'penjualan': pd.DataFrame()
            }
        st.session_state.data_saved['stok_barang'] = st.session_state.stok_barang
        st.session_state.data_saved['supplier'] = st.session_state.supplier
        st.session_state.data_saved['penjualan'] = st.session_state.penjualan

# Menampilkan halaman berdasarkan menu yang dipilih
if menu == "Stock Barang":
    halaman_stock_barang()
elif menu == "Penjualan":
    halaman_penjualan()
elif menu == "Supplier":
    halaman_supplier()
elif menu == "Owner":
    halaman_owner()
# Button to exit
if st.button("Keluar"):
    st.write("Silakan tutup tab atau jendela aplikasi untuk keluar.")

st.markdown('</div>', unsafe_allow_html=True)

# Save data when the app is closed or the menu is changed
save_data()

