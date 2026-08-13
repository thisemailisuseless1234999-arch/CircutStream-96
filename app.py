import streamlit as st

with st.sidebar:
    st.header("Settings")
    name = st.text_input("Enter your name")
    mood = st.selectbox("How are you feeling today?", ["Happy", "Sad", "Excited", "Bored"])
    creativity = st.slider("Rate your creativity", 1, 10, 5)
    if st.button("Save"):
        st.write(f"Saved: Your name is {name}! You are feeling {mood} and your creativity level is {creativity}.")