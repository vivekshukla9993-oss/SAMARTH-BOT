import streamlit as st
import pandas as pd
import google.generativeai as genai
import requests
from streamlit_lottie import st_lottie

# 1. पेज का सेटअप
st.set_page_config(page_title="समर्थ पोर्टल हेल्पडेस्क", page_icon="🎓", layout="wide")

# 2. कस्टम डिज़ाइन (CSS)
st.markdown("""
<style>
    .stApp { background-color: #f8fcfd; }
    .letterhead-hi { color: #b30000; text-align: center; font-family: 'Sanskrit Text', serif; font-size: 32px; font-weight: bold; margin-bottom: 0px;}
    .letterhead-en { color: #000080; text-align: center; font-size: 20px; font-weight: bold; margin-top: 0px;}
    .subtitle { text-align: center; color: #4b4b4b; font-size: 18px; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# 3. मुख्य लेटरहेड हेडिंग
st.markdown("<div class='letterhead-hi'>श्री भगवानदास आदर्श संस्कृत महाविद्यालय</div>", unsafe_allow_html=True)
st.markdown("<div class='letterhead-en'>Shri Bhagwandas Adarsh Sanskrit Mahavidyalaya</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>🎓 समर्थ पोर्टल एवं AI हेल्पडेस्क</div>", unsafe_allow_html=True)

# 4. MARQUEE (चलती हुई सूचना)
st.markdown("""
    <marquee width="100%" direction="left" height="30px" style="color: red; font-size: 18px; font-weight: bold; background-color: #fff3f3; padding-top: 2px;">
    📢 आवश्यक सूचना: विषय चयन, समर्थ पोर्टल आई.डी. और ABC आई.डी. के लिए छात्र अपने विषय प्राध्यापकों से शीघ्र संपर्क करें। || टाइम टेबल 5 नवंबर को घोषित होगा।
    </marquee>
""", unsafe_allow_html=True)

st.divider()

# Lottie Animation लोड करने का फंक्शन
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 5. TABS (अलग-अलग सेक्शन में बाँटना)
# इससे सारा कंटेंट एक ही पेज पर खिचड़ी नहीं बनेगा
tab1, tab2, tab3 = st.tabs(["💬 AI चैट असिस्टेंट", "📢 सूचना एवं ट्यूटोरियल", "🔍 एनरोलमेंट सर्च"])

# --- TAB 1: AI CHATBOT ---
with tab1:
    col1, col2 = st.columns([1, 4])
    with col1:
        # Lottie Animation (नमस्ते करता हुआ रोबोट)
        lottie_robot = load_lottieurl("https://lottie.host/78f2ec67-36e2-43d9-9ec6-8ddaa241f3ee/bI70G7fD35.json")
        if lottie_robot:
            st_lottie(lottie_robot, height=150, key="robot")
    with col2:
        st.subheader("आपका स्मार्ट AI दोस्त")
        st.write("समर्थ पोर्टल या कॉलेज से जुड़ी कोई भी समस्या यहाँ पूछें।")

    # API और बॉट का सेटअप
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    college_rules = "तुम श्री भगवानदास आदर्श संस्कृत महाविद्यालय के हेल्पडेस्क बॉट हो। जवाब हमेशा आसान हिंदी में दो।"
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=college_rules)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = model.start_chat(history=[])

    for message in st.session_state.chat_history.history:
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    user_input = st.chat_input("अपना सवाल यहाँ टाइप करें...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("जानकारी ढूँढ रहा हूँ..."):
                try:
                    response = st.session_state.chat_history.send_message(user_input)
                    st.markdown(response.text)
                except Exception as e:
                    st.warning("⚠️ सर्वर व्यस्त है। कृपया 10 सेकंड बाद दोबारा पूछें।")

# --- TAB 2: NOTICE BOARD ---
with tab2:
    st.subheader("📢 आवश्यक सूचना बोर्ड")
    st.image("https://cdn-icons-png.flaticon.com/512/8074/8074804.png", width=100) # यहाँ आप अपने लेटरपैड की फोटो भी लगा सकते हैं 'notic.jpg' नाम से
    st.write("**विषय चयन हेतु प्राध्यापकों की सूची:**")
    st.markdown("""
    * **व्याकरण:** डॉ. श्री ओम शर्मा जी / डॉ. शिवदेव आर्य
    * **साहित्य:** डॉ. अङ्कुर कुमार आर्य
    * **दर्शन:** डॉ. सचिन द्विवेदी
    * **ज्योतिष:** डॉ. श्रीकृष्णचन्द्र शर्मा
    * **वेदान्त:** डॉ. तरुण डोभाल
    """)
    st.subheader("🌐 महत्वपूर्ण लिंक")
    st.markdown("[👉 समर्थ पोर्टल लॉगिन के लिए यहाँ क्लिक करें](https://samarth.edu.in/)")
    st.subheader("📺 ट्यूटोरियल वीडियो")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # अपना वीडियो लिंक डालें

# --- TAB 3: STUDENT SEARCH ---
with tab3:
    st.subheader("🔍 अपना Enrollment No. जानें")
    student_name = st.text_input("अपना पूरा नाम लिखें:")
    student_mobile = st.text_input("अपना मोबाइल नंबर डालें:")
    
    if st.button("सर्च करें"):
        if student_name and student_mobile:
            try:
                df = pd.read_csv("students.csv")
                df.columns = df.columns.str.strip()
                df['NAME'] = df['NAME'].astype(str).str.strip().str.lower()
                df['MOBILE'] = df['MOBILE'].astype(str).str.split('.').str[0].str.strip()
                
                match = df[(df['NAME'] == student_name.strip().lower()) & 
                           (df['MOBILE'] == student_mobile.strip())]
                
                if not match.empty:
                    st.success("✅ डिटेल्स मिल गईं!")
                    st.write(f"**Enrollment No:** {match.iloc[0]['ENROLMENT']}")
                else:
                    st.error("❌ नाम या मोबाइल नंबर मैच नहीं हुआ।")
            except Exception as e:
                st.warning("⚠️ स्टूडेंट्स का डेटा अभी उपलब्ध नहीं है।")
        else:
            st.warning("कृपया डिटेल्स भरें।")

# Footer
st.markdown("<br><hr><center><b>💻 CHAT BOT DESIGNED BY VIVEK SHUKLA (COMPUTER INSTRUCTOR)</b></center>", unsafe_allow_html=True)
