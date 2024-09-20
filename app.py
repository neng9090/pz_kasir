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

# Function for Stock Management Page with Advanced Features
def halaman_stock_barang():
    st.markdown('<h1 style="text-align: center;">Stock Barang</h1>', unsafe_allow_html=True)

    # Load stock data from session or file
    file_path = get_user_file_paths(st.session_state.username)['STOK_BARANG_FILE']
    if os.path.exists(file_path):
        st.session_state.stok_barang = pd.read_csv(file_path)
    else:
        st.session_state.stok_barang = pd.DataFrame(columns=['ID', 'Nama Barang', 'Merk', 'Ukuran/Kemasan', 'Harga', 'Stok', 'Kode Warna/Base', 'Harga Jual', 'Waktu Input'])

    # Search and filter options
    st.sidebar.markdown("### Cari/Filter Barang")
    search_keyword = st.sidebar.text_input("Cari Nama Barang/Merk", "")
    filter_merk = st.sidebar.multiselect("Filter Berdasarkan Merk", st.session_state.stok_barang['Merk'].unique())
    
    # Apply search and filter
    filtered_data = st.session_state.stok_barang[
        (st.session_state.stok_barang['Nama Barang'].str.contains(search_keyword, case=False)) &
        (st.session_state.stok_barang['Merk'].isin(filter_merk) if filter_merk else True)
    ]
    
    # Display stock table with filtering
    st.dataframe(filtered_data)

    # Stock alerts for low quantities
    st.markdown('<h2>Notifikasi Stok Rendah</h2>', unsafe_allow_html=True)
    low_stock_items = filtered_data[filtered_data['Stok'] < 10]  # Customize threshold for low stock
    if not low_stock_items.empty:
        st.error(f"Item dengan stok rendah:\n{low_stock_items[['Nama Barang', 'Merk', 'Stok']].to_string(index=False)}")
    
    # Form input for adding/updating stock
    st.markdown('<h2 style="text-align: center;">Tambah/Edit Barang</h2>', unsafe_allow_html=True)
    
    # Batch update or delete options
    batch_options = st.sidebar.selectbox("Batch Aksi", ["None", "Hapus Barang", "Update Harga", "Update Stok"])
    
    if batch_options == "Hapus Barang":
        selected_ids = st.multiselect("Pilih ID Barang untuk Dihapus", filtered_data["ID"].tolist())
        if st.button("Hapus"):
            st.session_state.stok_barang = st.session_state.stok_barang[~st.session_state.stok_barang["ID"].isin(selected_ids)]
            save_data()
            st.success("Barang berhasil dihapus!")
    
    elif batch_options in ["Update Harga", "Update Stok"]:
        selected_ids = st.multiselect(f"Pilih ID Barang untuk {batch_options}", filtered_data["ID"].tolist())
        if selected_ids:
            new_value = st.number_input(f"Nilai Baru {batch_options}", min_value=0.0 if batch_options == "Update Harga" else 0, value=0)
            if st.button("Update"):
                if batch_options == "Update Harga":
                    st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"].isin(selected_ids), "Harga"] = new_value
                else:
                    st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"].isin(selected_ids), "Stok"] = new_value
                save_data()
                st.success(f"{batch_options} berhasil diperbarui!")

    # Form for adding or editing stock
    with st.form("input_barang"):
        selected_action = st.selectbox("Pilih Aksi", ["Tambah Barang", "Edit Barang"])
        if selected_action == "Edit Barang":
            selected_id = st.selectbox("Pilih ID Barang untuk Diedit", filtered_data["ID"].tolist())
            barang_dipilih = st.session_state.stok_barang[st.session_state.stok_barang["ID"] == selected_id].iloc[0]
        else:
            selected_id = None
            barang_dipilih = pd.Series(default_values)

        nama_barang = st.text_input("Nama Barang", value=barang_dipilih["Nama Barang"])
        merk = st.text_input("Merk", value=barang_dipilih["Merk"])
        ukuran = st.text_input("Ukuran/Kemasan", value=barang_dipilih["Ukuran/Kemasan"])
        harga = st.number_input("Harga", min_value=0, value=int(barang_dipilih["Harga"]))
        stok = st.number_input("Stok Barang", min_value=0, value=int(barang_dipilih["Stok"]))
        kode_warna = st.text_input("Kode Warna/Base", value=barang_dipilih["Kode Warna/Base"], placeholder="Opsional")

        # Calculate selling price
        selling_price = harga * 1.15

        submit = st.form_submit_button("Simpan Barang")
        if submit:
            if selected_action == "Edit Barang":
                st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"] == selected_id, ["Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Stok", "Kode Warna/Base", "Harga Jual"]] = [nama_barang, merk, ukuran, harga, stok, kode_warna, selling_price]
            else:
                new_id = st.session_state.stok_barang["ID"].max() + 1 if not st.session_state.stok_barang.empty else 1
                new_data = pd.DataFrame({
                    "ID": [new_id],
                    "Nama Barang": [nama_barang],
                    "Merk": [merk],
                    "Ukuran/Kemasan": [ukuran],
                    "Harga": [harga],
                    "Stok": [stok],
                    "Kode Warna/Base": [kode_warna],
                    "Harga Jual": [selling_price],
                    "Waktu Input": [datetime.now()]
                })
                st.session_state.stok_barang = pd.concat([st.session_state.stok_barang, new_data], ignore_index=True)

            save_data()
            st.success(f"Barang berhasil {'diedit' if selected_action == 'Edit Barang' else 'ditambahkan'}!")

    # Export/Import options
    st.sidebar.markdown("### Export/Import Data")
    export_format = st.sidebar.selectbox("Pilih Format Ekspor", ["CSV", "Excel"])
    
    if st.sidebar.button("Export Data"):
        export_file_path = f"stock_barang_export.{export_format.lower()}"
        if export_format == "CSV":
            st.session_state.stok_barang.to_csv(export_file_path, index=False)
        else:
            st.session_state.stok_barang.to_excel(export_file_path, index=False)
        st.sidebar.success(f"Data berhasil diexport sebagai {export_format}!")

    uploaded_file = st.sidebar.file_uploader("Import Data", type=["csv", "xlsx"])
    if uploaded_file:
        if uploaded_file.name.endswith("csv"):
            imported_data = pd.read_csv(uploaded_file)
        else:
            imported_data = pd.read_excel(uploaded_file)
        st.session_state.stok_barang = pd.concat([st.session_state.stok_barang, imported_data], ignore_index=True)
        save_data()
        st.sidebar.success("Data berhasil diimpor!")

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
        
        # Calculate total income and total expenses
        total_income = st.session_state.historical_data['Total Pemasukan'].sum()
        total_expenses = st.session_state.historical_data['Total Pengeluaran'].sum()
        
        st.subheader("Total Keuangan")
        st.write(f"Total Pemasukan: {total_income}")
        st.write(f"Total Pengeluaran: {total_expenses}")
        st.write(f"Sisa: {total_income - total_expenses}")
    
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
                    # Remove the experimental_rerun() call
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
