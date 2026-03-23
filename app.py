import streamlit as st
import pandas as pd
import json
import plotly.express as px

# --- 1. CORE FUNCTIONS ---
def create_week():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return {day: {"PQ": False, "IQ": False, "EQ": False, "SQ": False} for day in days}

# --- 2. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="4Q Mastery Dashboard", layout="wide")

# Theme Colors based on Week
if 'selected_week' not in st.session_state:
    st.session_state.selected_week = "Week 1"

themes = {
    "Week 1": {"bg": "#F0F4F8", "accent": "#3B82F6"}, # Blueish
    "Week 2": {"bg": "#F0FFF4", "accent": "#10B981"}, # Greenish
    "Week 3": {"bg": "#FFF5F5", "accent": "#EF4444"}, # Redish
}
current_theme = themes.get(st.session_state.selected_week, themes["Week 1"])

st.markdown(f"""
    <style>
    .stApp {{ background-color: {current_theme['bg']}; }}
    
    /* Clean Cards */
    .section-card {{
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
        color: #1A202C;
    }}
    
    /* Text Fixes */
    h1 {{ font-size: 24px !important; color: #1A202C !important; font-weight: 800; }}
    h3 {{ font-size: 18px !important; color: #2D3748 !important; margin-bottom: 10px; }}
    p, span, label {{ color: #4A5568 !important; font-size: 14px !important; }}
    
    /* Sidebar Fix */
    section[data-testid="stSidebar"] {{ background-color: #FFFFFF !important; border-right: 1px solid #CBD5E0; }}
    section[data-testid="stSidebar"] * {{ color: #1A202C !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if 'all_data' not in st.session_state:
    st.session_state.all_data = {"Week 1": create_week()}
    st.session_state.reflections = {"Week 1": ""}
    st.session_state.goals = {"Week 1": ""}

# --- 4. SIDEBAR (NAVIGATION) ---
with st.sidebar:
    st.title("📂 Navigation")
    if st.button("➕ Create New Week"):
        nw_id = f"Week {len(st.session_state.all_data) + 1}"
        st.session_state.all_data[nw_id] = create_week()
        st.session_state.reflections[nw_id] = ""
        st.session_state.goals[nw_id] = ""
        st.rerun()
    
    st.session_state.selected_week = st.radio("Switch Week Page:", list(st.session_state.all_data.keys()))
    st.divider()
    
    # Save Feature
    full_pkg = {"data": st.session_state.all_data, "refl": st.session_state.reflections, "goal": st.session_state.goals}
    st.download_button("💾 Save All Data", json.dumps(full_pkg), file_name="4q_data.json")

# --- 5. MAIN CONTENT ---
week_ref = st.session_state.all_data[st.session_state.selected_week]
st.title(f"📊 {st.session_state.selected_week} Performance Tracker")

# --- SECTION 1: HABIT TRACKER GRID ---
st.markdown('<div class="section-card"><h3>🗓️ 1. Weekly Habit Log</h3>', unsafe_allow_html=True)
# Using a table-like layout for PQ/IQ/EQ/SQ
header_cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
qs = ["PQ", "IQ", "EQ", "SQ"]

# Render Grid
for q in qs:
    row_cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
    row_cols[0].markdown(f"**{q}**")
    for i, day in enumerate(days):
        active = week_ref[day][q]
        if row_cols[i+1].checkbox("", value=active, key=f"{st.session_state.selected_week}_{day}_{q}"):
            week_ref[day][q] = True
        else:
            week_ref[day][q] = False
st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 2: PERFORMANCE SUMMARY ---
daily_scores = [sum(week_ref[d].values()) for d in days]
total_pts = sum(daily_scores)
q_totals = {q: sum(week_ref[day][q] for day in days) for q in qs}
consistency = (total_pts / 28) * 100

st.markdown('<div class="section-card"><h3>📊 2. Performance Summary</h3>', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
m1.metric("Total Score", f"{total_pts} / 28")
m2.metric("Consistency", f"{consistency:.1f}%")
m3.metric("Daily Avg", f"{total_pts/7:.1f}")

st.markdown("**Q-Wise Performance (Requirement Met):**")
q_cols = st.columns(4)
for i, q in enumerate(qs):
    q_cols[i].info(f"**{q}:** {q_totals[q]}/7")
st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 3: CHART ---
st.markdown('<div class="section-card"><h3>📈 3. Energy Flow</h3>', unsafe_allow_html=True)
chart_df = pd.DataFrame({"Day": days, "Score": daily_scores})
fig = px.line(chart_df, x="Day", y="Score", text="Score", markers=True)
fig.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20), yaxis=dict(range=[0, 4.5]))
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 4: REFLECTION & GOALS ---
st.markdown('<div class="section-card"><h3>🧠 4. Weekly Reflection & Goals</h3>', unsafe_allow_html=True)

# Goal Setting (Added back)
st.session_state.goals[st.session_state.selected_week] = st.text_input("🎯 Next Week Goal:", value=st.session_state.goals[st.session_state.selected_week])

# Auto-Draft Magic Wand
if st.button("🪄 Auto-Draft 300 Word Reflection"):
    strong = max(q_totals, key=q_totals.get)
    weak = min(q_totals, key=q_totals.get)
    st.session_state.reflections[st.session_state.selected_week] = (
        f"In {st.session_state.selected_week}, my strongest area was {strong} ({q_totals[strong]}/7) while my weakest was {weak} ({q_totals[weak]}/7). "
        "The primary distraction this week was [Insert distraction here]. "
        "To improve next week, I plan to focus on [Insert plan here]. "
        "Consistency is the path to mastery, and I am taking full responsibility for my growth..."
    )

refl_text = st.text_area("Analysis (Min 300 Words):", value=st.session_state.reflections[st.session_state.selected_week], height=250)
st.session_state.reflections[st.session_state.selected_week] = refl_text

wc = len(refl_text.split())
st.write(f"**Word Count:** {wc} / 300")
if wc >= 300: st.success("✅ Minimum Word Count Met!")
else: st.warning("⚠️ Keep writing to reach 300 words.")
st.markdown('</div>', unsafe_allow_html=True)
