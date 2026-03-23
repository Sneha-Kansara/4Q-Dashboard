import streamlit as st
import pandas as pd
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="4Q Mastery Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR BETTER UI ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stTextArea textarea { border-radius: 10px; border: 1px solid #4F46E5; }
    .status-box { padding: 10px; border-radius: 5px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
# This acts as our "In-Web Memory"
if 'all_weeks_data' not in st.session_state:
    def create_empty_week():
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        return {day: {"PQ": False, "IQ": False, "EQ": False, "SQ": False} for day in days}
    
    # Start with Week 1
    st.session_state.all_weeks_data = {"Week 1": create_empty_week()}

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🎯 4Q Mastery")
    st.markdown("---")
    
    # Week Selection
    selected_week = st.selectbox("📅 Select Week", list(st.session_state.all_weeks_data.keys()))
    
    # Add Week Button
    if st.button("➕ Add New Week"):
        new_week_num = len(st.session_state.all_weeks_data) + 1
        st.session_state.all_weeks_data[f"Week {new_week_num}"] = create_empty_week()
        st.rerun()
    
    st.markdown("---")
    st.info("💡 Data is saved in this browser session. Do not refresh to keep progress for 2 weeks!")

# --- TOP SECTION: QUOTE & KPIs ---
st.title(f"🚀 {selected_week} Performance Dashboard")

quotes = [
    "“Discipline is the bridge between goals and accomplishment.”",
    "“Your IQ gets you hired, but your EQ gets you promoted.”",
    "“Self-responsibility is the highest form of human maturity.”",
    "“PQ is the fuel, IQ is the engine, EQ is the driver, SQ is the destination.”"
]
st.warning(f"💡 **Motivation:** {random.choice(quotes)}")

# --- THE INTERACTIVE TRACKER ---
st.subheader("Interactive Habit Log")
current_data = st.session_state.all_weeks_data[selected_week]

# Convert dict to DataFrame for display
df = pd.DataFrame(current_data).T.reset_index().rename(columns={'index': 'Day'})

# The "Smart" Data Editor
edited_df = st.data_editor(
    df,
    column_config={
        "Day": st.column_config.TextColumn("Day", disabled=True),
        "PQ": st.column_config.CheckboxColumn("Physical (PQ)"),
        "IQ": st.column_config.CheckboxColumn("Intelligence (IQ)"),
        "EQ": st.column_config.CheckboxColumn("Emotional (EQ)"),
        "SQ": st.column_config.CheckboxColumn("Spiritual (SQ)"),
    },
    hide_index=True,
    use_container_width=True,
    key="editor"
)

# Sync edits back to session state immediately
for _, row in edited_df.iterrows():
    day = row['Day']
    st.session_state.all_weeks_data[selected_week][day] = {
        "PQ": row['PQ'], "IQ": row['IQ'], "EQ": row['EQ'], "SQ": row['SQ']
    }

# --- CALCULATIONS ---
numeric_df = edited_df.drop(columns=['Day']).astype(int)
daily_scores = numeric_df.sum(axis=1)
total_score = daily_scores.sum()
consistency = (total_score / 28) * 100
avg_day = total_score / 7

# Q-Wise breakdown
q_totals = numeric_df.sum()

# --- ANALYTICS UI ---
st.divider()
c1, c2, c3, c4 = st.columns(4)

c1.metric("Weekly Points", f"{total_score}/28", delta=f"{total_score-14 if total_score > 14 else 0} above pass")
c2.metric("Consistency", f"{consistency:.1f}%")
c3.metric("Daily Avg", f"{avg_day:.1f}")
c4.metric("Top Q", q_totals.idxmax() if total_score > 0 else "N/A")

# --- VISUAL CHART ---
st.subheader("📈 Performance Trend (Daily Score 0-4)")
st.area_chart(daily_scores, color="#4F46E5")

# --- REFLECTION AREA ---
st.divider()
st.subheader("🧠 Weekly Reflection Summary")
st.markdown("*Min. 300 words required for the assignment*")

refl_key = f"refl_{selected_week}"
if refl_key not in st.session_state:
    st.session_state[refl_key] = ""

reflection_text = st.text_area(
    "Analyze your performance, distractions, and improvements:",
    value=st.session_state[refl_key],
    height=300,
    placeholder="Start typing your reflection here...",
    key="refl_input"
)
st.session_state[refl_key] = reflection_text

words = len(reflection_text.split())
progress_color = "red" if words < 300 else "green"
st.markdown(f"**Word Count:** <span style='color:{progress_color}'>{words} / 300</span>", unsafe_allow_html=True)

if words >= 300:
    st.success("✅ Reflection Length Requirement Met!")
else:
    st.info(f"📝 Write {300 - words} more words to complete the assignment.")
