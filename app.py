import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import random

# --- SETTINGS & UI STYLING ---
st.set_page_config(page_title="4Q Mastery Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7fb; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #4F46E5; }
    .quote-style { 
        background: white; padding: 20px; border-radius: 15px; 
        border-left: 10px solid #4F46E5; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        font-style: italic; margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
# This allows the app to SAVE data permanently
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        return conn.read(worksheet="Sheet1", ttl="0m")
    except:
        # Initial dummy data if sheet is empty
        return pd.DataFrame([{"Week": "Week 1", "Day": d, "PQ": False, "IQ": False, "EQ": False, "SQ": False} 
                            for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]])

# --- INTERACTIVE SIDEBAR ---
with st.sidebar:
    st.title("🎯 4Q Mastery Pro")
    df = load_data()
    all_weeks = df["Week"].unique().tolist()
    selected_week = st.selectbox("📅 Select Progress Week", all_weeks)
    
    if st.button("➕ Start New Week"):
        new_week_name = f"Week {len(all_weeks) + 1}"
        new_data = pd.DataFrame([{"Week": new_week_name, "Day": d, "PQ": False, "IQ": False, "EQ": False, "SQ": False} 
                                for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]])
        df = pd.concat([df, new_data], ignore_index=True)
        conn.update(worksheet="Sheet1", data=df)
        st.rerun()

# --- DAILY MOTIVATION ---
quotes = [
    "“The successful warrior is the average man, with laser-like focus.” — Bruce Lee",
    "“Discipline is choosing between what you want now and what you want most.”",
    "“Your body is a temple, but keep it as a workshop, not a lumber yard.”"
]
st.markdown(f'<div class="quote-style">{random.choice(quotes)}</div>', unsafe_allow_html=True)

# --- THE INTERACTIVE TRACKER ---
st.subheader(f"Activity Log: {selected_week}")
week_df = df[df["Week"] == selected_week].copy()

# Interactive Grid
edited_week_df = st.data_editor(
    week_df,
    column_config={
        "Week": None, # Hide this column
        "PQ": st.column_config.CheckboxColumn("Physical (PQ)"),
        "IQ": st.column_config.CheckboxColumn("Intellect (IQ)"),
        "EQ": st.column_config.CheckboxColumn("Emotion (EQ)"),
        "SQ": st.column_config.CheckboxColumn("Spirit (SQ)"),
    },
    hide_index=True,
    use_container_width=True
)

# SAVE BUTTON (Interactive UI Logic)
if st.button("💾 Save Progress to Cloud"):
    df.update(edited_week_df)
    conn.update(worksheet="Sheet1", data=df)
    st.success("Week Progress Saved Successfully!")

# --- SMART ANALYTICS ---
numeric_vals = edited_week_df[["PQ", "IQ", "EQ", "SQ"]].astype(int)
daily_scores = numeric_vals.sum(axis=1)
total_score = daily_scores.sum()
consistency = (total_score / 28) * 100

st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("Weekly Completion", f"{total_score}/28")
col2.metric("Consistency Index", f"{consistency:.1f}%")
col3.metric("Daily Score Avg", f"{total_score/7:.2f}")

# Progress Bar Chart
st.subheader("📈 Performance Trend")
st.area_chart(daily_scores, color="#4F46E5")

# --- REFLECTION ---
st.subheader("🧠 Self-Reflection (Min. 300 Words)")
reflection = st.text_area("What did you learn about your discipline this week?", height=250)
word_count = len(reflection.split())
if word_count < 300:
    st.warning(f"Current count: {word_count}. You need {300 - word_count} more words.")
else:
    st.success(f"Requirement Met! ({word_count} words)")
