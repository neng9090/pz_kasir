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
        'HISTORIS_KEUNTUNGAN_FILE': f'{username}_historis_keuntungan_bersih.csv'
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

# Initialize new users if user_data.csv does not exist or is empty
def initialize_users():
    new_users = pd.DataFrame({
        "Username": ["mira", "yono", "tini"],
        "Password": ["123oke", "456", "789"],
        "Role": ["user", "user", "user"]
    })
    new_users.to_csv(USER_DATA_FILE, index=False)

def save_data(df, file_path):
    try:
        df.to_csv(file_path, index=False)
    except Exception as e:
        st.error(f"Error saving data: {e}")

def export_data_to_excel(dataframes, file_path):
    try:
        with pd.ExcelWriter(file_path) as writer:
            for name, df in dataframes.items():
                df.to_excel(writer, sheet_name=name, index=False)
        st.success("Data successfully exported to Excel!")
    except Exception as e:
        st.error(f"Error exporting data: {e}")

def update_historical_data(username):
    st.title("Laporan Keuangan")
    file_path = get_user_file_paths(username)['HISTORIS_KEUANGAN_FILE']
    
    if os.path.exists(file_path):
        st.session_state.historical_data = pd.read_csv(file_path)
    else:
        st.session_state.historical_data = pd.DataFrame(columns=['Tanggal', 'Total Pemasukan', 'Total Pengeluaran'])

    if 'historical_data' in st.session_state:
        st.dataframe(st.session_state.historical_data)
        
        total_income = st.session_state.historical_data['Total Pemasukan'].sum()
        total_expenses = st.session_state.historical_data['Total Pengeluaran'].sum()
        
        st.subheader("Total Keuangan")
        st.write(f"Total Pemasukan: {total_income}")
        st.write(f"Total Pengeluaran: {total_expenses}")
        st.write(f"Sisa: {total_income - total_expenses}")

    st.subheader("Tambah Data Keuangan")
    
    with st.form("financial_form"):
        tanggal = st.date_input("Tanggal", value=datetime.now())
        total_pemasukan = st.number_input("Total Pemasukan", min_value=0.0, format="%.2f")
        total_pengeluaran = st.number_input("Total Pengeluaran", min_value=0.0, format="%.2f")
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_financial_data = pd.DataFrame({
                'Tanggal': [tanggal],
                'Total Pemasukan': [total_pemasukan],
                'Total Pengeluaran': [total_pengeluaran]
            })
            
            st.session_state.historical_data = pd.concat([st.session_state.historical_data, new_financial_data], ignore_index=True)
            save_data(st.session_state.historical_data, file_path)
            st.success("Data keuangan berhasil diperbarui.")

def manage_stok_barang(username):
    st.header("Pengelolaan Stok Barang")
    stok_file_path = get_user_file_paths(username)['STOK_BARANG_FILE']
    
    if os.path.exists(stok_file_path):
        st.session_state.stok_barang = pd.read_csv(stok_file_path)
    else:
        st.session_state.stok_barang = pd.DataFrame(columns=["ID", "Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Stok", "Persentase Keuntungan", "Kode Warna"])

    barang_ids = st.session_state.stok_barang["ID"].tolist()
    barang_ids.insert(0, "Tambah Baru")
    selected_row = st.selectbox("Pilih ID Barang untuk Diedit atau Tambah Baru", barang_ids)
    
    if selected_row == "Tambah Baru":
        barang_dipilih = None
        default_values = {key: "" for key in ["Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Stok", "Persentase Keuntungan", "Kode Warna"]}
        default_values["Harga"] = 0
        default_values["Stok"] = 0
        default_values["Persentase Keuntungan"] = 0
    else:
        barang_dipilih = st.session_state.stok_barang[st.session_state.stok_barang["ID"] == selected_row].iloc[0]
        default_values = barang_dipilih.to_dict()

    with st.form("edit_barang"):
        nama_barang = st.text_input("Nama Barang", value=default_values["Nama Barang"])
        merk = st.text_input("Merk", value=default_values["Merk"])
        ukuran = st.text_input("Ukuran/Kemasan", value=default_values["Ukuran/Kemasan"])
        harga = st.number_input("Harga", min_value=0.0, value=float(default_values["Harga"]), format="%.2f")
        stok = st.number_input("Stok Barang", min_value=0, value=int(default_values["Stok"]))
        persentase_keuntungan = st.number_input("Persentase Keuntungan (%)", min_value=0, max_value=100, value=int(default_values["Persentase Keuntungan"]))
        kode_warna = st.text_input("Kode Warna/Base", value=default_values["Kode Warna"], placeholder="Opsional")
        
        selling_price = harga * (1 + (persentase_keuntungan / 100))
        submit = st.form_submit_button("Simpan Barang")
    
        if submit:
            if barang_dipilih is None:
                new_id = st.session_state.stok_barang["ID"].max() + 1 if not st.session_state.stok_barang.empty else 1
                new_data = pd.DataFrame({
                    "ID": [new_id],
                    "Nama Barang": [nama_barang],
                    "Merk": [merk],
                    "Ukuran/Kemasan": [ukuran],
                    "Harga": [harga],
                    "Stok": [stok],
                    "Persentase Keuntungan": [persentase_keuntungan],
                    "Kode Warna": [kode_warna],
                    "Harga Jual": [selling_price],
                    "Waktu Input": [datetime.now()]
                })
                st.session_state.stok_barang = pd.concat([st.session_state.stok_barang, new_data], ignore_index=True)
                st.success("Barang baru berhasil ditambahkan!")
            else:
                st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"] == selected_row, 
                    ["Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Stok", "Persentase Keuntungan", "Kode Warna", "Harga Jual"]] = \
                    [nama_barang, merk, ukuran, harga, stok, persentase_keuntungan, kode_warna, selling_price]
                st.success(f"Barang ID {selected_row} berhasil diupdate!")
            
            save_data(st.session_state.stok_barang, stok_file_path)

    st.subheader("Daftar Stok Barang")
    df_stok_barang = st.session_state.stok_barang.copy()
    
    search_text = st.text_input("Cari Nama Barang atau Merk", key='search_text')
    if search_text:
        df_stok_barang = df_stok_barang[
            (df_stok_barang["Nama Barang"].str.contains(search_text, case=False, na=False)) |
            (df_stok_barang["Merk"].str.contains(search_text, case=False, na=False))
        ]
    
    st.dataframe(df_stok_barang)
    
    if selected_row != "Tambah Baru" and st.button("Hapus Barang"):
        st.session_state.stok_barang = st.session_state.stok_barang[st.session_state.stok_barang["ID"] != selected_row]
        st.success(f"Barang ID {selected_row} berhasil dihapus!")
        save_data(st.session_state.stok_barang, stok_file_path)

    if st.button("Ekspor Semua Data ke Excel"):
        export_file_path = get_user_file_paths(username)['EXPORT_FILE']
        dataframes = {
            'Historis Keuangan': st.session_state.historical_data,
            'Stok Barang': st.session_state.stok_barang
        }
        export_data_to_excel(dataframes, export_file_path)
# Function to get user file paths
def get_user_file_paths(username):
    return {
        'PENJUALAN_FILE': f"{username}_penjualan.csv",
        'STOK_FILE': f"{username}_stok.csv"
    }

# Function to save data
def save_data(username):
    file_paths = get_user_file_paths(username)
    st.session_state.penjualan.to_csv(file_paths['PENJUALAN_FILE'], index=False)
    st.session_state.stok_barang.to_csv(file_paths['STOK_FILE'], index=False)
    st.success("Data berhasil disimpan!")

# Function to load data
def load_data(username):
    file_paths = get_user_file_paths(username)
    if os.path.exists(file_paths['PENJUALAN_FILE']):
        st.session_state.penjualan = pd.read_csv(file_paths['PENJUALAN_FILE'])
    if os.path.exists(file_paths['STOK_FILE']):
        st.session_state.stok_barang = pd.read_csv(file_paths['STOK_FILE'])

# Function for the sales page
def halaman_penjualan(username):
    st.header("Penjualan")

    # Search stock items
    st.subheader("Pencarian Stok Barang")
    search_barang = st.text_input("Cari Barang", "")
    
    if search_barang:
        filtered_stok_barang = st.session_state.stok_barang[
            st.session_state.stok_barang.apply(lambda row: search_barang.lower() in row.astype(str).str.lower().to_list(), axis=1)
        ]
    else:
        filtered_stok_barang = st.session_state.stok_barang

    if "Harga" in filtered_stok_barang.columns:
        filtered_stok_barang = filtered_stok_barang.drop(columns=["Harga"])
    if "Persentase Keuntungan" in filtered_stok_barang.columns:
        filtered_stok_barang = filtered_stok_barang.drop(columns=["Persentase Keuntungan"])
    
    st.subheader("Stok Barang Terupdate")
    st.dataframe(filtered_stok_barang, use_container_width=True, hide_index=False)

    # Action selection for Add or Edit Sale
    selected_action = st.selectbox("Pilih Aksi", ["Tambah Penjualan", "Edit Penjualan"], key='action_select')

    # Form for adding/updating sales
    st.subheader(selected_action)

    # Default values for form fields
    default_values = {
        "Nama Pelanggan": "",
        "Nomor Telepon": "",
        "Alamat": "",
        "Nama Barang": st.session_state.stok_barang["Nama Barang"].tolist()[0] if not st.session_state.stok_barang.empty else "",
        "Ukuran/Kemasan": st.session_state.stok_barang["Ukuran/Kemasan"].tolist()[0] if not st.session_state.stok_barang.empty else "",
        "Merk": st.session_state.stok_barang["Merk"].tolist()[0] if not st.session_state.stok_barang.empty else "",
        "Jumlah": 1,
        "Kode Warna/Base": ""
    }

    if selected_action == "Edit Penjualan":
        # Select the sale to edit
        sale_id = st.selectbox("Pilih ID Penjualan untuk Diedit", st.session_state.penjualan["ID"].tolist() + ["Tambah Baru"], key='sale_id_select')
        
        if sale_id != "Tambah Baru":
            sale_data = st.session_state.penjualan[st.session_state.penjualan["ID"] == sale_id].iloc[0]
            default_values.update({
                "Nama Pelanggan": sale_data["Nama Pelanggan"],
                "Nomor Telepon": sale_data["Nomor Telepon"],
                "Alamat": sale_data["Alamat"],
                "Nama Barang": sale_data["Nama Barang"],
                "Ukuran/Kemasan": sale_data["Ukuran/Kemasan"],
                "Merk": sale_data["Merk"],
                "Kode Warna/Base": sale_data["Kode Warna/Base"] if "Kode Warna/Base" in sale_data and pd.notna(sale_data["Kode Warna/Base"]) else "",
                "Jumlah": sale_data["Jumlah"],
                "ID": sale_id
            })
    
    with st.form("input_penjualan"):
        nama_pelanggan = st.text_input("Nama Pelanggan", value=default_values["Nama Pelanggan"])
        nomor_telpon = st.text_input("Nomor Telepon", value=default_values["Nomor Telepon"])
        alamat = st.text_area("Alamat", value=default_values["Alamat"])

        nama_barang_options = st.session_state.stok_barang["Nama Barang"].tolist()
        nama_barang = st.selectbox("Pilih Barang", nama_barang_options, index=nama_barang_options.index(default_values["Nama Barang"]) if default_values["Nama Barang"] in nama_barang_options else 0)

        ukuran_options = st.session_state.stok_barang[
            st.session_state.stok_barang["Nama Barang"] == nama_barang
        ]["Ukuran/Kemasan"].tolist()
        ukuran = st.selectbox("Ukuran/Kemasan", ukuran_options, index=ukuran_options.index(default_values["Ukuran/Kemasan"]) if default_values["Ukuran/Kemasan"] in ukuran_options else 0)

        merk_options = st.session_state.stok_barang[
            (st.session_state.stok_barang["Nama Barang"] == nama_barang) & 
            (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran)
        ]["Merk"].tolist()
        merk = st.selectbox("Merk", merk_options, index=merk_options.index(default_values["Merk"]) if default_values["Merk"] in merk_options else 0)

        kode_warna = st.text_input("Kode Warna/Base (Opsional)", value=default_values["Kode Warna/Base"])

        # Query to get stock IDs based on selected criteria
        stock_query = st.session_state.stok_barang[(
            st.session_state.stok_barang["Nama Barang"] == nama_barang) &
            (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran) &
            (st.session_state.stok_barang["Merk"] == merk)
        ]
        if kode_warna:
            stock_query = stock_query[stock_query["Kode Warna/Base"] == kode_warna]

        stock_id_options = stock_query["ID"].tolist()
        stock_id = st.selectbox("Pilih ID Stok", stock_id_options, index=stock_id_options.index(default_values.get("ID", stock_id_options[0])) if "ID" in default_values and default_values["ID"] in stock_id_options else 0)

        if stock_id:
            harga_terpilih = stock_query[stock_query["ID"] == stock_id]["Harga Jual"].values[0]
        else:
            harga_terpilih = 0

        jumlah = st.number_input("Jumlah Orderan", min_value=1, value=int(default_values["Jumlah"]))
        total_harga = harga_terpilih * jumlah

        submit = st.form_submit_button("Simpan Penjualan")

        if submit:
            if selected_action == "Tambah Penjualan":
                stok_barang_filter = st.session_state.stok_barang[st.session_state.stok_barang["ID"] == stock_id]

                if not stok_barang_filter.empty:
                    if jumlah <= stok_barang_filter["Stok"].values[0]:
                        new_penjualan = pd.DataFrame({
                            "ID": [st.session_state.penjualan["ID"].max() + 1 if not st.session_state.penjualan.empty else 1],
                            "Nama Pelanggan": [nama_pelanggan],
                            "Nomor Telepon": [nomor_telpon],
                            "Alamat": [alamat],
                            "Nama Barang": [nama_barang],
                            "Ukuran/Kemasan": [ukuran],
                            "Merk": [merk],
                            "Kode Warna/Base": [kode_warna] if kode_warna else None,
                            "Jumlah": [jumlah],
                            "Total Harga": [total_harga],
                            "Waktu": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                        })

                        st.session_state.penjualan = pd.concat([st.session_state.penjualan, new_penjualan], ignore_index=True)

                        # Reduce stock based on the ordered quantity
                        st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"] == stock_id, "Stok"] -= jumlah

                        st.success(f"Penjualan untuk {nama_pelanggan} berhasil disimpan!")
                        
                        save_data(username)  # Save data after successful transaction
                    else:
                        st.error("Stok tidak cukup untuk memenuhi pesanan.")
                else:
                    st.error("ID Stok tidak ditemukan di stok.")
            
            elif selected_action == "Edit Penjualan":
                # Get old sale data to see previous quantity
                penjualan_lama = st.session_state.penjualan.loc[st.session_state.penjualan["ID"] == sale_id].iloc[0]
                jumlah_lama = penjualan_lama["Jumlah"]

                # Update sale
                st.session_state.penjualan.loc[
                    st.session_state.penjualan["ID"] == sale_id,
                    ["Nama Pelanggan", "Nomor Telepon", "Alamat", "Nama Barang", "Ukuran/Kemasan", "Merk", "Kode Warna/Base", "Jumlah", "Total Harga", "Waktu"]
                ] = [nama_pelanggan, nomor_telpon, alamat, nama_barang, ukuran, merk, kode_warna, jumlah, total_harga, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

                # Update stock
                selisih = jumlah - jumlah_lama
                stok_tersedia = st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"] == stock_id, "Stok"].values[0]

                if selisih > 0:  # If adding to stock
                    if selisih <= stok_tersedia:
                        st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"] == stock_id, "Stok"] -= selisih
                        st.success(f"Penjualan dengan ID {sale_id} berhasil diperbarui!")
                    else:
                        st.error("Stok tidak cukup untuk memenuhi tambahan jumlah.")
                elif selisih < 0:  # If reducing from stock
                    st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"] == stock_id, "Stok"] += abs(selisih)
                    st.success(f"Penjualan dengan ID {sale_id} berhasil diperbarui!")

                save_data(username)  # Save data after successful edit
                
    # Customer search section
    st.subheader("Pencarian Pelanggan")
    search_pelanggan = st.text_input("Cari Pelanggan (Nama atau Nomor Telepon)", "")
    
    if search_pelanggan:
        filtered_penjualan = st.session_state.penjualan[
            st.session_state.penjualan.apply(lambda row: search_pelanggan.lower() in row[['Nama Pelanggan', 'Nomor Telepon']].astype(str).str.lower().to_list(), axis=1)
        ]
    else:
        filtered_penjualan = st.session_state.penjualan
    
    if "Keuntungan" in filtered_penjualan.columns:
        filtered_penjualan = filtered_penjualan.drop(columns=["Keuntungan"])

    st.subheader("Riwayat Penjualan")
    st.dataframe(filtered_penjualan, use_container_width=True, hide_index=False)

    # Feature for downloading sales receipt
    st.subheader("Download Struk Penjualan")
    
    receipt_header = st.text_input("Judul Struk", "STRUK PENJUALAN")
    thank_you_message = st.text_area("Pesan Terima Kasih", "Terima Kasih atas Pembelian Anda!")
    
    struk_id = st.selectbox("Pilih ID Penjualan", st.session_state.penjualan["ID"].tolist())
    
    if struk_id:
        penjualan_struk = st.session_state.penjualan[st.session_state.penjualan["ID"] == struk_id].iloc[0]
        struk_content = f"""
        ==============================
        {receipt_header.center(32)}
        ==============================
        ID Penjualan : {penjualan_struk['ID']}
        Tanggal      : {penjualan_struk['Waktu'].strftime("%d-%m-%Y %H:%M") if isinstance(penjualan_struk['Waktu'], datetime) else penjualan_struk['Waktu']}
        ------------------------------
        Nama Pelanggan: {penjualan_struk['Nama Pelanggan'][:20]}
        No. Telepon   : {penjualan_struk['Nomor Telepon']}
        Alamat        : {penjualan_struk['Alamat'][:20]}
        ------------------------------
        Barang  : {penjualan_struk['Nama Barang'][:20]}
        Ukuran  : {penjualan_struk['Ukuran/Kemasan']}
        Merk    : {penjualan_struk['Merk'][:20]}
        Jumlah  : {penjualan_struk['Jumlah']}
        Warna   : {penjualan_struk['Kode Warna/Base'] if 'Kode Warna/Base' in penjualan_struk and penjualan_struk['Kode Warna/Base'] else 'N/A'}
        ------------------------------
        Total Harga : Rp {penjualan_struk['Total Harga']:,.2f}
        ==============================
        {thank_you_message.center(32)}
        ==============================
        """
    
        struk_file = StringIO()
        struk_file.write(struk_content)
    
        st.download_button(
            label="Download Struk",
            data=struk_file.getvalue(),
            file_name=f"struk_penjualan_{struk_id}.txt",
            mime="text/plain"
        )

def main():
    st.title("Aplikasi Penjualan")
    
    # Initialize session state for user and data
    if 'logged_in_user' not in st.session_state:
        st.session_state.logged_in_user = None
    if 'stok_barang' not in st.session_state:
        st.session_state.stok_barang = pd.DataFrame(columns=["ID", "Nama Barang", "Ukuran/Kemasan", "Merk", "Stok", "Harga Jual"])
    if 'penjualan' not in st.session_state:
        st.session_state.penjualan = pd.DataFrame(columns=["ID", "Nama Pelanggan", "Nomor Telepon", "Alamat", "Nama Barang", "Ukuran/Kemasan", "Merk", "Kode Warna/Base", "Jumlah", "Total Harga", "Waktu"])

    # Simulated login for demonstration
    if st.button("Login"):
        st.session_state.logged_in_user = "User"
        load_data(st.session_state.logged_in_user)  # Load user data after login

    # Check if the user is logged in
    if st.session_state.logged_in_user:
        halaman_penjualan(st.session_state.logged_in_user)  # Correct function call



import pandas as pd
import os
from datetime import datetime

# Function to get user file paths
def get_user_file_paths(username):
    return {
        'SUPPLIER_FILE': f"{username}_supplier.csv"
    }

# Function to load data
def load_data(username):
    file_path = get_user_file_paths(username)['SUPPLIER_FILE']
    if os.path.exists(file_path):
        st.session_state.supplier = pd.read_csv(file_path)
    else:
        st.session_state.supplier = pd.DataFrame(columns=['ID', 'Nama Barang', 'Merk', 'Ukuran/Kemasan', 'Jumlah Barang', 'Nama Supplier', 'Tagihan', 'Waktu', 'Jatuh Tempo'])

# Function for Supplier Page
def halaman_supplier(username):
    st.header("Data Supplier")

    # Ensure data is loaded
    if 'supplier' not in st.session_state:
        load_data(username)

    # Selecting Supplier ID for editing or adding new
    supplier_ids = st.session_state.supplier["ID"].tolist()
    supplier_ids.insert(0, "Tambah Baru")  # Option to add new data
    selected_supplier_id = st.selectbox("Pilih ID Supplier untuk Diedit atau Tambah Baru", supplier_ids)

    # Default values for form fields
    if selected_supplier_id == "Tambah Baru":
        selected_supplier = None
        default_values = {
            "Nama Barang": "",
            "Merk": "",
            "Ukuran/Kemasan": "",
            "Jumlah Barang": 0,
            "Nama Supplier": "",
            "Tagihan": 0,
            "Jatuh Tempo": datetime.today()
        }
    else:
        # Retrieve data for the selected supplier ID
        selected_supplier = st.session_state.supplier[st.session_state.supplier["ID"] == selected_supplier_id].iloc[0]
        default_values = {
            "Nama Barang": selected_supplier["Nama Barang"],
            "Merk": selected_supplier["Merk"],
            "Ukuran/Kemasan": selected_supplier["Ukuran/Kemasan"],
            "Jumlah Barang": selected_supplier["Jumlah Barang"],
            "Nama Supplier": selected_supplier["Nama Supplier"],
            "Tagihan": selected_supplier["Tagihan"],
            "Jatuh Tempo": pd.to_datetime(selected_supplier["Jatuh Tempo"])  # Ensure date format is correct
        }

    # Form for inputting supplier data
    with st.form("supplier_form"):
        nama_barang = st.text_input("Nama Barang", value=default_values["Nama Barang"])
        merk = st.text_input("Merk", value=default_values["Merk"])
        ukuran = st.text_input("Ukuran/Kemasan", value=default_values["Ukuran/Kemasan"])
        jumlah_barang = st.number_input("Jumlah Barang", min_value=0, value=int(default_values["Jumlah Barang"]))
        nama_supplier = st.text_input("Nama Supplier", value=default_values["Nama Supplier"])
        tagihan = st.number_input("Tagihan", min_value=0, value=int(default_values["Tagihan"]))
        jatuh_tempo = st.date_input("Tanggal Jatuh Tempo", value=default_values["Jatuh Tempo"])
        submit = st.form_submit_button("Simpan Data Supplier")
        
        if submit:
            if selected_supplier is None:
                # Add new data
                new_id = st.session_state.supplier["ID"].max() + 1 if not st.session_state.supplier.empty else 1
                new_data = pd.DataFrame({
                    "ID": [new_id],
                    "Nama Barang": [nama_barang],
                    "Merk": [merk],
                    "Ukuran/Kemasan": [ukuran],
                    "Jumlah Barang": [jumlah_barang],
                    "Nama Supplier": [nama_supplier],
                    "Tagihan": [tagihan],
                    "Waktu": [datetime.now()],
                    "Jatuh Tempo": [jatuh_tempo]
                })
                st.session_state.supplier = pd.concat([st.session_state.supplier, new_data], ignore_index=True)
                st.success("Data supplier baru berhasil ditambahkan!")
            else:
                # Update existing data
                st.session_state.supplier.loc[st.session_state.supplier["ID"] == selected_supplier_id, 
                    ["Nama Barang", "Merk", "Ukuran/Kemasan", "Jumlah Barang", "Nama Supplier", "Tagihan", "Jatuh Tempo"]] = \
                    [nama_barang, merk, ukuran, jumlah_barang, nama_supplier, tagihan, jatuh_tempo]
                st.success(f"Data supplier ID {selected_supplier_id} berhasil diupdate!")
            
            # Save data after adding or editing supplier
            st.session_state.supplier.to_csv(get_user_file_paths(username)['SUPPLIER_FILE'], index=False)

    # Search by Name or Brand
    search_input = st.text_input("Cari Nama Barang atau Merk")
    
    if search_input:
        filtered_supplier = st.session_state.supplier[
            (st.session_state.supplier["Nama Barang"].str.contains(search_input, case=False)) |
            (st.session_state.supplier["Merk"].str.contains(search_input, case=False))
        ]
        st.write("Hasil Pencarian:")
        st.dataframe(filtered_supplier)
    else:
        # Display data without filter
        st.subheader("Daftar Data Supplier")
        st.dataframe(st.session_state.supplier)



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

def get_user_file_paths(username):
    # Fungsi ini mengembalikan path file untuk data pengguna
    return {
        'HISTORIS_KEUANGAN_FILE': f"data/{username}_historis_keuangan.csv",
        'STOK_BARANG_FILE': f"data/{username}_stok_barang.csv"
    }

def save_data(df, file_path):
    # Simpan DataFrame ke file CSV
    df.to_csv(file_path, index=False)

def save_all_to_excel(username):
    with pd.ExcelWriter(f"data/{username}_data_export.xlsx", engine='openpyxl') as writer:
        # Save each DataFrame to a different sheet
        if 'historical_data' in st.session_state:
            st.session_state.historical_data.to_excel(writer, sheet_name='Historis Keuangan', index=False)
        if 'stok_barang' in st.session_state:
            st.session_state.stok_barang.to_excel(writer, sheet_name='Stok Barang', index=False)

def update_historical_data(username):
    st.title("Laporan Keuangan")

    # Ambil path file untuk data keuangan historis
    file_path = get_user_file_paths(username)['HISTORIS_KEUANGAN_FILE']
    
    # Load data historis jika file ada
    if os.path.exists(file_path):
        st.session_state.historical_data = pd.read_csv(file_path)
    else:
        st.session_state.historical_data = pd.DataFrame(columns=['Tanggal', 'Total Pemasukan', 'Total Pengeluaran'])

    # Tampilkan data historis
    if 'historical_data' in st.session_state:
        st.dataframe(st.session_state.historical_data)
        
        # Hitung total pemasukan dan pengeluaran
        total_income = st.session_state.historical_data['Total Pemasukan'].sum()
        total_expenses = st.session_state.historical_data['Total Pengeluaran'].sum()
        
        st.subheader("Total Keuangan")
        st.write(f"Total Pemasukan: {total_income}")
        st.write(f"Total Pengeluaran: {total_expenses}")
        st.write(f"Sisa: {total_income - total_expenses}")

    st.subheader("Tambah Data Keuangan")
    
    with st.form("financial_form"):
        tanggal = st.date_input("Tanggal", value=datetime.now())
        total_pemasukan = st.number_input("Total Pemasukan", min_value=0.0, format="%.2f")
        total_pengeluaran = st.number_input("Total Pengeluaran", min_value=0.0, format="%.2f")
        
        submitted = st.form_submit_button("Simpan")
        
        if submitted:
            new_financial_data = pd.DataFrame({
                'Tanggal': [tanggal],
                'Total Pemasukan': [total_pemasukan],
                'Total Pengeluaran': [total_pengeluaran]
            })
            
            st.session_state.historical_data = pd.concat([st.session_state.historical_data, new_financial_data], ignore_index=True)
            save_data(st.session_state.historical_data, file_path)
            st.success("Data keuangan berhasil diperbarui.")

    # Form login
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.form("login_form"):
            password = st.text_input("Masukkan Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit and password == "Jayaselalu123":  # Ganti dengan password yang diinginkan
                st.session_state.authenticated = True
                st.success("Login berhasil!")
            elif submit:
                st.error("Password salah!")
        return

    # Jika sudah login, lanjutkan dengan pengelolaan stok barang
    st.header("Pengelolaan Stok Barang")

    # Load data stok barang
    stok_file_path = get_user_file_paths(username)['STOK_BARANG_FILE']
    if os.path.exists(stok_file_path):
        st.session_state.stok_barang = pd.read_csv(stok_file_path)
    else:
        st.session_state.stok_barang = pd.DataFrame(columns=["ID", "Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Stok", "Persentase Keuntungan", "Kode Warna"])

    # Pilihan untuk menambah barang baru
    barang_ids = st.session_state.stok_barang["ID"].tolist()
    barang_ids.insert(0, "Tambah Baru")  # Opsi untuk menambah barang baru
    selected_row = st.selectbox("Pilih ID Barang untuk Diedit atau Tambah Baru", barang_ids)
    
    if selected_row == "Tambah Baru":
        barang_dipilih = None
        default_values = {
            "Nama Barang": "",
            "Merk": "",
            "Ukuran/Kemasan": "",
            "Harga": 0,
            "Stok": 0,
            "Persentase Keuntungan": 0,
            "Kode Warna": ""
        }
    else:
        barang_dipilih = st.session_state.stok_barang[st.session_state.stok_barang["ID"] == selected_row].iloc[0]
        
        default_values = {
            "Nama Barang": barang_dipilih["Nama Barang"],
            "Merk": barang_dipilih["Merk"],
            "Ukuran/Kemasan": barang_dipilih["Ukuran/Kemasan"],
            "Harga": barang_dipilih["Harga"],
            "Stok": barang_dipilih["Stok"],
            "Persentase Keuntungan": barang_dipilih["Persentase Keuntungan"],
            "Kode Warna": barang_dipilih["Kode Warna"]
        }
    
    # Form untuk menambah atau mengedit barang
    with st.form("edit_barang"):
        nama_barang = st.text_input("Nama Barang", value=default_values["Nama Barang"])
        merk = st.text_input("Merk", value=default_values["Merk"])
        ukuran = st.text_input("Ukuran/Kemasan", value=default_values["Ukuran/Kemasan"])
        
        harga = st.number_input("Harga", min_value=0.0, value=float(default_values["Harga"]), format="%.2f")
        stok = st.number_input("Stok Barang", min_value=0, value=int(default_values["Stok"]))
        persentase_keuntungan = st.number_input("Persentase Keuntungan (%)", min_value=0, max_value=100, value=int(default_values["Persentase Keuntungan"]))
        kode_warna = st.text_input("Kode Warna/Base", value=default_values["Kode Warna"], placeholder="Opsional")
        
        # Hitung harga jual berdasarkan persentase keuntungan
        selling_price = harga * (1 + (persentase_keuntungan / 100))
        
        submit = st.form_submit_button("Simpan Barang")
    
        if submit:
            if barang_dipilih is None:
                # Tambah barang baru
                new_id = st.session_state.stok_barang["ID"].max() + 1 if not st.session_state.stok_barang.empty else 1
                new_data = pd.DataFrame({
                    "ID": [new_id],
                    "Nama Barang": [nama_barang],
                    "Merk": [merk],
                    "Ukuran/Kemasan": [ukuran],
                    "Harga": [harga],
                    "Stok": [stok],
                    "Persentase Keuntungan": [persentase_keuntungan],
                    "Kode Warna": [kode_warna],
                    "Harga Jual": [selling_price],
                    "Waktu Input": [datetime.now()]
                })
                st.session_state.stok_barang = pd.concat([st.session_state.stok_barang, new_data], ignore_index=True)
                st.success("Barang baru berhasil ditambahkan!")
            else:
                # Update barang yang sudah ada
                st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"] == selected_row, 
                    ["Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Stok", "Persentase Keuntungan", "Kode Warna", "Harga Jual"]] = \
                    [nama_barang, merk, ukuran, harga, stok, persentase_keuntungan, kode_warna, selling_price]
                st.success(f"Barang ID {selected_row} berhasil diupdate!")
            
            save_data(st.session_state.stok_barang, stok_file_path)  # Simpan data setelah penambahan atau pengeditan

    # Tampilkan daftar stok barang
    st.subheader("Daftar Stok Barang")
    df_stok_barang = st.session_state.stok_barang.copy()
    
    # Cari barang berdasarkan nama atau merk
    search_text = st.text_input("Cari Nama Barang atau Merk", key='search_text')
    if search_text:
        df_stok_barang = df_stok_barang[
            (df_stok_barang["Nama Barang"].str.contains(search_text, case=False, na=False)) |
            (df_stok_barang["Merk"].str.contains(search_text, case=False, na=False))
        ]
    
    st.dataframe(df_stok_barang)
    
    # Tombol untuk menghapus barang
    if selected_row != "Tambah Baru" and st.button("Hapus Barang"):
        st.session_state.stok_barang = st.session_state.stok_barang[st.session_state.stok_barang["ID"] != selected_row]
        st.success(f"Barang ID {selected_row} berhasil dihapus!")
        save_data(st.session_state.stok_barang, stok_file_path)  # Simpan data setelah penghapusan barang

    # Button to export all data to Excel
    if st.button("Ekspor Semua Data ke Excel"):
        save_all_to_excel(username)
        with open(f"data/{username}_data_export.xlsx", "rb") as file:
            st.download_button(
                label="Download Excel",
                data=file,
                file_name=f"{username}_data_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

def main():
    # Initialize session state
    if 'logged_in_user' not in st.session_state:
        st.session_state.logged_in_user = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = pd.DataFrame(columns=['Username', 'Password', 'Role'])  # Adjust based on your user data structure

    # Load user data (this can be from a file or database)
    load_user_data()  # Ensure this function populates st.session_state.user_data

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
                else:
                    st.sidebar.error("Incorrect password.")
            else:
                st.sidebar.error("Username not found.")
    else:
        st.sidebar.write(f"Logged in as: {st.session_state.logged_in_user}")
        with st.sidebar:
            choice = option_menu(
                menu_title="Main Menu",
                options=["Manajemen Stok Barang", "Manajemen Penjualan", "Manajemen Supplier", "Manajemen Piutang Konsumen", "Manajemen Pengeluaran", "Laporan Keuangan"],
                icons=["box", "cart", "person", "credit-card", "cash", "bar-chart"],
                default_index=0
            )

            # Handle navigation based on user choice
            if choice == "Manajemen Stok Barang":
                manage_stock()  # Call your stock management function here
            elif choice == "Manajemen Penjualan":
                halaman_penjualan(st.session_state.logged_in_user)  # Call your sales management function here
            elif choice == "Manajemen Supplier":
                manage_suppliers()  # Add your supplier management function
            elif choice == "Manajemen Piutang Konsumen":
                manage_receivables()  # Add your receivables management function
            elif choice == "Manajemen Pengeluaran":
                manage_expenses()  # Add your expenses management function
            elif choice == "Laporan Keuangan":
                view_financial_reports()  # Add your financial report viewing function


if __name__ == "__main__":
    main()
