import streamlit as st
import pandas as pd
import json
import plotly.express as px

# --- 1. CORE FUNCTIONS ---
def create_week():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return {day: {"PQ": False, "IQ": False, "EQ": False, "SQ": False} for day in days}

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="4Q Mastery Assignment", layout="wide")

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
    
    selected_week = st.radio("Switch Week Page:", list(st.session_state.all_data.keys()))
    st.divider()
    full_pkg = {"data": st.session_state.all_data, "refl": st.session_state.reflections, "goal": st.session_state.goals}
    st.download_button("💾 Save All Progress", json.dumps(full_pkg), file_name="4q_assignment_data.json")

# --- 5. DYNAMIC THEME ENGINE ---
# This changes the background color based on the week selected
themes = {
    "Week 1": "#EBF8FF", # Light Blue
    "Week 2": "#F0FFF4", # Light Green
    "Week 3": "#FFF5F7", # Light Pink
    "Week 4": "#FAF5FF"  # Light Purple
}
current_bg = themes.get(selected_week, "#F7FAFC")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {current_bg} !important; }}
    .section-box {{
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #2D3748;
        margin-bottom: 25px;
        color: black !important;
    }}
    h1, h2, h3, p, span {{ color: #1A202C !important; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. MAIN CONTENT ---
st.title(f"🚀 {selected_week} Mastery Dashboard")

week_ref = st.session_state.all_data[selected_week]

# SECTION A: DAILY HABIT TRACKER
st.markdown('<div class="section-box"><h3>🗓️ 1. Daily Habit Tracker (PQ, IQ, EQ, SQ)</h3>', unsafe_allow_html=True)
cols = st.columns(7)
for i, day in enumerate(week_ref.keys()):
    with cols[i]:
        st.markdown(f"**{day[:3]}**")
        for q in ["PQ", "IQ", "EQ", "SQ"]:
            active = week_ref[day][q]
            label = f"✅ {q}" if active else f"⬜ {q}"
            if st.button(label, key=f"{selected_week}_{day}_{q}"):
                st.session_state.all_data[selected_week][day][q] = not active
                st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# CALCULATIONS
daily_scores = [sum(week_ref[d].values()) for d in week_ref.keys()]
total_pts = sum(daily_scores)
q_totals = {q: sum(week_ref[day][q] for day in week_ref.keys()) for q in ["PQ", "IQ", "EQ", "SQ"]}
consistency = (total_pts / 28) * 100
avg_day = total_pts / 7

# SECTION B: PERFORMANCE SUMMARY (AS REQUESTED IN ASSIGNMENT)
st.markdown('<div class="section-box"><h3>📊 2. Performance Summary</h3>', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
m1.metric("Total Score", f"{total_pts} / 28")
m2.metric("Consistency", f"{consistency:.1f}%")
m3.metric("Average per Day", f"{avg_day:.1f}")

st.markdown("#### Q-Wise Performance (Out of 7)")
q_cols = st.columns(4)
for i, q in enumerate(["PQ", "IQ", "EQ", "SQ"]):
    q_cols[i].info(f"**{q}:** {q_totals[q]} out of 7")
st.markdown('</div>', unsafe_allow_html=True)

# SECTION C: ENERGY FLOW CHART
st.markdown('<div class="section-box"><h3>📈 3. Energy Flow Chart</h3>', unsafe_allow_html=True)
chart_df = pd.DataFrame({"Day": list(week_ref.keys()), "Score": daily_scores})
fig = px.line(chart_df, x="Day", y="Score", text="Score", markers=True)
fig.update_layout(yaxis=dict(range=[0, 4.5]), plot_bgcolor='white')
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# SECTION D: WEEKLY REFLECTION (MIN 300 WORDS)
st.markdown('<div class="section-box"><h3>🧠 4. Weekly Reflection Summary</h3>', unsafe_allow_html=True)

# THE AUTO-DRAFT BUTTON (Smarter Analysis)
if st.button("🪄 CLICK HERE: Auto-Draft Reflection"):
    strongest = max(q_totals, key=q_totals.get)
    weakest = min(q_totals, key=q_totals.get)
    draft = (f"Reflection for {selected_week}:\n\n"
             f"1. Strongest Q: My strongest area was {strongest} with {q_totals[strongest]}/7 points.\n"
             f"2. Weakest Q: My weakest area was {weakest} with {q_totals[weakest]}/7 points.\n"
             f"3. Distractions: I noticed that I got distracted by... [Add your details here]\n"
             f"4. Improvements: Next week, I plan to improve my {weakest} by... [Add your details here]\n\n"
             "Achieving a total score of {total_pts}/28 taught me that self-responsibility is key...")
    st.session_state.reflections[selected_week] = draft
    st.rerun()

refl_text = st.text_area("Write your 300 words here:", value=st.session_state.reflections[selected_week], height=350)
st.session_state.reflections[selected_week] = refl_text

wc = len(refl_text.split())
if wc < 300:
    st.error(f"⚠️ Current Word Count: {wc} / 300. You need {300-wc} more words to pass.")
else:
    st.success(f"✅ Requirement Met! Word Count: {wc}")
st.markdown('</div>', unsafe_allow_html=True)
