import streamlit as st
import pandas as pd
import json

# --- 1. CORE FUNCTIONS (Must be at top) ---
def create_week():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return {day: {"PQ": False, "IQ": False, "EQ": False, "SQ": False} for day in days}

# --- 2. PAGE CONFIG & HIGH-CONTRAST UI ---
st.set_page_config(page_title="4Q Mastery Dashboard", layout="wide")

# Using a solid, clean light-grey background for maximum readability
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    
    /* Solid White Cards for Readability */
    .content-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        color: #1E293B;
    }

    /* Clear Typography */
    h1, h2, h3 { color: #0F172A !important; font-family: 'Inter', sans-serif; font-weight: 700; }
    p, span, label { color: #334155 !important; font-size: 1rem; }
    
    /* Interactive Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        height: 45px;
        border: 1px solid #CBD5E1;
        transition: 0.2s;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] { background-color: #1E293B !important; color: white !important; }
    section[data-testid="stSidebar"] * { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if 'all_data' not in st.session_state:
    st.session_state.all_data = {"Week 1": create_week()}
    st.session_state.reflections = {"Week 1": ""}
    st.session_state.goals = {"Week 1": ""}

# --- 4. SIDEBAR NAVIGATION (DEDICATED PAGES) ---
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
    
    st.divider()
    st.subheader("💾 Backup Data")
    full_pkg = {
        "all_data": st.session_state.all_data, 
        "reflections": st.session_state.reflections, 
        "goals": st.session_state.goals
    }
    st.download_button("Export ALL Weeks (.json)", json.dumps(full_pkg), file_name="my_4q_progress.json")

# --- 5. MAIN PAGE CONTENT ---
st.title(f"🚀 Dashboard: {selected_week}")
st.write(f"Tracking your 4Q growth for **{selected_week}**. Switch weeks in the sidebar to see other records.")

# High Contrast Quotient Colors
q_colors = {"PQ": "#DCFCE7", "IQ": "#DBEAFE", "EQ": "#FCE7F3", "SQ": "#F3E8FF"}
q_borders = {"PQ": "#22C55E", "IQ": "#3B82F6", "EQ": "#EC4899", "SQ": "#A855F7"}
q_text = {"PQ": "#166534", "IQ": "#1E40AF", "EQ": "#9D174D", "SQ": "#581C87"}

# --- DAILY LOG SECTION ---
st.subheader("📅 Daily Habit Tracker")
cols = st.columns(7)
week_ref = st.session_state.all_data[selected_week]

for i, day in enumerate(week_ref.keys()):
    with cols[i]:
        st.markdown(f"**{day}**")
        for q in q_colors.keys():
            active = week_ref[day][q]
            # Solid color toggle
            if st.button(f"{'✅ ' if active else ''}{q}", key=f"{selected_week}_{day}_{q}", 
                         type="primary" if active else "secondary"):
                st.session_state.all_data[selected_week][day][q] = not active
                st.rerun()

# --- CALCULATIONS ---
daily_scores = [sum(week_ref[d].values()) for d in week_ref.keys()]
total_pts = sum(daily_scores)
q_totals = {q: sum(week_ref[day][q] for day in week_ref.keys()) for q in q_colors.keys()}

# --- STATS CARDS ---
st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="content-card"><h3>Points</h3><p style="font-size:2rem; font-weight:800;">{total_pts}/28</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="content-card"><h3>Consistency</h3><p style="font-size:2rem; font-weight:800;">{(total_pts/28)*100:.1f}%</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="content-card"><h3>Daily Avg</h3><p style="font-size:2rem; font-weight:800;">{total_pts/7:.1f}</p></div>', unsafe_allow_html=True)

# Quotient Score Tiles
st.subheader("🧬 Quotient Performance")
qtiles = st.columns(4)
for i, q in enumerate(q_colors.keys()):
    with qtiles[i]:
        st.markdown(f"""
            <div style="background-color:{q_colors[q]}; border:2px solid {q_borders[q]}; 
                        padding:20px; border-radius:10px; text-align:center;">
                <b style="color:{q_text[q]}">{q} Mastery</b><br>
                <span style="font-size:1.5rem; font-weight:bold; color:{q_text[q]}">{q_totals[q]}/7</span>
            </div>
        """, unsafe_allow_html=True)

# --- PROGRESS CHART ---
st.subheader("📈 Energy Flow Chart")
st.area_chart(pd.DataFrame({"Daily Score": daily_scores}, index=week_ref.keys()), color="#4F46E5")

# --- REFLECTION & GOALS ---
st.divider()
st.subheader("✍️ Weekly Analysis")

# Auto-Generator Button
if st.button("🪄 Auto-Draft My Reflection"):
    top = max(q_totals, key=q_totals.get)
    low = min(q_totals, key=q_totals.get)
    draft = (f"In {selected_week}, my focus was strongest in {top} ({q_totals[top]}/7), showing high self-discipline. "
             f"However, {low} was my weakest area ({q_totals[low]}/7) due to environmental distractions. "
             f"Overall, scoring {total_pts}/28 highlights a consistency of {(total_pts/28)*100:.0f}%. "
             "I need to take more self-responsibility to balance my Quotients next week.")
    st.session_state.reflections[selected_week] = draft + " " + st.session_state.reflections[selected_week]

g_col, r_col = st.columns([1, 2])
with g_col:
    st.session_state.goals[selected_week] = st.text_area("🎯 Goals for this week:", value=st.session_state.goals[selected_week], height=300)
with r_col:
    refl_input = st.text_area("🧠 Reflection (300+ Words):", value=st.session_state.reflections[selected_week], height=300)
    st.session_state.reflections[selected_week] = refl_input
    word_count = len(refl_input.split())
    if word_count < 300:
        st.error(f"Word Count: {word_count}/300. Write {300-word_count} more words.")
    else:
        st.success(f"Requirement Met! ({word_count} words)")
