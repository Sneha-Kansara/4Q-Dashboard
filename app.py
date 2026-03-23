import streamlit as st
import pandas as pd
import json

# --- 1. CORE FUNCTIONS ---
def create_week():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return {day: {"PQ": False, "IQ": False, "EQ": False, "SQ": False} for day in days}

# --- 2. PRETTY UI CONFIG ---
st.set_page_config(page_title="4Q Mastery Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); }
    .glass-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .metric-val { color: #0f172a; font-size: 2.2rem; font-weight: 800; }
    .stButton>button { border-radius: 10px; font-weight: 600; height: 42px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if 'all_data' not in st.session_state:
    st.session_state.all_data = {"Week 1": create_week()}
    st.session_state.reflections = {"Week 1": ""}
    st.session_state.goals = {"Week 1": ""}

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🎛️ App Menu")
    if st.button("✨ Add New Week"):
        nw = f"Week {len(st.session_state.all_data) + 1}"
        st.session_state.all_data[nw] = create_week()
        st.session_state.reflections[nw] = ""
        st.session_state.goals[nw] = ""
        st.rerun()
    
    selected_week = st.selectbox("📅 Select Week", list(st.session_state.all_data.keys()))
    st.divider()
    save_pkg = {"all_data": st.session_state.all_data, "reflections": st.session_state.reflections, "goals": st.session_state.goals}
    st.download_button("💾 Export All Data", json.dumps(save_pkg), file_name="4q_mastery_backup.json")

# --- 5. MAIN TRACKER ---
st.title(f"🚀 {selected_week} Performance")

q_colors = {"PQ": "#dcfce7", "IQ": "#dbeafe", "EQ": "#fce7f3", "SQ": "#f3e8ff"}
q_text = {"PQ": "#166534", "IQ": "#1e40af", "EQ": "#9d174d", "SQ": "#5b21b6"}

cols = st.columns(7)
curr_week = st.session_state.all_data[selected_week]

for i, day in enumerate(curr_week.keys()):
    with cols[i]:
        st.markdown(f"**{day}**")
        for q in q_colors.keys():
            active = curr_week[day][q]
            if st.button(f"{'✓ ' if active else ''}{q}", key=f"{selected_week}_{day}_{q}", type="primary" if active else "secondary"):
                st.session_state.all_data[selected_week][day][q] = not active
                st.rerun()

# --- 6. CALCULATIONS & SUMMARY ---
daily_sums = [sum(curr_week[d].values()) for d in curr_week.keys()]
total = sum(daily_sums)
const = (total / 28) * 100
q_scores = {q: sum(curr_week[day][q] for day in curr_week.keys()) for q in q_colors.keys()}

st.divider()
m1, m2, m3 = st.columns(3)
with m1: st.markdown(f'<div class="glass-card"><p>Total Points</p><p class="metric-val">{total}/28</p></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="glass-card"><p>Consistency</p><p class="metric-val">{const:.1f}%</p></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="glass-card"><p>Avg Daily</p><p class="metric-val">{total/7:.1f}</p></div>', unsafe_allow_html=True)

q_cols = st.columns(4)
for i, (q, color) in enumerate(q_colors.items()):
    with q_cols[i]:
        st.markdown(f'<div style="background:{color}; padding:20px; border-radius:12px; color:{q_text[q]}; text-align:center; font-weight:bold;">{q}<br><span style="font-size:24px;">{q_scores[q]}/7</span></div>', unsafe_allow_html=True)

st.area_chart(pd.DataFrame({"Score": daily_sums}, index=curr_week.keys()), color="#6366f1")

# --- 7. AUTO-REFLECTION GENERATOR ---
st.divider()
st.subheader("🧠 Reflection & Analysis")

# Generator Logic
if st.button("🪄 Generate Reflection Draft"):
    strongest = max(q_scores, key=q_scores.get)
    weakest = min(q_scores, key=q_scores.get)
    
    draft = f"During {selected_week}, my performance data reveals that my strongest area was {strongest} with a score of {q_scores[strongest]}/7. This suggests that my discipline in this area is becoming a natural habit. Conversely, my weakest area was {weakest} at {q_scores[weakest]}/7. This imbalance indicates that my daily distractions often compromise my {weakest} growth, highlighting a need for better self-responsibility. Achieving a total score of {total}/28 shows that I am {const:.1f}% consistent, but there is significant room to improve my daily focus..."
    st.session_state.reflections[selected_week] = draft + " " + st.session_state.reflections[selected_week]

g_col, r_col = st.columns([1, 2])
with g_col:
    st.session_state.goals[selected_week] = st.text_area("🎯 Weekly Goals:", value=st.session_state.goals[selected_week], height=300)
with r_col:
    refl_input = st.text_area("✍️ Reflection (Min 300 words):", value=st.session_state.reflections[selected_week], height=300)
    st.session_state.reflections[selected_week] = refl_input
    wc = len(refl_input.split())
    st.markdown(f"**Word Count:** {wc} / 300")
    if wc >= 300: st.success("✅ Requirement Met!")
    else: st.warning(f"📝 Write {300-wc} more words.")
