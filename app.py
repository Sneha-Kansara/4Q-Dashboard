import streamlit as st
import pandas as pd
import json
import plotly.express as px
import random

# --- 1. CORE FUNCTIONS ---
def create_week():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return {day: {"PQ": False, "IQ": False, "EQ": False, "SQ": False} for day in days}

# --- 2. PAGE CONFIG & FORCED LIGHT THEME ---
st.set_page_config(page_title="4Q Mastery Dashboard", layout="wide")

# Strong CSS to fix visibility issues
st.markdown("""
    <style>
    /* Force background and text colors */
    .stApp { background-color: #F4F7F9 !important; }
    
    /* Force All Text to be Black for readability */
    h1, h2, h3, h4, p, span, label, .stMarkdown {
        color: #1A202C !important;
        font-family: 'Inter', sans-serif;
    }

    /* Fix Sidebar visibility */
    section[data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 2px solid #E2E8F0; }
    section[data-testid="stSidebar"] * { color: #1A202C !important; }

    /* Fix Button Colors (Make them stand out) */
    .stButton>button {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
        border: 2px solid #CBD5E0 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    
    /* Card styling */
    .section-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Quote Styling */
    .quote-box {
        background-color: #EDF2F7;
        padding: 15px;
        border-left: 5px solid #3182CE;
        font-style: italic;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if 'all_data' not in st.session_state:
    st.session_state.all_data = {"Week 1": create_week()}
    st.session_state.reflections = {"Week 1": ""}
    st.session_state.goals = {"Week 1": ""}

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.header("📂 Navigation")
    if st.button("➕ Create New Week"):
        nw_id = f"Week {len(st.session_state.all_data) + 1}"
        st.session_state.all_data[nw_id] = create_week()
        st.session_state.reflections[nw_id] = ""
        st.session_state.goals[nw_id] = ""
        st.rerun()
    
    selected_week = st.radio("Switch Week Page:", list(st.session_state.all_data.keys()))
    st.divider()
    
    # Save Feature
    full_pkg = {"data": st.session_state.all_data, "refl": st.session_state.reflections, "goal": st.session_state.goals}
    st.download_button("💾 Save My Progress", json.dumps(full_pkg), file_name="4q_data.json")

# --- 5. DAILY QUOTE ---
quotes = [
    "“Self-responsibility is the first step toward personal mastery.”",
    "“What you measure, you improve.”",
    "“Discipline is the bridge between goals and accomplishment.”",
    "“Your energy flows where your attention goes.”"
]
st.markdown(f'<div class="quote-box">{random.choice(quotes)}</div>', unsafe_allow_html=True)

# --- 6. MAIN CONTENT ---
week_ref = st.session_state.all_data[selected_week]
st.title(f"🚀 {selected_week} Performance Tracker")

# --- SECTION 1: HABIT TRACKER GRID ---
st.markdown('<div class="section-card"><h3>🗓️ 1. Weekly Habit Log</h3>', unsafe_allow_html=True)
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
qs = ["PQ", "IQ", "EQ", "SQ"]

# Creating a Header Row for Days
cols = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1])
cols[0].write("**Quotient**")
for i, day in enumerate(days):
    cols[i+1].write(f"**{day[:3]}**")

# Creating Rows for PQ, IQ, EQ, SQ
for q in qs:
    row = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1])
    row[0].write(f"**{q}**")
    for i, day in enumerate(days):
        active = week_ref[day][q]
        # Using a toggle button for better visibility
        if row[i+1].button("ON" if active else "OFF", key=f"{selected_week}_{day}_{q}"):
            week_ref[day][q] = not active
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 2: PERFORMANCE SUMMARY ---
daily_scores = [sum(week_ref[d].values()) for d in days]
total_pts = sum(daily_scores)
q_totals = {q: sum(week_ref[day][q] for day in days) for q in qs}

st.markdown('<div class="section-card"><h3>📊 2. Performance Summary</h3>', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
m1.metric("Total Score", f"{total_pts} / 28")
m2.metric("Consistency", f"{(total_pts/28)*100:.1f}%")
m3.metric("Daily Avg", f"{total_pts/7:.1f}")

st.write("**Q-Wise Performance (Assignment Requirement):**")
q_cols = st.columns(4)
for i, q in enumerate(qs):
    q_cols[i].info(f"**{q}:** {q_totals[q]} / 7")
st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 3: CHART ---
st.markdown('<div class="section-card"><h3>📈 3. Energy Flow</h3>', unsafe_allow_html=True)
chart_df = pd.DataFrame({"Day": days, "Score": daily_scores})
fig = px.line(chart_df, x="Day", y="Score", text="Score", markers=True)
fig.update_layout(height=300, yaxis=dict(range=[0, 4.5]), paper_bgcolor='white', plot_bgcolor='white')
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 4: REFLECTION & GOALS ---
st.markdown('<div class="section-card"><h3>🧠 4. Weekly Reflection & Goals</h3>', unsafe_allow_html=True)

# Goal Setting
st.session_state.goals[selected_week] = st.text_input("🎯 Goal for Next Week:", value=st.session_state.goals[selected_week])

# Smarter Auto-Draft
if st.button("🪄 Auto-Draft 300 Word Reflection", use_container_width=True):
    strong = max(q_totals, key=q_totals.get)
    weak = min(q_totals, key=q_totals.get)
    st.session_state.reflections[selected_week] = (
        f"During {selected_week}, my strongest area was {strong} ({q_totals[strong]}/7) and my weakest was {weak} ({q_totals[weak]}/7). "
        "I realized that my biggest distraction was [Detail here] which affected my scores on Wednesday. "
        "Next week, I will prioritize my SQ to ensure a better balance. Achieving a consistency of "
        f"{(total_pts/28)*100:.0f}% has shown me that I need more self-discipline to reach my full potential."
    )
    st.rerun()

refl_text = st.text_area("Analysis (Min 300 Words):", value=st.session_state.reflections[selected_week], height=250)
st.session_state.reflections[selected_week] = refl_text

wc = len(refl_text.split())
st.write(f"Word Count: **{wc} / 300**")
if wc >= 300: st.success("✅ Minimum Word Count Met!")
else: st.warning(f"⚠️ You need {300-wc} more words.")
st.markdown('</div>', unsafe_allow_html=True)
