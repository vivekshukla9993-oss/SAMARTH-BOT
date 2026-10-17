import streamlit as st
import google.generativeai as genai

# 1. पेज का नया डिज़ाइन (छात्रों के लिए)
st.set_page_config(page_title="समर्थ पोर्टल हेल्पर", page_icon="🎓", layout="centered")

API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

# 2. बॉट का दिमाग और नियम (System Instructions) - यहाँ अपनी असली जानकारी भरें!
college_rules = """
तुम एक बहुत ही मददगार और नम्र कॉलेज असिस्टेंट हो। तुम्हारा नाम 'समर्थ हेल्पर बॉट' है। 
तुम्हारा काम छात्रों की 'Samarth Portal' से जुड़ी समस्याओं (Fees, Exam Form, Course Selection) को हल करना है।

तुम्हारे लिए कुछ नियम और जानकारी:
1. Fees (फीस): अगर छात्र CSU की फीस के बारे में पूछे, तो उन्हें बताओ कि समर्थ पोर्टल पर लॉगिन करके 'Fee' सेक्शन में जाएं। (यहाँ अपनी फीस की लिंक या असली प्रोसेस लिखें)
2. Exam Form (परीक्षा फॉर्म): एग्जाम फॉर्म भरने के लिए 'Examination' टैब पर क्लिक करना होता है। (यहाँ फॉर्म की तारीख या ज़रूरी डॉक्यूमेंट्स लिखें)
3. Course Selection (विषय चुनना): कोर्स सेलेक्ट करने के लिए 'Academics' सेक्शन में जाएं।
4. अगर कोई छात्र ऐसा सवाल पूछे जो पोर्टल या पढ़ाई से जुड़ा नहीं है (जैसे- आज का मौसम, चुटकुले, या राजनीति), तो विनम्रता से मना कर दो और कहो: "मैं केवल समर्थ पोर्टल और कॉलेज से जुड़ी जानकारी देने के लिए बना हूँ।"
5. जवाब हमेशा आसान भाषा में (हिंदी या हिंगलिश) पॉइंट्स में दो।
"""

# 3. जेमिनी मॉडल को नियम सिखाना
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=college_rules)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = model.start_chat(history=[])

# 4. वेबसाइट का हेडर
st.title("🎓 समर्थ पोर्टल हेल्पर")
st.caption("फीस, एग्जाम फॉर्म या कोर्स सिलेक्शन से जुड़ा अपना सवाल पूछें 👇")
st.divider()

# 5. पुरानी चैट दिखाना
for message in st.session_state.chat_history.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 6. नया सवाल पूछना
user_input = st.chat_input("अपना सवाल यहाँ टाइप करें (जैसे: एग्जाम फॉर्म कैसे भरें?)...")

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