import streamlit as st
import pandas as pd
import json
import plotly.express as px
import random

# --- 1. CORE FUNCTIONS ---
def create_week():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return {day: {"PQ": False, "IQ": False, "EQ": False, "SQ": False} for day in days}

# --- 2. PAGE CONFIG & HIGH-VISIBILITY THEME ---
st.set_page_config(page_title="4Q Mastery Dashboard", layout="wide")

st.markdown("""
    <style>
    /* Force Light Theme */
    .stApp { background-color: #F8FAFC !important; }
    
    /* Force All Text to be Solid Black */
    h1, h2, h3, h4, p, span, label, .stMarkdown {
        color: #000000 !important;
        font-family: 'Arial', sans-serif;
    }

    /* Professional Sidebar */
    section[data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 2px solid #CBD5E0; }
    section[data-testid="stSidebar"] * { color: #000000 !important; }

    /* Section Cards */
    .section-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #000000;
        margin-bottom: 20px;
    }

    /* Header Labels for Days */
    .day-header {
        font-weight: bold;
        text-align: center;
        border-bottom: 1px solid #000000;
        padding-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if 'all_data' not in st.session_state:
    st.session_state.all_data = {"Week 1": create_week()}
    st.session_state.reflections = {"Week 1": ""}
    st.session_state.goals = {"Week 1": ""}

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("📂 App Menu")
    if st.button("➕ Create New Week"):
        nw_id = f"Week {len(st.session_state.all_data) + 1}"
        st.session_state.all_data[nw_id] = create_week()
        st.session_state.reflections[nw_id] = ""
        st.session_state.goals[nw_id] = ""
        st.rerun()
    
    selected_week = st.radio("Select Week:", list(st.session_state.all_data.keys()))
    st.divider()
    full_pkg = {"data": st.session_state.all_data, "refl": st.session_state.reflections, "goal": st.session_state.goals}
    st.download_button("💾 Download Data", json.dumps(full_pkg), file_name="4q_mastery_report.json")

# --- 5. QUOTES & TITLE ---
quotes = ["“Self-responsibility is the key.”", "“Measure what matters.”", "“Balance is created.”"]
st.info(random.choice(quotes))
st.title(f"🚀 {selected_week} Performance Summary")

# --- 6. DAILY HABIT TRACKER (FIXED KEYERROR) ---
st.markdown('<div class="section-card"><h3>🗓️ 1. Daily Habit Tracker</h3>', unsafe_allow_html=True)
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
qs = ["PQ", "IQ", "EQ", "SQ"]

week_ref = st.session_state.all_data[selected_week]

cols = st.columns([1.5] + [1]*7)
cols[0].write("**Type**")
for i, day in enumerate(days):
    cols[i+1].markdown(f'<div class="day-header">{day[:3]}</div>', unsafe_allow_html=True)

for q in qs:
    row = st.columns([1.5] + [1]*7)
    row[0].write(f"**{q}**")
    for i, day in enumerate(days):
        # DOUBLE SAFETY: Ensure day and Q exist before reading
        if day not in week_ref: week_ref[day] = {"PQ":False, "IQ":False, "EQ":False, "SQ":False}
        active = week_ref[day].get(q, False)
        
        btn_label = "✅" if active else "⬜"
        if row[i+1].button(btn_label, key=f"{selected_week}_{day}_{q}"):
            st.session_state.all_data[selected_week][day][q] = not active
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- 7. ASSIGNMENT SUMMARY (Points, Consistency, Q-wise) ---
# Calculation with Safety
daily_scores = []
for d in days:
    day_val = week_ref.get(d, {"PQ":False, "IQ":False, "EQ":False, "SQ":False})
    daily_scores.append(sum(day_val.values()))

total_pts = sum(daily_scores)
consistency = (total_pts / 28) * 100

st.markdown('<div class="section-card"><h3>📊 2. Performance Metrics</h3>', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
m1.metric("Total Score", f"{total_pts} / 28")
m2.metric("Consistency", f"{consistency:.1f}%")
m3.metric("Daily Average", f"{total_pts/7:.1f}")

st.write("**Q-Wise Performance (Assignment Criteria):**")
q_sum_cols = st.columns(4)
for i, q in enumerate(qs):
    # Safe counting
    q_count = sum(1 for d in days if week_ref.get(d, {}).get(q, False))
    q_sum_cols[i].success(f"**{q}:** {q_count} / 7")
st.markdown('</div>', unsafe_allow_html=True)

# --- 8. CHART ---
st.markdown('<div class="section-card"><h3>📈 3. Energy Flow Chart</h3>', unsafe_allow_html=True)
chart_df = pd.DataFrame({"Day": days, "Score": daily_scores})
fig = px.line(chart_df, x="Day", y="Score", text="Score", markers=True)
fig.update_layout(height=300, yaxis=dict(range=[0, 4.5]), paper_bgcolor='white', plot_bgcolor='white')
fig.update_traces(line_color='#2563EB', marker=dict(size=10, color='black'))
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 9. REFLECTION SUMMARY (MIN 300 WORDS) ---
st.markdown('<div class="section-card"><h3>🧠 4. Weekly Reflection Summary</h3>', unsafe_allow_html=True)

st.session_state.goals[selected_week] = st.text_input("🎯 Goal for Next Week:", value=st.session_state.goals[selected_week])

if st.button("🪄 Auto-Draft 300 Word Reflection"):
    q_counts = {q: sum(1 for d in days if week_ref.get(d, {}).get(q, False)) for q in qs}
    strong = max(q_counts, key=q_counts.get)
    weak = min(q_counts, key=q_counts.get)
    
    draft = (f"Reflection for {selected_week}:\n\n"
             f"My strongest Quotient was {strong} with {q_counts[strong]}/7, while {weak} was weakest at {q_counts[weak]}/7. "
             "I found that my primary distraction was [Detail Here]. "
             f"Next week, I plan to improve by {st.session_state.goals[selected_week]}. "
             "Taking full self-responsibility, I realize that my consistency of "
             f"{consistency:.0f}% requires more discipline in my daily routine...")
    st.session_state.reflections[selected_week] = draft
    st.rerun()

refl_area = st.text_area("Analysis (Min 300 Words):", value=st.session_state.reflections[selected_week], height=300)
st.session_state.reflections[selected_week] = refl_area
wc = len(refl_area.split())
st.write(f"Current Word Count: **{wc} / 300**")
if wc >= 300: st.success("✅ Requirement Met!")
else: st.warning(f"📝 Write {300-wc} more words.")
st.markdown('</div>', unsafe_allow_html=True)
