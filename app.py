import streamlit as st
import pandas as pd
import json

# --- SETTINGS & BEAUTIFICATION ---
st.set_page_config(page_title="4Q Mastery", layout="wide")

# Custom CSS for a "Premium App" Aesthetic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F0F2F5; }
    
    .main-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 20px;
    }
    
    .q-tag {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        font-size: 12px;
        margin-bottom: 10px;
    }
    
    .stButton>button {
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
        height: 50px;
        width: 100%;
    }
    
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- DATA STATE ---
if 'data' not in st.session_state:
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    st.session_state.data = {day: {"PQ": False, "IQ": False, "EQ": False, "SQ": False} for day in days}
    st.session_state.reflection = ""

# --- HEADER & QUOTE ---
st.title("✨ 4Q Aesthetic Growth")
st.markdown("> *“The quality of your life is defined by the balance of your 4 Quotients.”*")

# --- INTERACTIVE SMART GRID ---
st.subheader("🗓️ Weekly Rituals")
cols = st.columns(7)
days_list = list(st.session_state.data.keys())

# Define Colors for each Q
q_styles = {
    "PQ": "#10B981", # Green
    "IQ": "#3B82F6", # Blue
    "EQ": "#EC4899", # Pink
    "SQ": "#8B5CF6"  # Purple
}

for i, day in enumerate(days_list):
    with cols[i]:
        st.markdown(f"### {day}")
        for q, color in q_styles.items():
            is_active = st.session_state.data[day][q]
            # Use a unique button for each habit
            if st.button(f"{q}", key=f"{day}_{q}", 
                         type="primary" if is_active else "secondary", 
                         help=f"Mark {q} for {day}"):
                st.session_state.data[day][q] = not is_active
                st.rerun()

# --- CALCULATIONS (THE MATH) ---
total_score = sum(sum(d.values()) for d in st.session_state.data.values())
consistency = (total_score / 28) * 100
avg_day = total_score / 7
q_scores = {q: sum(st.session_state.data[day][q] for day in days_list) for q in q_styles.keys()}

# --- PERFORMANCE SUMMARY (AESTHETIC CARDS) ---
st.divider()
st.subheader("📊 Performance Analytics")
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(f'<div class="main-card"><p>Total Score</p><h2>{total_score} / 28</h2></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="main-card"><p>Consistency</p><h2>{consistency:.1f}%</h2></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="main-card"><p>Daily Avg</p><h2>{avg_per_day:.1f}</h2></div>', unsafe_allow_html=True)

# Q-Wise Performance
st.markdown("#### Quotient Mastery")
q_cols = st.columns(4)
for i, (q, color) in enumerate(q_styles.items()):
    score = q_scores[q]
    with q_cols[i]:
        st.markdown(f"""
            <div style="background:{color}; padding:15px; border-radius:15px; color:white; text-align:center;">
                <small>{q} Balance</small>
                <h3 style="margin:0;">{score}/7</h3>
            </div>
        """, unsafe_allow_html=True)

# --- PROGRESS CHART ---
st.subheader("📈 Energy Trend")
chart_data = pd.DataFrame({
    "Day": days_list,
    "Score": [sum(st.session_state.data[day].values()) for day in days_list]
})
st.area_chart(chart_data.set_index("Day"), color="#6366F1")

# --- REFLECTION & SAVE ---
st.divider()
st.subheader("🧠 Weekly Reflection Summary")
st.session_state.reflection = st.text_area("Write minimum 300 words...", value=st.session_state.reflection, height=250)

# Export Functionality
json_str = json.dumps({"data": st.session_state.data, "refl": st.session_state.reflection})
st.download_button("💾 Save Progress (Download File)", json_str, file_name="my_4q_data.json")

# Word count logic
words = len(st.session_state.reflection.split())
if words < 300:
    st.warning(f"Word Count: {words}/300. You need {300-words} more to meet assignment criteria.")
else:
    st.success("✅ Requirement Met!")
