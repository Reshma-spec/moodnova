import streamlit as st
import pandas as pd
import datetime
from streamlit_option_menu import option_menu

# ----------------- Page Config -----------------
st.set_page_config(page_title="MoodNova", layout="wide", page_icon="🧠")

# ----------------- Initialize Session -----------------
if "users" not in st.session_state:
    st.session_state.users = {}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ----------------- Functions -----------------
def create_account():
    st.subheader("Create Account")
    username = st.text_input("Username", key="c_user")
    password = st.text_input("Password", type="password", key="c_pass")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male","Female","Other"])
    location = st.selectbox("Location", ["Urban","Rural"])
    marital_status = st.selectbox("Marital Status", ["Married","Unmarried","Divorcee"])
    kids = 0
    if marital_status=="Married":
        kids = st.selectbox("Number of Kids", [0,1,2,"More"])
    work_status = st.selectbox("Working?", ["No","Yes"])
    work_type = None
    if work_status=="Yes":
        work_type = st.selectbox("Work Type", ["Business person","Employee","Govt Employee","Other"])
    weight = st.number_input("Weight (kg)")

    if st.button("Sign Up"):
        if age < 15:
            st.error("You must be at least 15 years old!")
        else:
            st.session_state.users[username] = {
                "password": password,
                "age": age,
                "gender": gender,
                "location": location,
                "marital_status": marital_status,
                "kids": kids,
                "work_status": work_status,
                "work_type": work_type,
                "weight": weight,
                "history": []
            }
            st.success("Account created! Please login now.")

def login():
    st.subheader("Login")
    username = st.text_input("Username", key="l_user")
    password = st.text_input("Password", type="password", key="l_pass")
    if st.button("Login"):
        user = st.session_state.users.get(username)
        if user and user["password"]==password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Invalid credentials")

# ----------------- Authentication -----------------
with st.sidebar:
    page = option_menu(
        menu_title="Login / Sign Up / Admin",
        options=["Login","Create Account","Admin"],
        icons=["box-arrow-in-right","person-plus","gear"],
        menu_icon="key",
        default_index=0
    )

# ----------------- Admin -----------------
if page=="Admin":
    st.subheader("Admin Dashboard")
    st.write(st.session_state.users)

# ----------------- User Dashboard -----------------
elif st.session_state.logged_in:
    user = st.session_state.users[st.session_state.current_user]

    nav = option_menu(
        menu_title="Navigation",
        options=["Home","Weekly Graph","MoodCard","Calendar Heatmap","History","Assessment"],
        icons=["house","graph-up","card-text","calendar","clock-history","file-text"],
        orientation="horizontal"
    )

    # ----------------- Home -----------------
    if nav=="Home":
        st.title("🧠 Welcome to MoodNova")
        st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e", width=700)
        st.info("“Happiness is not something ready made. It comes from your own actions.” – Dalai Lama")
        st.warning("⚠️ Disclaimer: MoodNova is AI-based and not a substitute for professional medical advice.")

    # ----------------- Weekly Graph -----------------
    elif nav=="Weekly Graph":
        st.subheader("Weekly Mood Graph")
        df = pd.DataFrame(user["history"])
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            weekly = df.groupby(df['date'].dt.day_name())['score'].mean()
            weekly.plot(kind="bar")
            st.pyplot(plt)
        else:
            st.write("No data yet. Take an assessment!")

    # ----------------- MoodCard -----------------
    elif nav=="MoodCard":
        st.subheader("Your Mood Card")
        if user["history"]:
            last = user["history"][-1]
            st.metric(label="Mood Score", value=last["score"])
            st.write("Recommendation:", last["recommendation"])
        else:
            st.write("Take an assessment to see your mood card!")

    # ----------------- Calendar Heatmap -----------------
    elif nav=="Calendar Heatmap":
        st.subheader("Mood Calendar Heatmap")
        st.write("Coming soon!")

    # ----------------- History -----------------
    elif nav=="History":
        st.subheader("Your Previous Data")
        if user["history"]:
            st.dataframe(user["history"])
        else:
            st.write("No history yet.")

    # ----------------- Assessment -----------------
    elif nav=="Assessment":
        st.subheader("📝 Mood & Stress Assessment")
        questions = [
            "How are you feeling right now?",
            "How well did you sleep last night?",
            "How easily do small problems frustrate you?",
            "How is your concentration level today?",
            "How often do you feel nervous or anxious?",
            "How do you react to unexpected situations?",
            "How motivated do you feel to do your daily tasks?",
            "How do you feel physically?",
            "How often do you overthink things?",
            "How connected do you feel with others today?"
        ]
        options = ["A","B","C","D","E"]
        answers = []
        for q in questions:
            ans = st.selectbox(q, options, key=q)
            answers.append(ans)

        if st.button("Submit Assessment"):
            mapping = {"A":1,"B":2,"C":3,"D":4,"E":5}
            score = sum([mapping[a] for a in answers])
            rec = []
            if score<=18:
                rec.append("Low Stress 😊 Try listening to music 🎵 or cooking 🍳!")
            elif score<=30:
                rec.append("Mild Stress 😐 Walk 🚶 or light exercise 🏃‍♀️!")
            elif score<=40:
                rec.append("Moderate Stress 😟 Yoga 🧘‍♀️ or workout 💪 recommended!")
            else:
                rec.append("High Stress ⚠️ Take rest 🛌 and mindfulness 🧘!")

            st.success(f"Your Mood Score: {score}")
            st.write("Recommendation:", rec[0])

            # Store history
            user["history"].append({
                "date": datetime.date.today(),
                "score": score,
                "recommendation": rec[0]
            })
            st.session_state.users[st.session_state.current_user] = user

# ----------------- Login / Signup -----------------
else:
    if page=="Create Account":
        create_account()
    else:
        login()