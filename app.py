import streamlit as st
import pandas as pd
import google.generativeai as genai

# पेज का सेटअप
st.set_page_config(page_title="समर्थ पोर्टल हेल्पडेस्क", page_icon="🎓", layout="wide")

# कस्टम डिज़ाइन (CSS)
st.markdown("""
<style>
    .stApp { background-color: #f8fcfd; }
    .letterhead-hi { color: #b30000; text-align: center; font-family: 'Sanskrit Text', serif; font-size: 32px; font-weight: bold; margin-bottom: 0px;}
    .letterhead-en { color: #000080; text-align: center; font-size: 20px; font-weight: bold; margin-top: 0px;}
    .subtitle { text-align: center; color: #4b4b4b; font-size: 18px; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# मुख्य लेटरहेड हेडिंग
st.markdown("<div class='letterhead-hi'>श्री भगवानदास आदर्श संस्कृत महाविद्यालय</div>", unsafe_allow_html=True)
st.markdown("<div class='letterhead-en'>Shri Bhagwandas Adarsh Sanskrit Mahavidyalaya</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>🎓 समर्थ पोर्टल एवं AI हेल्पडेस्क</div>", unsafe_allow_html=True)
st.divider()

# बायीं तरफ का साइडबार
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8074/8074804.png", width=150)
    
    # आवश्यक सूचना (नई अपडेटेड)
    st.error("📢 आवश्यक सूचना (09-10-2026)")
    st.write("**विषय चयन, समर्थ पोर्टल आई.डी. और ABC आई.डी.** के लिए छात्र अपने विषय अनुसार निम्नलिखित प्राध्यापकों से संपर्क करें:")
    
    with st.expander("👨‍🏫 प्राध्यापकों की सूची देखें"):
        st.markdown("""
        * **व्याकरण:** डॉ. श्री ओम शर्मा जी / डॉ. शिवदेव आर्य
        * **साहित्य:** डॉ. अङ्कुर कुमार आर्य
        * **दर्शन:** डॉ. सचिन द्विवेदी
        * **ज्योतिष:** डॉ. श्रीकृष्णचन्द्र शर्मा
        * **वेदान्त:** डॉ. तरुण डोभाल
        """)
    
    st.subheader("🌐 महत्वपूर्ण लिंक")
    st.markdown("[👉 समर्थ पोर्टल लॉगिन](https://samarth.edu.in/)")
    
    st.subheader("📺 ट्यूटोरियल वीडियो")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # अपना लिंक डालें
    
    # Enrollment Search Box
    st.subheader("🔍 अपना Enrollment No. जानें")
    with st.expander("यहाँ क्लिक करें"):
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

# API और बॉट का सेटअप
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

# बॉट को नए नोटिस की जानकारी देना
college_rules = """
तुम श्री भगवानदास आदर्श संस्कृत महाविद्यालय के हेल्पडेस्क बॉट हो।
नियम:
1. अगर छात्र विषय चयन, समर्थ पोर्टल ID या ABC ID के बारे में पूछे, तो उन्हें बताओ कि वे अपने विषय के अनुसार इन प्राध्यापकों से मिलें: व्याकरण के लिए डॉ. ओम शर्मा या डॉ. शिवदेव आर्य, साहित्य के लिए डॉ. अङ्कुर कुमार आर्य, दर्शन के लिए डॉ. सचिन द्विवेदी, ज्योतिष के लिए डॉ. श्रीकृष्णचन्द्र शर्मा, और वेदान्त के लिए डॉ. तरुण डोभाल।
2. जवाब हमेशा पॉइंट्स में और आसान हिंदी में दो।
"""

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=college_rules)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = model.start_chat(history=[])

# चैट इंटरफ़ेस
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

# सबसे नीचे आपका नाम (Footer)
st.markdown("<br><hr><center><b>💻 CHAT BOT DESIGNED BY VIVEK SHUKLA (COMPUTER INSTRUCTOR)</b></center>", unsafe_allow_html=True)
