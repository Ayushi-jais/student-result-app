import streamlit as st
import pandas as pd
import os

# ---------- LOGIN SYSTEM ----------
def login():

    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        # Simple credentials (you can change)
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Username or Password")

            # Initialize session
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# If not logged in → show login page
if not st.session_state["logged_in"]:
    login()
    st.stop()

    # ---------- AI FEEDBACK ----------
def generate_feedback(marks_dict, percentage):

    strengths = []
    weaknesses = []

    for subject, mark in marks_dict.items():
        if mark >= 75:
            strengths.append(subject)
        elif mark < 50:
            weaknesses.append(subject)

    feedback = ""

    if percentage >= 90:
        feedback += "🌟 Excellent performance! Keep it up.\n"
    elif percentage >= 75:
        feedback += "👏 Great job! You're doing really well.\n"
    elif percentage >= 50:
        feedback += "🙂 Decent performance, but improvement needed.\n"
    else:
        feedback += "⚠️ You need to focus more on studies.\n"

    if strengths:
        feedback += f"💪 Strong in: {', '.join(strengths)}\n"

    if weaknesses:
        feedback += f"📉 Weak in: {', '.join(weaknesses)}\n"

    if not weaknesses:
        feedback += "🚀 No weak subjects. Amazing!"

    return feedback

st.set_page_config(page_title="Student Dashboard", page_icon="🎓", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
h1, h2, h3 {
    color: #1e3a8a;
}
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
}
.css-1d391kg {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)

# ---------- File ----------
FILE = "data/student_data.csv"
os.makedirs("data", exist_ok=True)

if not os.path.exists(FILE):
    pd.DataFrame(columns=["Name","Age","Maths","Science","English","Computer","Hindi","Total","Percentage","Grade"]).to_csv(FILE, index=False)

# ---------- Sidebar ----------
st.sidebar.title("🎓 Student App")
page = st.sidebar.radio("Navigate", ["🏠 Home", "📊 Dashboard"])

st.title("🎓 Student Performance System")
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

# ---------- HOME ----------
if page == "🏠 Home":

    st.subheader("Enter Details")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("👤 Name")

    with col2:
        age = st.slider("🎂 Age", 5, 25)

    st.subheader("📚 Marks")

    col3, col4, col5 = st.columns(3)

    with col3:
        maths = st.number_input("Maths", 0, 100)
        science = st.number_input("Science", 0, 100)

    with col4:
        english = st.number_input("English", 0, 100)
        computer = st.number_input("Computer", 0, 100)

    with col5:
        hindi = st.number_input("Hindi", 0, 100)

    if st.button("🚀 Generate Result"):

        marks = [maths, science, english, computer, hindi]
        total = sum(marks)
        percentage = total / 5

        if percentage >= 90:
            grade = "A+"
        elif percentage >= 75:
            grade = "A"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        else:
            grade = "F"

        marks_dict = {
            "Maths": maths,
            "Science": science,
            "English": english,
            "Computer": computer,
            "Hindi": hindi
        }

        ai_feedback = generate_feedback(marks_dict, percentage)

        st.subheader("🤖 AI Feedback")
        st.info(ai_feedback)

        # Save
        df_new = pd.DataFrame([[name, age, maths, science, english, computer, hindi, total, percentage, grade]],
                              columns=["Name","Age","Maths","Science","English","Computer","Hindi","Total","Percentage","Grade"])
        df_new.to_csv(FILE, mode="a", header=False, index=False)

        st.success("✅ Result Generated & Saved!")

        # Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Total", total)
        c2.metric("Percentage", f"{percentage:.2f}%")
        c3.metric("Grade", grade)

        # Chart
        df_chart = pd.DataFrame({
            "Subjects": ["Maths","Science","English","Computer","Hindi"],
            "Marks": marks
        }).set_index("Subjects")

        st.bar_chart(df_chart)

        # Feedback
        if percentage >= 90:
            st.balloons()
            st.success("🌟 Outstanding!")
        elif percentage >= 75:
            st.info("👏 Great Work!")
        elif percentage >= 50:
            st.warning("🙂 Keep Improving!")
        else:
            st.error("📚 Need More Practice!")

# ---------- DASHBOARD ----------
elif page == "📊 Dashboard":

    st.subheader("📋 Student Records")

    df = pd.read_csv(FILE)
    st.dataframe(df, use_container_width=True)

    if not df.empty:
        top = df.loc[df["Percentage"].idxmax()]
        st.success(f"🏆 Topper: {top['Name']} ({top['Percentage']:.2f}%)")

        st.subheader("📈 Class Performance")

        st.line_chart(df["Percentage"])

    if st.button("🗑 Clear Data"):
        os.remove(FILE)
        st.warning("Data Cleared! Refresh app.")