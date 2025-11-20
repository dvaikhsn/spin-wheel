import streamlit as st
import streamlit.components.v1 as components
import random
import json
import math

# ============================================
# 1. PAGE CONFIG (HARUS PALING ATAS)
# ============================================
st.set_page_config(page_title="Spin Wheel SATRIA-1", layout="wide")

# ============================================
# 2. LOGO SECTION (REVISI: CENTER)
# ============================================
# Kita pakai kolom spacer di kiri dan kanan untuk mendorong logo ke tengah
# Rasio: [Spacer, Logo1, Logo2, Spacer]
c_spacer_L, c_logo1, c_logo2, c_spacer_R = st.columns([4, 1.5, 1.5, 4])

with c_logo1:
    # Gunakan use_container_width=True (Streamlit baru) atau use_column_width=True
    # Agar logo menyesuaikan lebar kolom yang sudah kita set sempit
    try:
        st.image("snt.png", use_container_width=True) 
    except:
        st.write("SNT")

with c_logo2:
    try:
        st.image("bakti.png", use_container_width=True)
    except:
        st.write("BAKTI")

# Jarak sedikit ke judul
st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# 3. CUSTOM CSS 
# ============================================
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #1c1c25, #0e0e11 70%);
    color: white;
}

/* JUDUL */
.title-main {
    text-align: center;
    font-size: 50px;
    font-family: "Montserrat", sans-serif;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 0 0 18px #603bff;
    margin-top: 10px;
    margin-bottom: 5px;
}
.sub-title {
    text-align: center;
    font-size: 20px;
    color: #b9b9b9;
    margin-bottom: 30px;
}

/* INPUT CARD */
.card {
    background: rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    padding: 20px 30px;
    border: 1px solid rgba(130,130,130,0.15);
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
    backdrop-filter: blur(12px);
    margin-bottom: 30px;
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
    font-size: 18px;
    font-weight: 600;
    color: #dcdcdc;
    margin-bottom: 10px;
    border-left: 4px solid #6c4bff;
    padding-left: 8px;
}
.list-item {
    padding: 4px 0;
    font-size: 14px;
    color: #e6e6e6;
}

/* PEMISAH */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #6c4bff, transparent);
    margin: 30px 0;
}

/* TOMBOL (CSS AGAR PRESISI DI TENGAH) */
div.stButton > button {
    background: linear-gradient(135deg, #7a5bff, #6040ff);
    color: white;
    border-radius: 14px;
    padding: 12px 50px;
    font-size: 20px;
    font-weight: 700;
    border: none;
    box-shadow: 0 0 22px #6d49ff;
    transition: 0.3s;
    display: block; 
    margin: 0 auto; /* Posisi Tengah */
    width: fit-content;
}
div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 35px #8c6dff;
    border-color: white;
}
div.stButton > button:disabled {
    background: #333;
    color: #777;
    box-shadow: none;
    cursor: not-allowed;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# 4. HELPER: HTML/JS SPIN WHEEL
# ============================================
def spin_wheel_component(items, winner_name):
    colors = ["#6040ff", "#1f1f2e", "#7a5bff", "#2c2c35", "#5a42ff", "#14141a"]
    items_json = json.dumps(items)
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ 
                margin: 0; display: flex; justify-content: center; align-items: center; 
                background: transparent; overflow: hidden; font-family: 'Arial', sans-serif;
            }}
            #container {{
                position: relative; width: 500px; height: 550px; display: flex; justify-content: center;
            }}
            canvas {{ display: block; }}
            #pointer {{
                width: 0; height: 0; 
                border-left: 20px solid transparent;
                border-right: 20px solid transparent;
                border-top: 40px solid #2cff9b; 
                position: absolute; top: 0px; left: 50%;
                transform: translateX(-50%); z-index: 10;
                filter: drop-shadow(0 0 8px #2cff9b);
            }}
            #winner-modal {{
                display: none; position: absolute; top: 45%; left: 50%;
                transform: translate(-50%, -50%); background: rgba(0,0,0,0.9);
                padding: 20px 40px; border-radius: 15px; border: 2px solid #2cff9b;
                text-align: center; z-index: 20;
                box-shadow: 0 0 30px rgba(44, 255, 155, 0.5);
                animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                min-width: 320px;
            }}
            #winner-modal h2 {{ margin: 0; font-size: 18px; color: #ffffff; text-transform: uppercase; letter-spacing: 1px; }}
            #winner-modal h1 {{ margin: 10px 0 0 0; font-size: 34px; color: #2cff9b; text-shadow: 0 0 15px #27d477; }}
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
                    ctx.beginPath();
                    ctx.arc(centerX, centerY, outsideRadius, angle, angle + arc, false);
                    ctx.arc(centerX, centerY, insideRadius, angle + arc, angle, true);
                    ctx.fill();
                    ctx.strokeStyle = "rgba(0,0,0,0.2)";
                    ctx.lineWidth = 1;
                    ctx.stroke();
                    ctx.save();
                    ctx.translate(centerX, centerY);
                    ctx.rotate(angle + arc / 2);
                    ctx.textAlign = "right";
                    ctx.fillStyle = "white";
                    ctx.font = "bold 15px Arial";
                    const text = names[i];
                    const displayText = text.length > 18 ? text.substring(0, 17) + ".." : text;
                    ctx.fillText(displayText, outsideRadius - 20, 5);
                    ctx.restore();
                }} 
            }}

            function startSpin() {{
                if (!winner) return;
                const winnerIndex = names.indexOf(winner);
                if (winnerIndex === -1) return;
                const anglePerItem = (2 * Math.PI) / names.length;
                const winnerCenterAngle = (winnerIndex * anglePerItem) + (anglePerItem / 2);
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
# 5. TITLE & SUBTITLE
# ============================================
st.markdown("<div class='title-main'>TRAINING SATRIA-1</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Spin Doorprize Random Picker</div>", unsafe_allow_html=True)

# ============================================
# 6. SESSION STATE
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
if "wheel_state" not in st.session_state:
    st.session_state.wheel_state = "idle" 
if "current_winner" not in st.session_state:
    st.session_state.current_winner = ""

# ============================================
# 7. INPUT CARD
# ============================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
names_input = st.text_input("Masukkan daftar nama (pisahkan dengan koma):", key="input_names")
if st.button("Set Daftar Nama"):
    st.session_state.participants = [n.strip() for n in names_input.split(",") if n.strip()]
    st.session_state.winners = []
    st.session_state.preset_index = 0
    st.session_state.wheel_state = "idle"
    st.session_state.current_winner = ""
    st.success("Daftar nama berhasil diperbarui!")
st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# 8. MAIN WHEEL & LOGIC
# ============================================
wheel_placeholder = st.empty()

# Placeholder logic
if len(st.session_state.participants) == 0:
    display_participants = ["SATRIA-1", "DOORPRIZE", "BAKTI", "TRAINING", "SATRIA-1", "DOORPRIZE"]
    is_dummy_wheel = True
else:
    display_participants = st.session_state.participants
    is_dummy_wheel = False

with wheel_placeholder:
    display_winner_arg = st.session_state.current_winner if st.session_state.wheel_state == "spinning" else ""
    spin_wheel_component(display_participants, display_winner_arg)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# 9. CENTERED BUTTON
# ============================================
st.container()
if st.session_state.wheel_state == "idle":
    if st.button("SPIN! 🎉", disabled=is_dummy_wheel): 
        if len(st.session_state.participants) == 0:
            st.error("Masukkan nama peserta terlebih dahulu!")
        else:
            if st.session_state.preset_index < len(st.session_state.preset_winners):
                candidate = st.session_state.preset_winners[st.session_state.preset_index]
                winner = candidate if candidate in st.session_state.participants else random.choice(st.session_state.participants)
                st.session_state.preset_index += 1
            else:
                winner = random.choice(st.session_state.participants)
            st.session_state.current_winner = winner
            st.session_state.wheel_state = "spinning"
            st.rerun()
else:
    if st.button("Lanjut / Simpan Pemenang"):
        if st.session_state.current_winner in st.session_state.participants:
            st.session_state.winners.append(st.session_state.current_winner)
            st.session_state.participants.remove(st.session_state.current_winner)
        st.session_state.wheel_state = "idle"
        st.session_state.current_winner = ""
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================
# 10. BOTTOM LISTS
# ============================================
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
display_list_in_columns("🏆 Pemenang Doorprize (Terbaru Paling Bawah)", st.session_state.winners)
