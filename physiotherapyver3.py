import streamlit as st
import pandas as pd

# Konfigurasi tampilan aplikasi
st.set_page_config(page_title="PhysioConnect", layout="wide")

# Header Aplikasi (tanpa logo)
st.markdown("""
    <h1 style='color:#D62828;'>PhysioConnect</h1>
    <p><i>Your Physiotherapy Telemedicine Hub</i></p>
    <hr>
""", unsafe_allow_html=True)

# Inisialisasi session state
state = st.session_state
if 'user_type' not in state: state.user_type = None
if 'physios' not in state:
    state.physios = pd.DataFrame(columns=["name", "phone", "lat", "lon"])
if 'messages' not in state:
    state.messages = []

# Sidebar login
with st.sidebar:
    st.title("Login Area")
    role = st.radio("Login as:", ["Patient", "Admin"])
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if role == "Admin" and user == "admin" and pwd == "admin123":
            state.user_type = "admin"
            st.success("Logged in as Admin")
        elif role == "Patient" and user:
            state.user_type = "patient"
            state.username = user
            st.success(f"Logged in as {user}")
        else:
            st.error("Login failed. Coba lagi!")

# Panel Admin
if state.user_type == "admin":
    st.subheader("🛠️ Admin Panel")
    admin_action = st.selectbox("Pilih Aksi:", ["Balas Chat", "Tambah Fisioterapis", "Pengaturan"])

    if admin_action == "Balas Chat":
        st.write("📩 Pesan dari Pasien:")
        for i, msg in enumerate(state.messages):
            st.write(f"**{msg['user']}**: {msg['text']}")
            reply = st.text_input(f"Balas ke {msg['user']}", key=f"r{i}")
            if st.button("Kirim", key=f"s{i}") and reply:
                state.messages[i]["reply"] = reply
                st.success("Balasan terkirim!")
    elif admin_action == "Tambah Fisioterapis":
        with st.form("tambah_fisio"):
            nama = st.text_input("Nama")
            nohp = st.text_input("Nomor HP")
            lat = st.number_input("Latitude", value=0.0)
            lon = st.number_input("Longitude", value=0.0)
            if st.form_submit_button("Tambah"):
                state.physios = state.physios.append({"name": nama, "phone": nohp, "lat": lat, "lon": lon}, ignore_index=True)
                st.success(f"Fisioterapis {nama} berhasil ditambahkan.")
    else:
        st.write("⚙️ Pengaturan")
        st.text_input("Ubah Password (fitur belum aktif)")
        st.selectbox("Bahasa", ["Bahasa Indonesia", "English"])

# Panel Pasien
elif state.user_type == "patient":
    st.subheader(f"👤 Selamat datang, {state.username}")
    menu = st.selectbox("Menu Layanan:", ["Jurnal Fisioterapi", "Fisioterapis Terdekat", "Chat dengan Fisioterapis", "Rekomendasi Latihan"])

    if menu == "Jurnal Fisioterapi":
        st.markdown("📚 [Kunjungi Jurnal Fisiomu UMS](https://journals.ums.ac.id/)")

    elif menu == "Fisioterapis Terdekat":
        if not state.physios.empty:
            st.map(state.physios.rename(columns={"lat": "latitude", "lon": "longitude"}))
            st.dataframe(state.physios)
        else:
            st.warning("Data fisioterapis belum tersedia.")

    elif menu == "Chat dengan Fisioterapis":
        pesan = st.text_input("Tulis pesan kamu:")
        if st.button("Kirim"):
            state.messages.append({"user": state.username, "text": pesan, "reply": ""})
            st.success("Pesan terkirim.")
        st.write("---")
        for m in state.messages:
            if m["user"] == state.username:
                st.write(f"🗨️ Kamu: {m['text']}")
                if m.get("reply"):
                    st.write(f"💬 Admin: {m['reply']}")

    elif menu == "Rekomendasi Latihan":
        kondisi = st.text_input("Masukkan nama kondisi (contoh: nyeri punggung bawah)")
        if st.button("Cari Rekomendasi") and kondisi:
            st.video("https://www.youtube.com/watch?v=4BOTvaRaDjI")
            st.markdown(f"**Rekomendasi:** Lakukan latihan ringan untuk {kondisi}. 3 set × 10 repetisi.")

# Belum login
else:
    st.info("Silakan login di sidebar untuk mengakses fitur aplikasi PhysioConnect.")
