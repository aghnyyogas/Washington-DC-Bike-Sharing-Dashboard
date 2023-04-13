import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

# Load  data
daily_df = pd.read_csv("day.csv")
hourly_data = pd.read_csv("hour.csv")
daily_df['Temperatur_(C)'] = daily_df['temp'] * 41
daily_df['yr'] = daily_df['yr'].replace({0: 2011, 1: 2012})
daily_df['season'] = daily_df['season'].replace({1: 'Springer', 2: "Summer", 3:"Fall", 4:"Winter"})

def dashboard_performa_tahunan(df):
    jumlah_sewa_berdasarkan_tahun = df.groupby('yr')['cnt'].sum()
    kenaikan_jumlah_sewa_by_tahun = jumlah_sewa_berdasarkan_tahun[2012] - jumlah_sewa_berdasarkan_tahun[2011]
    kenaikan_jumlah_sewa_by_tahun_persentase = ((jumlah_sewa_berdasarkan_tahun[2012] - jumlah_sewa_berdasarkan_tahun[2011]) / jumlah_sewa_berdasarkan_tahun[2011]) * 100

    fig, ax = plt.subplots()
    ax.bar(x=daily_df['yr'], height=daily_df['cnt'])
    ax.set_xticks([2011, 2012])
    ax.set_title(f'Kenaikan Persentase: {kenaikan_jumlah_sewa_by_tahun} atau {kenaikan_jumlah_sewa_by_tahun_persentase:.2f}%')
    ax.set_ylabel("Jumlah sewa")
    # Menampilkan plot menggunakan Streamlit
    st.pyplot(fig)
    return fig

def dashboard_performa_bulanan(df):
    # Menghitung jumlah sewa per bulan berdasarkan tahun
    jumlah_sewa_per_bulan_berdasarkan_tahun = daily_df.groupby(['yr', 'mnth'])['cnt'].agg(['sum']).reset_index()

    # Pisahkan data untuk tiap tahun
    data_2011 = jumlah_sewa_per_bulan_berdasarkan_tahun[jumlah_sewa_per_bulan_berdasarkan_tahun['yr']==2011]
    data_2012 = jumlah_sewa_per_bulan_berdasarkan_tahun[jumlah_sewa_per_bulan_berdasarkan_tahun['yr']==2012]

    # Buat plot
    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(data_2011['mnth'], data_2011['sum'], label='2011')
    ax.plot(data_2012['mnth'], data_2012['sum'], label='2012')

    # Konfigurasi plot
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Sewa')
    ax.set_xticks(data_2011['mnth'])
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
    ax.legend()

    # Tampilkan plot di Streamlit
    st.pyplot(fig)
    return fig

def dashboard_musim_favorite(df):
    st.subheader("Jumlah sewa berdasarkan musim")
    # Menghitung jumlah penyewa per musim
    jumlah_penyewa_berdasarkan_musim = daily_df.groupby('season')['cnt'].sum().sort_values(ascending=False)

    # membuat bar plot
    fig, ax = plt.subplots()
    ax.bar(jumlah_penyewa_berdasarkan_musim.index, jumlah_penyewa_berdasarkan_musim.values)

    # menambahkan nilai pada tiap bar chart
    for i in ax.patches:
        ax.text(i.get_x()+0.15, i.get_height()+10000, str(round(i.get_height(), 2)), fontsize=11, color='black')

    # # menambahkan judul dan label sumbu
    # ax.set_title('Jumlah Penyewa Berdasarkan Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penyewa')
    

    # menampilkan plot
    st.pyplot(fig)
    return fig

st.title("Dashboard Analisis Data Bike Sharing")



with st.sidebar.form('my_form'):
    st.image("logo.png")
    pilihan_dashboard = st.selectbox("", ('----Pilih Dashboard----', 'Performa sewa', 'Musim Favorit'))

    submitted1 = st.form_submit_button('Tampilkan')
    
# st.subheader("Biodata Pridadi")
if pilihan_dashboard == 'Performa sewa':
    dashboard_performa_tahunan(daily_df)
    dashboard_performa_bulanan(daily_df)
elif pilihan_dashboard ==  'Musim Favorit':
    dashboard_musim_favorite(daily_df)
else:
    with st.expander("Lihat detail tentang dashboard ini"):
        st.image("logo_2.png", use_column_width=True)
        st.markdown("""
            Sistem ***bike sharing*** adalah generasi baru dari penyewaan sepeda tradisional dengan proses otomatis.
        Saat ini, terdapat lebih dari 500 program berbagi sepeda di seluruh dunia yang terdiri dari lebih dari 500 ribu sepeda.
        Sistem ***bike sharing*** dapat digunakan sebagai jaringan sensor virtual untuk mendeteksi mobilitas di kota.

        Proses penyewaan ***bike sharing*** sangat dipengaruhi oleh kondisi lingkungan dan musiman.
        **Data set** yang digunakan pada dashboard ini adalah data history pada tahun **2011 dan 2012 dari sistem Capital Bikeshare, Washington D.C., AS**.
        Data tersebut telah diolah dengan mengekstrak dan menambahkan informasi cuaca dan musiman yang sesuai.
        """)

st.caption("Aghny Yogaswara Arifianyah - Washington D.C Bike Sharing - DiCoding Indonesia")
