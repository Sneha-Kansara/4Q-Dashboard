import streamlit as st
import pandas as pd
import json
import plotly.express as px
import random

# --- 1. CORE FUNCTIONS ---
def create_week():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    # Ensure every day and every Q is pre-set to False to prevent KeyErrors
    return {day: {"PQ": False, "IQ": False, "EQ": False, "SQ": False} for day in days}

# --- 2. PAGE CONFIG & FORCED LIGHT THEME ---
st.set_page_config(page_title="4Q Mastery Dashboard", layout="wide")

st.markdown("""
    <style>
    /* Force Light Mode UI */
    .stApp { background-color: #F8FAFC !important; }
    
    /* Text Visibility */
    h1, h2, h3, h4, p, span, label, .stMarkdown {
        color: #1E293B !important;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* Professional Content Cards */
    .section-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Day Column Headers */
    .day-label {
        font-weight: 800 !important;
        color: #334155 !important;
        text-align: center;
        border-bottom: 2px solid #E2E8F0;
        margin-bottom: 10px;
    }

    /* Sidebar Contrast Fix */
    section[data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 2px solid #CBD5E0; }
    section[data-testid="stSidebar"] * { color: #0F172A !important; }
    
    /* Quote Box */
    .quote-box {
        background: #F1F5F9;
        border-left: 4px solid #6366F1;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 4px;
        font-style: italic;
        color: #475569;
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
    st.header("📂 Menu")
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
    st.download_button("💾 Backup Data", json.dumps(full_pkg), file_name="4q_data_export.json")

# --- 5. QUOTE & HEADER ---
quotes = [
    "“Self-responsibility is the bridge to mastery.”",
    "“Measurement is the first step that leads to control and eventually to improvement.”",
    "“Balance is not something you find, it's something you create.”"
]
st.markdown(f'<div class="quote-box">{random.choice(quotes)}</div>', unsafe_allow_html=True)
st.title(f"🚀 {selected_week}: Mastery Report")

# --- SECTION 1: HABIT TRACKER GRID ---
st.markdown('<div class="section-card"><h3>🗓️ 1. Daily Habit Tracker</h3>', unsafe_allow_html=True)
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
qs = ["PQ", "IQ", "EQ", "SQ"]

# Columns for Days
cols = st.columns([1.2] + [1]*7)
cols[0].write("**Quotient**")
for i, day in enumerate(days):
    cols[i+1].markdown(f'<div class="day-label">{day[:3]}</div>', unsafe_allow_html=True)

# Grid Rows
week_ref = st.session_state.all_data[selected_week]
for q in qs:
    row = st.columns([1.2] + [1]*7)
    row[0].write(f"**{q}**")
    for i, day in enumerate(days):
        # SAFETY CHECK: Get value or default to False to prevent KeyError
        active = week_ref.get(day, {}).get(q, False)
        
        btn_label = "✅" if active else "⬜"
        if row[i+1].button(btn_label, key=f"{selected_week}_{day}_{q}", use_container_width=True):
            st.session_state.all_data[selected_week][day][q] = not active
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 2: PERFORMANCE SUMMARY ---
daily_scores = [sum(week_ref.get(d, {}).values()) for d in days]
total_pts = sum(daily_scores)
q_totals = {q: sum(week_ref[day].get(q, False) for day in days) for q in qs}

st.markdown('<div class="section-card"><h3>📊 2. Performance Summary</h3>', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
m1.metric("Total Score", f"{total_pts} / 28")
m2.metric("Consistency", f"{(total_pts/28)*100:.1f}%")
m3.metric("Daily Avg", f"{total_pts/7:.1f}")

st.write("**Q-Wise Performance (Assignment Requirements):**")
q_cols = st.columns(4)
for i, q in enumerate(qs):
    # This clearly shows "X out of 7" as requested
    q_cols[i].info(f"**{q}:** {q_totals[q]} / 7")
st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 3: CHART ---
st.markdown('<div class="section-card"><h3>📈 3. Energy Flow</h3>', unsafe_allow_html=True)
chart_df = pd.DataFrame({"Day": days, "Score": daily_scores})
fig = px.line(chart_df, x="Day", y="Score", text="Score", markers=True)
fig.update_layout(height=300, yaxis=dict(range=[0, 4.5]), paper_bgcolor='white', plot_bgcolor='white', margin=dict(l=10, r=10, t=30, b=10))
fig.update_traces(line_color='#6366F1', marker=dict(size=10))
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 4: REFLECTION & GOALS ---
st.markdown('<div class="section-card"><h3>🧠 4. Weekly Reflection Summary</h3>', unsafe_allow_html=True)

# Goal Input
st.session_state.goals[selected_week] = st.text_input("🎯 Goal for Next Week:", value=st.session_state.goals[selected_week], placeholder="e.g., Achieve 7/7 in EQ")

# Smarter Auto-Draft
if st.button("🪄 Auto-Draft My 300-Word Start"):
    strong = max(q_totals, key=q_totals.get)
    weak = min(q_totals, key=q_totals.get)
    st.session_state.reflections[selected_week] = (
        f"In {selected_week}, my strongest area was {strong} ({q_totals[strong]}/7) while my weakest was {weak} ({q_totals[weak]}/7). "
        "The primary distraction this week was [Add specific distraction here]. "
        f"Next week, my goal is to {st.session_state.goals[selected_week] if st.session_state.goals[selected_week] else 'improve my lowest scores'}. "
        "I am taking self-responsibility for this {(total_pts/28)*100:.0f}% consistency score..."
    )
    st.rerun()

refl_text = st.text_area("Write Summary (Min 300 Words):", value=st.session_state.reflections[selected_week], height=300)
st.session_state.reflections[selected_week] = refl_text

wc = len(refl_text.split())
st.markdown(f"**Word Count:** {wc} / 300")
if wc >= 300: st.success("✅ Requirement Met!")
else: st.warning(f"📝 You need {300-wc} more words.")
st.markdown('</div>', unsafe_allow_html=True)
