import streamlit as st
import google.generativeai as genai
import pandas as pd
# 1. पेज का सेटअप और थीम
st.set_page_config(page_title="कॉलेज हेल्पडेस्क", page_icon="🎓", layout="wide")

# 2. कस्टम डिज़ाइन और कलर (CSS) - आप यहाँ कलर बदल सकते हैं
st.markdown("""
<style>
    /* बैकग्राउंड का रंग (हल्का नीला) */
    .stApp {
        background-color: #1cc94a; 
    }
    /* हेडिंग का रंग (गहरा नीला) */
    h1, h2, h3 {
        color: #000080; 
    }
</style>
""", unsafe_allow_html=True)

# 3. बायीं तरफ का साइडबार (Logo, Links, Notices, Video)
with st.sidebar:
    # कॉलेज का लोगो (यहाँ अपने लोगो का वेब लिंक डालें)
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTajyaMtBCOPtpQt4MXPMbhAfstcgeh6F5ALRF_YKRF_w&s=10", width=150)
    
    st.title("📌 ज़रूरी जानकारी")
    
    # समर्थ पोर्टल का लिंक
    st.subheader("🌐 पोर्टल लिंक")
    st.markdown("[👉 यहाँ क्लिक करके समर्थ पोर्टल खोलें](https://sanskrit.samarth.edu.in/index.php/abc/app/index)")
    
    # नोटिस बोर्ड
    st.subheader("📢 नोटिस बोर्ड")
    st.info("""
    **एग्जाम फॉर्म:** 15 अक्टू. - 30 अक्टू.\n
    **टाइम टेबल:** 5 नवंबर को आएगा\n
    **एडमिट कार्ड:** 10 नवंबर से डाउनलोड करें
    """)
    
    # वीडियो ट्यूटोरियल
    st.subheader("📺 ट्यूटोरियल वीडियो")
    st.write("फीस कैसे भरें? नीचे वीडियो देखें:")
    # यहाँ अपने YouTube या स्क्रीन रिकॉर्डिंग का लिंक डालें
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
    # for enrollement number
    st.subheader("🔍 अपना Enrollment/Roll No. जानें")
    with st.expander("यहाँ क्लिक करें"):
        student_name = st.text_input("अपना पूरा नाम लिखें:")
        student_mobile = st.text_input("अपना मोबाइल नंबर डालें:")
        
        if st.button("सर्च करें"):
            if student_name and student_mobile:
                try:
                    # CSV file ko padhna
                   df = pd.read_csv("students.csv")
                    
                    # Headings ke extra space hatana
                    df.columns = df.columns.str.strip()
                    
                    # Aapki list ki headings (NAME, MOBILE) ke anusar match karna
                    df['NAME'] = df['NAME'].astype(str).str.strip().str.lower()
                    df['MOBILE'] = df['MOBILE'].astype(str).str.strip()
                    
                    match = df[(df['NAME'] == student_name.strip().lower()) & 
                               (df['MOBILE'] == student_mobile.strip())]
                    
                    if not match.empty:
                        st.success("✅ डिटेल्स मिल गईं!")
                        # Aapki list mein ENROLMENT likha hai, wahi print karenge
                        st.write(f"**Enrollment No:** {match.iloc[0]['ENROLMENT']}")
                    else:
                        st.error("❌ नाम या मोबाइल नंबर मैच नहीं हुआ। कृपया सही डिटेल्स डालें।")  
                except FileNotFoundError:
                    st.warning("⚠️ स्टूडेंट्स का डेटा अभी अपलोड नहीं हुआ है।")
            else:
                st.warning("कृपया अपना नाम और मोबाइल नंबर दोनों डालें।")

# 4. API Key और मॉडल सेटअप
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

# 5. बॉट का दिमाग (System Instructions)
college_rules = """
श्री भगवानदास आदर्श संस्कृत महाविद्यालय -chatbot
यह एक बहुत ही मददगार कॉलेज असिस्टेंट है, इसका काम छात्रों की 'Samarth Portal' से जुड़ी समस्याओं को हल करना है।
नियम:
1. अगर कोई फीस, एग्जाम फॉर्म या कोर्स सिलेक्शन का पूछे, तो यह स्टेप्स बताता है|
2. छात्रों को यह भी बताता है कि "ज़रूरी लिंक्स, आखिरी तारीखें और मदद के लिए वीडियो बायीं तरफ (Sidebar) में दिए गए हैं, आप उन्हें देख सकते हैं।"
3.
"""

model = genai.GenerativeModel('gemini-3.8-flash', system_instruction=college_rules)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = model.start_chat(history=[])

# 6. मुख्य चैट स्क्रीन
st.title("🎓 Shri Bhagwandas Adarsh Sanskrit Mahavidyalaya - समर्थ पोर्टल हेल्पर")
st.caption("पोर्टल से जुड़ी कोई भी समस्या यहाँ पूछें 👇")
st.divider()

# पुरानी चैट दिखाना
for message in st.session_state.chat_history.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# नया सवाल पूछना
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
                st.error(f"कुछ गड़बड़ हुई: {e}")
