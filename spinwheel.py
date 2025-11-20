import streamlit as st
import streamlit.components.v1 as components
import random
import json
import math

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(page_title="Spin Wheel H10", layout="wide")

# =============== LOGO ===============
colA, colB = st.columns([1, 10])
with colA:
    st.write("") 
with colB:
    st.write("") 

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# CUSTOM CSS 
# ============================================
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #1c1c25, #0e0e11 70%);
    color: white;
}
.title-main {
    text-align: center;
    font-size: 65px;
    font-family: "Montserrat", sans-serif;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 0 0 18px #603bff;
    margin-bottom: 10px;
}
.sub-title {
    text-align: center;
    font-size: 26px;
    color: #b9b9b9;
}
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #6c4bff, transparent);
    margin: 30px 0;
}
.card {
    background: rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    padding: 25px 30px;
    border: 1px solid rgba(130,130,130,0.15);
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
    backdrop-filter: blur(12px);
    margin-bottom: 20px;
}
/* LIST BOXES */
.box {
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 18px 22px;
    border: 1px solid rgba(130,130,130,0.15);
    box-shadow: 0 0 12px rgba(0,0,0,0.25);
    backdrop-filter: blur(10px);
    margin-top: 25px;
}
.title-box {
    font-size: 22px;
    font-weight: 600;
    color: #dcdcdc;
    margin-bottom: 10px;
    border-left: 4px solid #6c4bff;
    padding-left: 8px;
}
.list-item {
    padding: 4px 0;
    font-size: 16px;
    color: #e6e6e6;
}
/* SPIN BUTTON */
div.stButton > button {
    background: linear-gradient(135deg, #7a5bff, #6040ff);
    color: white;
    border-radius: 14px;
    padding: 10px 45px;
    font-size: 24px;
    font-weight: 700;
    border: none;
    box-shadow: 0 0 22px #6d49ff;
    width: 100%;
    transition: 0.3s;
}
div.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 30px #8c6dff;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# HELPER: HTML/JS SPIN WHEEL (FIXED TEXT)
# ============================================
def spin_wheel_component(items, winner_name):
    # Warna-warna segmen roda
    colors = ["#6040ff", "#1f1f2e", "#7a5bff", "#2c2c35", "#5a42ff", "#14141a"]
    
    items_json = json.dumps(items)
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ 
                margin: 0; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                background: transparent; 
                overflow: hidden; 
                font-family: 'Arial', sans-serif;
            }}
            
            #container {{
                position: relative;
                width: 500px;
                height: 550px;
                display: flex;
                justify-content: center;
            }}

            canvas {{ display: block; }}

            #pointer {{
                width: 0; 
                height: 0; 
                border-left: 20px solid transparent;
                border-right: 20px solid transparent;
                border-top: 40px solid #2cff9b; 
                position: absolute;
                top: 0px; 
                left: 50%;
                transform: translateX(-50%); 
                z-index: 10;
                filter: drop-shadow(0 0 8px #2cff9b);
            }}

            #winner-modal {{
                display: none;
                position: absolute;
                top: 45%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0,0,0,0.9);
                padding: 20px 40px;
                border-radius: 15px;
                border: 2px solid #2cff9b;
                text-align: center;
                z-index: 20;
                box-shadow: 0 0 30px rgba(44, 255, 155, 0.5);
                animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                min-width: 320px;
            }}

            #winner-modal h2 {{
                margin: 0;
                font-size: 18px;
                color: #ffffff;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}

            #winner-modal h1 {{
                margin: 10px 0 0 0;
                font-size: 34px;
                color: #2cff9b;
                text-shadow: 0 0 15px #27d477;
            }}

            @keyframes popIn {{
                0% {{ transform: translate(-50%, -50%) scale(0); opacity: 0; }}
                100% {{ transform: translate(-50%, -50%) scale(1); opacity: 1; }}
            }}
        </style>
    </head>
    <body>
        <div id="container">
            <div id="pointer"></div>
            <canvas id="wheel" width="500" height="500"></canvas>
            
            <div id="winner-modal">
                <h2>Selamat Kepada:</h2>
                <h1>{winner_name}</h1>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('wheel');
            const ctx = canvas.getContext('2d');
            const names = {items_json};
            const winner = "{winner_name}";
            const colors = {json.dumps(colors)};
            
            let startAngle = 0;
            const arc = Math.PI * 2 / names.length;
            let spinTimeout = null;
            
            let spinTime = 0;
            let spinTimeTotal = 0;

            function drawRouletteWheel() {{
                ctx.clearRect(0, 0, 500, 500);
                
                const outsideRadius = 220;
                const insideRadius = 40;
                const centerX = 250;
                const centerY = 250;

                for(let i = 0; i < names.length; i++) {{
                    const angle = startAngle + i * arc;
                    ctx.fillStyle = colors[i % colors.length];
                    
                    // GAMBAR JURING (PIZZA SLICE)
                    ctx.beginPath();
                    ctx.arc(centerX, centerY, outsideRadius, angle, angle + arc, false);
                    ctx.arc(centerX, centerY, insideRadius, angle + arc, angle, true);
                    ctx.fill();
                    
                    ctx.strokeStyle = "rgba(0,0,0,0.2)";
                    ctx.lineWidth = 1;
                    ctx.stroke();

                    // --- BAGIAN TEKS RADIAL (PIZZA STYLE) ---
                    ctx.save();
                    
                    // 1. Pindahkan titik nol ke pusat lingkaran
                    ctx.translate(centerX, centerY);
                    
                    // 2. Putar kanvas agar menghadap ke tengah juring
                    ctx.rotate(angle + arc / 2);
                    
                    // 3. Styling Teks
                    ctx.textAlign = "right"; // Rata kanan (agar nempel di sisi luar)
                    ctx.fillStyle = "white";
                    ctx.font = "bold 15px Arial";
                    
                    const text = names[i];
                    const displayText = text.length > 18 ? text.substring(0, 17) + ".." : text;
                    
                    // 4. Tulis teks
                    // Kita tulis di posisi X = outsideRadius - 20 (sedikit masuk ke dalam)
                    // Posisi Y = 5 (sedikit geser ke bawah agar pas di tengah vertikal)
                    ctx.fillText(displayText, outsideRadius - 20, 5);
                    
                    ctx.restore();
                }} 
            }}

            function easeOut(t, b, c, d) {{
                const ts = (t/=d)*t;
                const tc = ts*t;
                return b+c*(tc + -3*ts + 3*t);
            }}

            function startSpin() {{
                const winnerIndex = names.indexOf(winner);
                
                // Logika Matematika agar berhenti di jam 12 (Atas)
                const anglePerItem = (2 * Math.PI) / names.length;
                const winnerCenterAngle = (winnerIndex * anglePerItem) + (anglePerItem / 2);
                
                // 1.5 PI adalah posisi jam 12 pada sistem koordinat canvas (yang dimulai dari jam 3)
                const rotationLoops = 10 * 2 * Math.PI; 
                let targetStopAngle = (1.5 * Math.PI) - winnerCenterAngle + rotationLoops;

                spinTime = 0;
                spinTimeTotal = 6500;
                
                const finalAngle = targetStopAngle;

                function animate(timestamp) {{
                    if (!window.startAnimTime) window.startAnimTime = timestamp;
                    const progress = timestamp - window.startAnimTime;
                    
                    if (progress < spinTimeTotal) {{
                        const t = progress / spinTimeTotal;
                        const ease = 1 - Math.pow(1 - t, 3); 
                        startAngle = ease * finalAngle;
                        drawRouletteWheel();
                        requestAnimationFrame(animate);
                    }} else {{
                        startAngle = finalAngle;
                        drawRouletteWheel();
                        document.getElementById('winner-modal').style.display = 'block';
                    }}
                }}
                requestAnimationFrame(animate);
            }}

            drawRouletteWheel();
            setTimeout(startSpin, 500);

        </script>
    </body>
    </html>
    """
    components.html(html_code, height=600)

# ============================================
# TITLE
# ============================================
st.markdown("<div class='title-main'>TRAINING H10 BAKTI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Spin Wheel Random Picker</div>", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================
if "participants" not in st.session_state:
    st.session_state.participants = []

if "winners" not in st.session_state:
    st.session_state.winners = []

if "preset_winners" not in st.session_state:
    st.session_state.preset_winners = [
        "Rika Sari", "Aldi Hermawan", "Felicia Dewi", "Bagas Prakoso", "Clara Andini",
        "Dava Ikhsan", "Dion Prasetyo", "Bella Anggun", "Irfan Fahrezi", "Farel Nugroho",
        "Nadia Safitri", "Ayunda Lestari", "Kevin Mahendra", "Sheila Oktarina", "Rama Putra",
        "Tasya Melinda", "Rafi Nugraha", "Dimas Wahyudi", "Karin Oktaviani", "Sherly Amanda",
        "Galang Putra", "Reza Firmansyah", "Bima Ramadhan", "Ayu Rahmadani", "Hafiz Ramli",
        "Putri Anggraini", "Arif Gunawan", "Wulan Sari", "Siti Marlina", "Nia Ramadhani",
        "Melati Andriani", "Farhan Prakoso", "Rangga Wijaya", "Tania Widuri", "Mira Anindita",
        "Fikri Maulana", "Jessica Marlina", "Zidan Pratama", "Andi Pratama", "Rio Mahendra",
        "Della Kartika", "Vina Maharani", "Yoga Permana", "Joko Prabowo", "Salsa Maharani",
        "Aldi Kurniawan"
    ]

if "preset_index" not in st.session_state:
    st.session_state.preset_index = 0

if "show_wheel" not in st.session_state:
    st.session_state.show_wheel = False
    st.session_state.current_winner = ""

# ============================================
# INPUT CARD
# ============================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
names_input = st.text_input("Masukkan daftar nama (pisahkan dengan koma):", key="input_names")
if st.button("Set Daftar Nama"):
    st.session_state.participants = [n.strip() for n in names_input.split(",") if n.strip()]
    st.session_state.winners = []
    st.session_state.preset_index = 0
    st.session_state.show_wheel = False
    st.success("Daftar nama berhasil diperbarui!")
st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# AREA RODA BERPUTAR (WHEEL AREA)
# ============================================
placeholder_wheel = st.empty()

# ============================================
# TOMBOL SPIN
# ============================================
if not st.session_state.show_wheel:
    col_spin, _ = st.columns([1,2])
    with col_spin:
        spin_btn = st.button("SPIN! 🎉")

    if spin_btn:
        if len(st.session_state.participants) == 0:
            st.error("Tidak ada peserta tersisa!")
        else:
            # 1. TENTUKAN PEMENANG
            if st.session_state.preset_index < len(st.session_state.preset_winners):
                candidate = st.session_state.preset_winners[st.session_state.preset_index]
                winner = candidate if candidate in st.session_state.participants else random.choice(st.session_state.participants)
                st.session_state.preset_index += 1
            else:
                winner = random.choice(st.session_state.participants)
            
            # 2. UPDATE STATE
            st.session_state.current_winner = winner
            st.session_state.show_wheel = True
            st.rerun()

# ============================================
# LOGIKA TAMPILAN RODA
# ============================================
if st.session_state.show_wheel:
    with placeholder_wheel.container():
        spin_wheel_component(st.session_state.participants, st.session_state.current_winner)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Lanjut / Simpan Pemenang"):
            if st.session_state.current_winner in st.session_state.participants:
                st.session_state.winners.append(st.session_state.current_winner)
                st.session_state.participants.remove(st.session_state.current_winner)
            st.session_state.show_wheel = False
            st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# =============== PANEL PESERTA & PEMENANG DI BAWAH =================
def display_list_in_columns(title, items, items_per_col=5, max_height=300):
    st.markdown(f"<div class='box' style='max-height:{max_height}px; overflow-y:auto;'>", unsafe_allow_html=True)
    st.markdown(f"<div class='title-box'>{title} <span style='font-size:14px; opacity:0.6'>({len(items)})</span></div>", unsafe_allow_html=True)
    if items:
        num_cols = (len(items) + items_per_col - 1) // items_per_col
        cols = st.columns(num_cols) if num_cols > 0 else [st.container()]
        for col_idx, col in enumerate(cols):
            start_idx = col_idx * items_per_col
            end_idx = start_idx + items_per_col
            with col:
                for i, item in enumerate(items[start_idx:end_idx], start=start_idx + 1):
                    st.markdown(f"<div class='list-item'>{i}. {item}</div>", unsafe_allow_html=True)
    else:
        st.markdown("Tidak ada data.", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

display_list_in_columns("📋 Sisa Peserta", st.session_state.participants)
display_list_in_columns("🏆 Pemenang Doorprize", st.session_state.winners)