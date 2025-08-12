import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Inspeksi Kapal", layout="wide")

# Load data
df = pd.read_csv("dataset/psakapal.csv", sep=";", encoding="latin1")
df['Inspection_Date'] = pd.to_datetime(df['Inspection_Date'], errors='coerce')
df['Next_Inspection_Date'] = pd.to_datetime(df['Next_Inspection_Date'], errors='coerce')
df['Year'] = df['Inspection_Date'].dt.year

# Tambahkan kolom Delay_Status
def label_delay(x):
    if pd.isna(x):
        return 'Belum Dijadwalkan'
    elif x > 250:
        return 'Lambat'
    else:
        return 'Cepat'

df['Delay_Status'] = df['Interval(Days)'].apply(label_delay)

# ============================
# SIDEBAR FILTER
# ============================
st.sidebar.title("🔎 Filter Data")

years = sorted(df['Year'].dropna().unique())
selected_years = st.sidebar.multiselect("Pilih Tahun Inspeksi", years, default=years)

ports = sorted(df['Port'].dropna().unique())
selected_ports = st.sidebar.multiselect("Pilih Pelabuhan", ports, default=ports)

df_filtered = df[
    (df['Year'].isin(selected_years)) &
    (df['Port'].isin(selected_ports))
]

# ============================
# JUDUL
# ============================
st.title("🚢 Dashboard Inspeksi Kapal Pertamina")
st.markdown("Data ini diambil dari website **PERTAVOS**, berisi informasi inspeksi berkala kapal terkait perpanjangan PSA.")

# ============================
# SECTION 1: KPI METRICS
# ============================
st.subheader("📌 Ringkasan Data")

col1, col2, col3 = st.columns(3)
col1.metric("Total Inspeksi", len(df_filtered))
col2.metric("Jumlah Kapal Unik", df_filtered['Vessel_Name'].nunique())
col3.metric("Pelabuhan Terlibat", df_filtered['Port'].nunique())

# ============================
# SECTION 2: Delay Status
# ============================
st.subheader("⏱️ Distribusi Delay Status")

delay_count = df_filtered['Delay_Status'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(delay_count, labels=delay_count.index, autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#ff9999','#d3d3d3'])
ax1.axis('equal')
st.pyplot(fig1)

# ============================
# SECTION 3: Top 5 Pelabuhan
# ============================
st.subheader("⚓ Top 5 Pelabuhan dengan Jumlah Inspeksi")

top_ports = df_filtered['Port'].value_counts().head(5)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_ports.values, y=top_ports.index, ax=ax2, palette="viridis")
ax2.set_xlabel("Jumlah Inspeksi")
ax2.set_ylabel("Pelabuhan")
st.pyplot(fig2)

# ============================
# SECTION 4: Histogram Interval
# ============================
st.subheader("📊 Distribusi Interval (Hari) Antar Inspeksi")

fig3, ax3 = plt.subplots()
sns.histplot(df_filtered['Interval(Days)'].dropna(), bins=30, kde=True, color='skyblue', ax=ax3)
ax3.set_xlabel("Interval (Hari)")
ax3.set_ylabel("Jumlah Inspeksi")
st.pyplot(fig3)

# ============================
# SECTION 5: Delay Terlama
# ============================
st.subheader("🚨 Top 5 Kapal dengan Delay Terlama")

top_delay = df_filtered[['Vessel_Name', 'Interval(Days)']].dropna().sort_values(by='Interval(Days)', ascending=False).head(5)

fig4, ax4 = plt.subplots()
sns.barplot(data=top_delay, x='Interval(Days)', y='Vessel_Name', palette='Reds_r', ax=ax4)
ax4.set_xlabel("Interval (Hari)")
ax4.set_ylabel("Nama Kapal")
st.pyplot(fig4)

with st.expander("📄 Lihat tabel detail"):
    st.dataframe(top_delay.set_index('Vessel_Name'))

# ============================
# SECTION 6: Tren Tahunan
# ============================
st.subheader("📈 Tren Jumlah Inspeksi per Tahun")

yearly = df_filtered['Year'].value_counts().sort_index()
fig5, ax5 = plt.subplots()
sns.lineplot(x=yearly.index, y=yearly.values, marker='o', ax=ax5, color="green")
ax5.set_xlabel("Tahun")
ax5.set_ylabel("Jumlah Inspeksi")
st.pyplot(fig5)

# ============================
# SECTION 7: Jenis Inspeksi
# ============================
st.subheader("🔍 Distribusi Jenis Inspeksi")

fig6, ax6 = plt.subplots()
sns.countplot(data=df_filtered, x='Type_of_Inspection', palette='Set2', ax=ax6)
ax6.set_xlabel("Jenis Inspeksi")
ax6.set_ylabel("Jumlah")
st.pyplot(fig6)

# ============================
# FOOTER
# ============================
st.markdown("---")
st.markdown("Made by Yovela Kalista Avansa | Data source: [PERTAVOS](https://apps.pertamina.com/vetting2/login)")