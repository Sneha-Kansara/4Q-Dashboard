import streamlit as st
import pandas as pd
import json
import random

# --- 1. PAGE SETUP & PASTEL CSS ---
st.set_page_config(page_title="✨ 4Q Pastel Mastery", layout="wide")

st.markdown("""
    <style>
    /* Main Background - Soft Pastel Gradient */
    .stApp {
        background: linear-gradient(135deg, #E0C3FC 0%, #8EC5FC 100%);
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 8px 32px 0 rgba(135, 150, 235, 0.2);
        margin-bottom: 20px;
    }

    /* Metric Styling */
    .metric-text { color: #5D5D9D; font-weight: bold; font-size: 1.2rem; }
    .metric-val { color: #4A4A8A; font-size: 2.2rem; font-weight: 800; }
    
    /* Button Customization */
    .stButton>button {
        border-radius: 15px;
        border: none;
        height: 45px;
        width: 100%;
        font-weight: bold;
        transition: 0.3s;
    }
    
    /* Headers */
    h1, h2, h3 { color: #4A4A8A !important; font-family: 'Quicksand', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SMART DATA STATE ---
if 'all_data' not in st.session_state:
    def create_week():
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        return {day: {"PQ": False, "IQ": False, "EQ": False, "SQ": False} for day in days}
    st.session_state.all_data = {"Week 1": create_week()}
    st.session_state.reflections = {"Week 1": ""}
    st.session_state.goals = {"Week 1": ""}

# --- 3. SIDEBAR (NAVIGATION & DATA) ---
with st.sidebar:
    st.markdown("### 🌸 Menu")
    if st.button("✨ Add New Week"):
        nw = f"Week {len(st.session_state.all_data) + 1}"
        st.session_state.all_data[nw] = create_week()
        st.session_state.reflections[nw] = ""
        st.session_state.goals[nw] = ""
        st.rerun()
    
    selected_week = st.selectbox("📅 View Progress", list(st.session_state.all_data.keys()))
    
    st.divider()
    st.markdown("### 📂 Storage")
    save_pkg = {"all_data": st.session_state.all_data, "reflections": st.session_state.reflections, "goals": st.session_state.goals}
    st.download_button("☁️ Export Data", json.dumps(save_pkg), file_name="4q_pastel_backup.json")
    
    up_file = st.file_uploader("🌸 Import Data", type="json")
    if up_file:
        loaded = json.load(up_file)
        st.session_state.all_data, st.session_state.reflections, st.session_state.goals = loaded["all_data"], loaded["reflections"], loaded["goals"]
        st.rerun()

# --- 4. THE UI LAYOUT ---
st.title(f"🌈 {selected_week}: 4Q Mastery")
st.markdown("*“Self-responsibility is the path to freedom.”*")

# Color Palette for Qs
q_colors = {"PQ": "#A7F3D0", "IQ": "#BFDBFE", "EQ": "#FBCFE8", "SQ": "#DDD6FE"} # Pastel Green, Blue, Pink, Purple

# --- DAILY INTERACTIVE LOG ---
st.markdown("### ✍️ Daily Log")
cols = st.columns(7)
curr_week = st.session_state.all_data[selected_week]

for i, day in enumerate(curr_week.keys()):
    with cols[i]:
        st.markdown(f"**{day}**")
        for q, color in q_colors.items():
            active = curr_week[day][q]
            if st.button(f"{q}", key=f"{selected_week}_{day}_{q}", 
                         type="primary" if active else "secondary"):
                st.session_state.all_data[selected_week][day][q] = not active
                st.rerun()

# --- PERFORMANCE SUMMARY ---
st.divider()
daily_sums = [sum(curr_week[d].values()) for d in curr_week.keys()]
total = sum(daily_sums)
const = (total / 28) * 100
avg = total / 7

st.markdown("### 📊 Performance Summary")
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="glass-card"><p class="metric-text">Total Score</p><p class="metric-val">{total}/28</p></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="glass-card"><p class="metric-text">Consistency</p><p class="metric-val">{const:.1f}%</p></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="glass-card"><p class="metric-text">Daily Average</p><p class="metric-val">{avg:.1f}</p></div>', unsafe_allow_html=True)

# Q-Wise Performance Tiles
st.markdown("#### 🧬 Quotient Mastery (Out of 7)")
q_cols = st.columns(4)
for i, (q, color) in enumerate(q_colors.items()):
    q_total = sum(curr_week[day][q] for day in curr_week.keys())
    with q_cols[i]:
        st.markdown(f"""
            <div style="background:{color}; padding:20px; border-radius:20px; color:#4A4A8A; text-align:center; border: 2px solid white;">
                <b>{q}</b><br><span style="font-size:28px; font-weight:bold;">{q_total}/7</span>
            </div>
        """, unsafe_allow_html=True)

# Progress Chart
st.subheader("📈 Energy Flow")
st.area_chart(pd.DataFrame({"Score": daily_sums}, index=curr_week.keys()), color="#8B5CF6")

# --- NEW: GOAL SETTING & REFLECTION ---
st.divider()
c_goal, c_refl = st.columns([1, 2])

with c_goal:
    st.subheader("🎯 Weekly Goals")
    goal_text = st.text_area("What are you improving?", 
                             value=st.session_state.goals[selected_week], 
                             height=320, key=f"goal_{selected_week}")
    st.session_state.goals[selected_week] = goal_text

with c_refl:
    st.subheader("🧠 Reflection Summary")
    refl_text = st.text_area("Min. 300 words (Strongest, Weakest, Distractions...)", 
                             value=st.session_state.reflections[selected_week], 
                             height=320, key=f"refl_{selected_week}")
    st.session_state.reflections[selected_week] = refl_text
    wc = len(refl_text.split())
    if wc < 300: st.warning(f"📝 {wc}/300 words")
    else: st.success("✅ Length Goal Met!")
