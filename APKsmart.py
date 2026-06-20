import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="OryzaSmart Logic",
    page_icon="🌾",
    layout="centered"
)

st.title("🌾 OryzaSmart Logic")
st.subheader("Monitoring dan Diagnosis Tanaman Padi")

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Monitoring", "Riwayat"]
)

if "data" not in st.session_state:
    st.session_state.data = []

# ==================================================
# DASHBOARD
# ==================================================
if menu == "Dashboard":

    st.header("Dashboard")

    st.info("""
    OryzaSmart Logic membantu petani
    memonitor kondisi tanaman padi,
    mendeteksi hama/penyakit,
    serta memberikan rekomendasi penanganan.
    """)

    st.metric(
        "Jumlah Monitoring",
        len(st.session_state.data)
    )

# ==================================================
# MONITORING
# ==================================================
elif menu == "Monitoring":

    st.header("Input Monitoring")

    luas = st.number_input(
        "Luas Lahan (m²)",
        min_value=100,
        value=1000
    )

    umur = st.number_input(
        "Umur Tanaman (hari)",
        min_value=1,
        value=30
    )

    suhu = st.number_input(
        "Suhu (°C)",
        min_value=20,
        max_value=45,
        value=30
    )

    gejala = st.text_area(
        "Gejala Tanaman",
        placeholder="""
Contoh:
- Daun menguning
- Ada bercak coklat
- Banyak serangga kecil coklat
- Batang berlubang
        """
    )

    if st.button("🔍 Analisis"):

        # ======================================
        # FASE PERTUMBUHAN
        # ======================================

        if umur <= 40:
            fase = "Vegetatif"
            pupuk = "Urea 100 kg/ha"

        elif umur <= 80:
            fase = "Generatif"
            pupuk = "NPK 75 kg/ha"

        else:
            fase = "Pematangan"
            pupuk = "Tidak perlu pemupukan besar"

        # ======================================
        # DIAGNOSIS
        # ======================================

        gejala_lower = gejala.lower()

        diagnosis = "Tanaman Sehat"
        pestisida = "-"
        status = "Sehat"

        # WERENG
        if (
            "serangga kecil" in gejala_lower
            or "coklat" in gejala_lower
            or "daun mengering" in gejala_lower
        ):

            diagnosis = "Hama Wereng"
            pestisida = "Imidakloprid atau BPMC"
            status = "Hama"

        # BLAS
        elif (
            "bercak" in gejala_lower
            or "abu abu" in gejala_lower
        ):

            diagnosis = "Penyakit Blas"
            pestisida = "Trisiklazol"
            status = "Penyakit"

        # TUNGRO
        elif (
            "kuning" in gejala_lower
            and "kerdil" in gejala_lower
        ):

            diagnosis = "Penyakit Tungro"
            pestisida = "Pengendalian vektor wereng hijau"
            status = "Penyakit"

        # PENGGEREK BATANG
        elif (
            "batang" in gejala_lower
            and "lubang" in gejala_lower
        ):

            diagnosis = "Penggerek Batang"
            pestisida = "Klorantraniliprol"
            status = "Hama"

        # TIKUS
        elif "gigitan" in gejala_lower:

            diagnosis = "Serangan Tikus"
            pestisida = "Perangkap tikus"
            status = "Hama"

        # ======================================
        # PREDIKSI PANEN
        # ======================================

        produktivitas = 7000

        if status != "Sehat":
            produktivitas -= 1000

        if suhu > 35:
            produktivitas -= 500

        luas_ha = luas / 10000

        prediksi_ton = (luas_ha * produktivitas)/1000

        # ======================================
        # OUTPUT
        # ======================================

        st.success("Analisis Berhasil")

        st.write("## Hasil Monitoring")

        st.write("🌱 Fase Pertumbuhan :", fase)
        st.write("🌾 Status :", diagnosis)
        st.write("💊 Rekomendasi Pengendalian :", pestisida)
        st.write("🧪 Rekomendasi Pupuk :", pupuk)

        st.write(
            "📦 Estimasi Panen :",
            round(prediksi_ton, 2),
            "ton"
        )

        st.session_state.data.append({
            "Tanggal": datetime.now().strftime("%d-%m-%Y"),
            "Luas (m²)": luas,
            "Umur": umur,
            "Suhu": suhu,
            "Diagnosis": diagnosis,
            "Pestisida": pestisida,
            "Prediksi (ton)": prediksi_ton
        })

# ==================================================
# RIWAYAT
# ==================================================
elif menu == "Riwayat":

    st.header("Riwayat Monitoring")

    if st.button("🗑️ Hapus Semua Riwayat"):
        st.session_state.data = []
        st.success("Riwayat berhasil dihapus")
        st.rerun()

    if len(st.session_state.data) == 0:

        st.warning("Belum ada data.")

    else:

        df = pd.DataFrame(st.session_state.data)

        st.dataframe(
            df,
            use_container_width=True
        )

        st.metric(
            "Jumlah Monitoring",
            len(df)
        )