import streamlit as st
import pandas as pd
import json
import plotly.express as px  # New library for better charts

# --- 1. CORE FUNCTIONS ---
def create_week():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return {day: {"PQ": False, "IQ": False, "EQ": False, "SQ": False} for day in days}

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="4Q Mastery Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FDFDFD; }
    .content-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #111827 !important; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if 'all_data' not in st.session_state:
    st.session_state.all_data = {"Week 1": create_week()}
    st.session_state.reflections = {"Week 1": ""}
    st.session_state.goals = {"Week 1": ""}

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("📂 Navigation")
    if st.button("➕ Create New Week"):
        nw_id = f"Week {len(st.session_state.all_data) + 1}"
        st.session_state.all_data[nw_id] = create_week()
        st.session_state.reflections[nw_id] = ""
        st.session_state.goals[nw_id] = ""
        st.rerun()
    
    st.divider()
    selected_week = st.radio("Go to Page:", list(st.session_state.all_data.keys()))

# --- 5. MAIN LOGIC ---
st.title(f"🚀 Dashboard: {selected_week}")
week_ref = st.session_state.all_data[selected_week]

# Habit Buttons
cols = st.columns(7)
for i, day in enumerate(week_ref.keys()):
    with cols[i]:
        st.markdown(f"**{day}**")
        for q in ["PQ", "IQ", "EQ", "SQ"]:
            active = week_ref[day][q]
            if st.button(f"{'✅ ' if active else ''}{q}", key=f"{selected_week}_{day}_{q}", 
                         type="primary" if active else "secondary"):
                st.session_state.all_data[selected_week][day][q] = not active
                st.rerun()

# --- 6. CHART UPGRADE (The "Smart" Energy Flow) ---
st.divider()
st.subheader("📈 Energy Flow Analysis")

daily_scores = [sum(week_ref[d].values()) for d in week_ref.keys()]
chart_df = pd.DataFrame({
    "Day": list(week_ref.keys()),
    "Score": daily_scores
})

# Create a Professional Plotly Chart
fig = px.area(chart_df, x="Day", y="Score", 
              markers=True, 
              text="Score", # This shows the data labels on the chart
              title=f"Daily Energy Trend - {selected_week}")

# Change Colors here: 'line_color' and 'fillcolor'
fig.update_traces(
    line_color='#4F46E5', 
    fillcolor='rgba(79, 70, 229, 0.2)', 
    textposition="top center",
    marker=dict(size=10, color='#4F46E5', line=dict(width=2, color='white'))
)

fig.update_layout(
    xaxis_title="Days of the Week",
    yaxis_title="Total Points (0-4)",
    yaxis=dict(range=[0, 4.5], dtick=1),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter", size=14, color="#111827")
)

# Display the high-contrast chart
st.plotly_chart(fig, use_container_width=True)

# --- 7. SUMMARY & REFLECTION ---
total_pts = sum(daily_scores)
st.divider()
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="content-card"><h3>Points</h3><p style="font-size:2rem; font-weight:800;">{total_pts}/28</p></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="content-card"><h3>Consistency</h3><p style="font-size:2rem; font-weight:800;">{(total_pts/28)*100:.1f}%</p></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="content-card"><h3>Daily Avg</h3><p style="font-size:2rem; font-weight:800;">{total_pts/7:.1f}</p></div>', unsafe_allow_html=True)

# Reflection Boxes
g_col, r_col = st.columns([1, 2])
with g_col:
    st.session_state.goals[selected_week] = st.text_area("🎯 Goals:", value=st.session_state.goals[selected_week], height=250)
with r_col:
    refl_input = st.text_area("🧠 Reflection (300+ Words):", value=st.session_state.reflections[selected_week], height=250)
    st.session_state.reflections[selected_week] = refl_input
    wc = len(refl_input.split())
    st.markdown(f"**Word Count:** {wc} / 300")
