import streamlit as st
import google.generativeai as genai

# 1. पेज का नया डिज़ाइन
st.set_page_config(page_title="मेरा स्मार्ट AI बॉट", page_icon="🤖", layout="centered")

# 2. API Key अब सुरक्षित तरीके से इंटरनेट सर्वर से ली जाएगी (यहाँ असली Key नहीं डालनी है)
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

# 3. जेमिनी मॉडल चुनें
model = genai.GenerativeModel('gemini-3.8-flash')

# 4. बॉट की याददाश्त (Memory) बनाना
if "chat_history" not in st.session_state:
    st.session_state.chat_history = model.start_chat(history=[])

# 5. वेबसाइट का हेडर
st.title("🤖 मेरा स्मार्ट AI दोस्त")
st.caption("मुझसे चैट करें 👇")
st.divider()

# 6. पुरानी चैट दिखाना
for message in st.session_state.chat_history.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 7. नया सवाल पूछना
user_input = st.chat_input("यहाँ अपना मैसेज टाइप करें...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("सोच रहा हूँ..."):
            try:
                response = st.session_state.chat_history.send_message(user_input)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"कुछ गड़बड़ हुई: {e}")