import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="4Q Habit Dashboard", layout="wide")

st.title("🚀 4Q Habit Dashboard")
st.markdown("Track your Physical (PQ), Intellectual (IQ), Emotional (EQ), and Spiritual (SQ) growth.")

# Initialize Data in Session State (to keep it while clicking)
if 'df' not in st.session_state:
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    st.session_state.df = pd.DataFrame({
        "Day": days,
        "PQ": [False]*7, "IQ": [False]*7, "EQ": [False]*7, "SQ": [False]*7
    })

# --- UI: The Input Table ---
st.subheader("Weekly Tracker")
st.info("Check the boxes below to mark your habits as complete.")

# Use data_editor to make it interactive
edited_df = st.data_editor(
    st.session_state.df, 
    hide_index=True,
    column_config={
        "PQ": st.column_config.CheckboxColumn("PQ (Physical)"),
        "IQ": st.column_config.CheckboxColumn("IQ (Intellectual)"),
        "EQ": st.column_config.CheckboxColumn("EQ (Emotional)"),
        "SQ": st.column_config.CheckboxColumn("SQ (Spiritual)"),
    },
    disabled=["Day"],
    use_container_width=True
)
st.session_state.df = edited_df

# --- Calculations ---
# Convert Booleans to 1 and 0 for math
numeric_df = edited_df.iloc[:, 1:].astype(int)
daily_scores = numeric_df.sum(axis=1)
total_score = daily_scores.sum()
consistency = (total_score / 28) * 100

# --- Metrics Display ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Score", f"{total_score} / 28")
col2.metric("Consistency", f"{consistency:.1f}%")
col3.metric("Daily Average", f"{total_score/7:.2f}")

# --- Charts ---
st.subheader("Progress Chart")
# Create a simple bar chart for scores
chart_data = pd.DataFrame({"Score": daily_scores.values}, index=edited_df["Day"])
st.bar_chart(chart_data)

# --- Reflection ---
st.subheader("Weekly Reflection Summary")
reflection_text = st.text_area(
    "Minimum 300 words:", 
    placeholder="Which Q was strongest? What distracted you?...", 
    height=300
)
word_count = len(reflection_text.split())
st.write(f"Word Count: {word_count} / 300")
