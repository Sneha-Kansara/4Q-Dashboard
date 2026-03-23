import streamlit as st
import pandas as pd
import json
import plotly.express as px

# --- 1. CORE FUNCTIONS (Fixed NameError) ---
def create_week():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return {day: {"PQ": False, "IQ": False, "EQ": False, "SQ": False} for day in days}

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="4Q Mastery Dashboard", layout="wide")

# HIGH-CONTRAST CSS (Max Visibility)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    
    /* Force All Text to Bold Black */
    h1, h2, h3, h4, p, span, label, .stMarkdown {
        color: #000000 !important;
        font-family: 'Arial', sans-serif;
    }

    /* Solid Content Cards */
    .content-card {
        background-color: #F1F5F9;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #000000;
        margin-bottom: 20px;
    }

    /* Day Labels */
    .day-header {
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        color: #000000 !important;
        text-decoration: underline;
    }

    /* Sidebar Background */
    section[data-testid="stSidebar"] { background-color: #0F172A !important; }
    section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
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
    
    selected_week = st.radio("Select Page:", list(st.session_state.all_data.keys()))
    st.divider()
    
    # Export for Submission
    full_pkg = {"data": st.session_state.all_data, "refl": st.session_state.reflections, "goal": st.session_state.goals}
    st.download_button("💾 Export All Data", json.dumps(full_pkg), file_name="4q_final_backup.json")

# --- 5. MAIN TRACKER ---
st.title(f"🚀 Dashboard: {selected_week}")
week_ref = st.session_state.all_data[selected_week]

# HABIT BUTTONS
st.subheader("🗓️ Daily Log")
cols = st.columns(7)
for i, day in enumerate(week_ref.keys()):
    with cols[i]:
        st.markdown(f'<p class="day-header">{day[:3]}</p>', unsafe_allow_html=True)
        for q in ["PQ", "IQ", "EQ", "SQ"]:
            active = week_ref[day][q]
            label = f"✅ {q}" if active else f"⚪ {q}"
            if st.button(label, key=f"{selected_week}_{day}_{q}"):
                st.session_state.all_data[selected_week][day][q] = not active
                st.rerun()

# --- 6. CALCULATIONS & STATS ---
daily_scores = [sum(week_ref[d].values()) for d in week_ref.keys()]
total_pts = sum(daily_scores)
q_totals = {q: sum(week_ref[day][q] for day in week_ref.keys()) for q in ["PQ", "IQ", "EQ", "SQ"]}

st.divider()
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="content-card"><b>Total Score</b><br><span style="font-size:2rem; font-weight:900;">{total_pts}/28</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="content-card"><b>Consistency</b><br><span style="font-size:2rem; font-weight:900;">{(total_pts/28)*100:.1f}%</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="content-card"><b>Daily Avg</b><br><span style="font-size:2rem; font-weight:900;">{total_pts/7:.1f}</span></div>', unsafe_allow_html=True)

# --- 7. ENERGY FLOW CHART (High Contrast) ---
st.subheader("📈 Energy Flow Analysis")
chart_df = pd.DataFrame({"Day": list(week_ref.keys()), "Score": daily_scores})
fig = px.line(chart_df, x="Day", y="Score", text="Score", markers=True)
fig.update_traces(line=dict(color='#FF4B4B', width=4), marker=dict(size=12, color='black'), textposition="top center")
fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color="black", size=14), yaxis=dict(range=[0, 4.5]))
st.plotly_chart(fig, use_container_width=True)

# --- 8. SMARTER MAGIC WAND & REFLECTION ---
st.divider()
st.subheader("🧠 Weekly Analysis")

# THE MAGIC WAND BUTTON
if st.button("🪄 Auto-Draft My Start"):
    strongest = max(q_totals, key=q_totals.get)
    weakest = min(q_totals, key=q_totals.get)
    draft = (f"For {selected_week}, my focus was strongest in {strongest} ({q_totals[strongest]}/7). "
             f"However, {weakest} was my weakest area ({q_totals[weakest]}/7) due to distractions. "
             f"Overall, scoring {total_pts}/28 highlights a consistency of {(total_pts/28)*100:.0f}%. "
             "I need to take more self-responsibility to balance my Quotients next week.")
    st.session_state.reflections[selected_week] = draft
    st.rerun()

g_col, r_col = st.columns([1, 2])
with g_col:
    st.session_state.goals[selected_week] = st.text_area("🎯 Weekly Goals:", value=st.session_state.goals[selected_week], height=300)
with r_col:
    refl_input = st.text_area("✍️ Reflection (Min 300 words):", value=st.session_state.reflections[selected_week], height=300)
    st.session_state.reflections[selected_week] = refl_input
    wc = len(refl_input.split())
    st.write(f"Word Count: **{wc} / 300**")
    if wc >= 300: st.success("✅ Length Goal Met!")
    else: st.warning(f"📝 You need {300-wc} more words.")
