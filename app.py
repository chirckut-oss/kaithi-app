import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import os

# ----------------- DATABASE SETUP -----------------
# यह फाइल आपके सर्वर पर कैथी डिक्शनरी और सुधारे गए अनुवादों को याद रखेगी
DB_FILE = "kaithi_knowledge.json"

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({"dictionary": {}, "corrections": []}, f)

def load_db():
    init_db()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db_data = load_db()

# ----------------- APP UI CONFIG -----------------
st.set_page_config(page_title="Kaithi AI Pro", page_icon="📜", layout="wide")
st.title("📜 Kaithi AI Pro (Self-Learning Translator)")

st.sidebar.header("⚙️ Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# 4 मुख्य फीचर्स के लिए टैब्स
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 अनुवाद (Translate)", 
    "📖 मेरी डिक्शनरी (Dictionary)", 
    "📊 ऐतिहासिक विश्लेषण (Analysis)", 
    "🧠 AI ट्यूटर (Learn)"
])

# ----------------- TAB 1: TRANSLATE & TEACH AI -----------------
with tab1:
    st.header("कैथी दस्तावेज़ का अनुवाद करें")
    uploaded_file = st.file_uploader("कैथी की इमेज अपलोड करें (JPG, PNG)", type=["jpg", "jpeg", "png"], key="trans_img")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Translate to Hindi/English"):
        if not api_key:
            st.error("कृपया बाईं ओर (Sidebar) अपनी API Key दर्ज करें।")
        elif uploaded_file is None:
            st.warning("इमेज अपलोड करें।")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                # AI को पुरानी डिक्शनरी और गलतियों का संदर्भ देना (Machine Learning Prompt)
                dict_context = json.dumps(db_data["dictionary"], ensure_ascii=False)
                
                learning_prompt = f"""
                तुम कैथी लिपि के विशेषज्ञ हो। मैं तुम्हें अपना 'Reference Data' दे रहा हूँ:
                कस्टम डिक्शनरी: {dict_context}
                
                इस कस्टम डिक्शनरी के शब्दों का इस्तेमाल करते हुए इस कैथी इमेज का सटीक हिंदी और अंग्रेजी अनुवाद करो। 
                ओरिजिनल फॉर्मेट बनाए रखो।
                """
                
                with st.spinner("AI अनुवाद कर रहा है..."):
                    response = model.generate_content([learning_prompt, image])
                    st.session_state['last_translation'] = response.text
                    st.success("अनुवाद पूरा हुआ!")
                    
            except Exception as e:
                st.error(f"Error: {e}")

    # Feedback Loop: AI को अपनी गलतियां सुधारना सिखाएं
    if 'last_translation' in st.session_state:
        st.markdown("### 📄 Translation Result:")
        st.write(st.session_state['last_translation'])
        
        st.divider()
        st.subheader("🛠️ AI की गलती सुधारें (Teach AI)")
        corrected_text = st.text_area("अगर AI ने कोई गलती की है, तो यहाँ सही अनुवाद लिखकर सेव करें:", value=st.session_state['last_translation'], height=150)
        
        if st.button("Save Correction to AI Memory"):
            db_data["corrections"].append(corrected_text)
            save_db(db_data)
            st.success("✅ आपका सुधारा हुआ अनुवाद AI की मेमोरी में सेव हो गया है! अगली बार यह इस गलती को नहीं दोहराएगा।")

# ----------------- TAB 2: CUSTOM DICTIONARY -----------------
with tab2:
    st.header("📖 कैथी शब्दकोश (AI Knowledge Base)")
    st.write("यहाँ नए कैथी शब्द जोड़ें। AI अनुवाद करते समय इन शब्दों का संदर्भ लेगा।")
    
    col1, col2 = st.columns(2)
    with col1:
        new_kaithi_word = st.text_input("कैथी/स्थानीय शब्द (जैसे: चौहद्दी, लगान)")
    with col2:
        new_word_meaning = st.text_input("हिंदी/अंग्रेजी अर्थ")
        
    if st.button("शब्द को डिक्शनरी में जोड़ें"):
        if new_kaithi_word and new_word_meaning:
            db_data["dictionary"][new_kaithi_word] = new_word_meaning
            save_db(db_data)
            st.success(f"'{new_kaithi_word}' डिक्शनरी में जुड़ गया!")
        else:
            st.warning("कृपया शब्द और अर्थ दोनों भरें।")
            
    st.divider()
    st.subheader("📚 आपकी सेव की गई डिक्शनरी:")
    st.json(db_data["dictionary"])

# ----------------- TAB 3: DOCUMENT ANALYSIS -----------------
with tab3:
    st.header("📊 लंबी किताब या पुराने कागज़ात का विश्लेषण")
    st.write("यहाँ कोई पुराना दस्तावेज़ अपलोड करें और उसकी ऐतिहासिक अहमियत, विषय और कठिन शब्दों की रिपोर्ट पाएं।")
    
    doc_file = st.file_uploader("दस्तावेज़ की इमेज अपलोड करें", type=["jpg", "jpeg", "png"], key="doc_img")
    
    if st.button("Analyze Document"):
        if not api_key:
            st.error("API Key दर्ज करें।")
        elif doc_file is None:
            st.warning("इमेज अपलोड करें।")
        else:
            try:
                doc_image = Image.open(doc_file)
                st.image(doc_image, use_container_width=True)
                
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                analysis_prompt = """
                तुम एक ऐतिहासिक दस्तावेज़ रिसर्चर हो। इस कैथी दस्तावेज़ का विश्लेषण करो और मुझे 4 पॉइंट में रिपोर्ट दो:
                1. मुख्य विषय (यह दस्तावेज़ किस बारे में है?)
                2. ऐतिहासिक संदर्भ (तारीख, स्थान, व्यक्तियों के नाम)
                3. इस्तेमाल किए गए 5 सबसे महत्वपूर्ण शब्द और उनके अर्थ।
                4. लिखावट की शैली।
                """
                
                with st.spinner("रिसर्च और विश्लेषण किया जा रहा है..."):
                    doc_response = model.generate_content([analysis_prompt, doc_image])
                    st.markdown("### 📋 दस्तावेज़ की रिपोर्ट:")
                    st.write(doc_response.text)
            except Exception as e:
                st.error(f"Error: {e}")

# ----------------- TAB 4: AI TUTOR (LEARN) -----------------
with tab4:
    st.header("🧠 कैथी ट्यूटर से सीखें")
    st.write("कैथी लिपि के बारे में कोई भी सवाल पूछें।")
    
    user_question = st.text_input("अपना सवाल लिखें (जैसे: कैथी में 'क' कैसे लिखते हैं?)")
    
    if st.button("Ask Tutor"):
        if not api_key:
            st.error("API Key दर्ज करें।")
        elif not user_question:
            st.warning("कृपया सवाल पूछें।")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                tutor_prompt = f"You are a teacher of the historical Kaithi script. Answer this student's question clearly in Hindi: {user_question}"
                
                with st.spinner("ट्यूटर जवाब तैयार कर रहा है..."):
                    tutor_resp = model.generate_content(tutor_prompt)
                    st.info("💡 **Tutor's Answer:**")
                    st.write(tutor_resp.text)
            except Exception as e:
                st.error(f"Error: {e}")
