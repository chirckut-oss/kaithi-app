import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import os
import PyPDF2 # PDF parsing ke liye naya library

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

# Model Setup
if api_key:
    genai.configure(api_key=api_key)
    # Aap 'gemini-1.5-pro' ya 'gemini-1.5-flash' ka use kar sakte hain
    model = genai.GenerativeModel('gemini-1.5-pro') 

# अब ऐप में 5 मुख्य टैब्स होंगे
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 अनुवाद (Translate)", 
    "⚖️ तुलना (Compare Samples)", 
    "📖 मेरी डिक्शनरी (Dictionary)", 
    "📊 ऐतिहासिक विश्लेषण (Analysis)", 
    "🧠 AI ट्यूटर (Learn)"
])

with tab1:
    st.header("📝 अनुवाद (Translate)")
    st.write("यहाँ आपका अनुवाद का कोड रहेगा।")
    # TODO: Add your existing translate code here

with tab2:
    st.header("⚖️ तुलना (Compare Samples)")
    st.write("यहाँ आपका तुलना का कोड रहेगा।")
    # TODO: Add your existing comparison code here

with tab3:
    st.header("📖 मेरी डिक्शनरी (Dictionary)")
    st.write("यहाँ डिक्शनरी का कोड रहेगा।")
    # TODO: Add your existing dictionary code here

with tab4:
    st.header("📊 लंबी किताब या पुराने कागज़ात का विश्लेषण")
    st.write("यहाँ कोई पुराना दस्तावेज़ अपलोड करें और उसकी ऐतिहासिक अहमियत, विषय और कठिन शब्दों की रिपोर्ट पाएं।")
    
    # PDF option add kar diya gaya hai type attribute me
    uploaded_file = st.file_uploader("दस्तावेज़ की इमेज या पीडीएफ अपलोड करें", type=["jpg", "png", "pdf"])
    
    if st.button("Analyze Document"):
        if not api_key:
            st.error("कृपया एनालिसिस के लिए साइडबार में Gemini API Key डालें।")
        elif uploaded_file is not None:
            with st.spinner("दस्तावेज़ का विश्लेषण हो रहा है... कृपया प्रतीक्षा करें।"):
                
                # Agar file PDF hai
                if uploaded_file.type == "application/pdf":
                    try:
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        num_pages = len(pdf_reader.pages)
                        st.success(f"PDF सफलतापूर्वक लोड हो गई। कुल पेज: {num_pages}")
                        
                        extracted_text = ""
                        # Text extract karna (yahan starting ke 10 page limit kiya hai taaki model overload na ho)
                        for page_num in range(min(num_pages, 10)): 
                            page = pdf_reader.pages[page_num]
                            if page.extract_text():
                                extracted_text += page.extract_text() + "\n"
                        
                        # Gemini Model ko text prompt bhejna
                        prompt = (
                            "आप एक विशेषज्ञ हैं जो कैथी और पुरानी हिंदी/भोजपुरी दस्तावेजों को समझते हैं। "
                            "नीचे दिए गए किताब/दस्तावेज़ के टेक्स्ट का ऐतिहासिक विश्लेषण करें, इसका मुख्य विषय बताएं "
                            "और कठिन शब्दों की सूची उनके अर्थ के साथ बनाएं:\n\n" + extracted_text
                        )
                        
                        response = model.generate_content(prompt)
                        st.subheader("📊 विश्लेषण रिपोर्ट:")
                        st.write(response.text)
                        
                    except Exception as e:
                        st.error(f"PDF पढ़ने में समस्या आई: {e}")
                        
                # Agar file Image (JPG/PNG) hai
                else:
                    try:
                        image = Image.open(uploaded_file)
                        st.image(image, caption="अपलोड की गई इमेज", use_container_width=True)
                        
                        # Gemini Model ko image aur text prompt dono bhejna
                        prompt = (
                            "इस इमेज में दिए गए कैथी/हिंदी दस्तावेज़ का ऐतिहासिक विश्लेषण करें, "
                            "इसका मुख्य विषय बताएं और कठिन शब्दों की सूची अर्थ के साथ बनाएं।"
                        )
                        
                        response = model.generate_content([prompt, image])
                        st.subheader("📊 विश्लेषण रिपोर्ट:")
                        st.write(response.text)
                        
                    except Exception as e:
                        st.error(f"इमेज पढ़ने में समस्या आई: {e}")
        else:
            st.warning("कृपया विश्लेषण करने के लिए पहले एक फाइल (JPG, PNG या PDF) अपलोड करें।")

with tab5:
    st.header("🧠 AI ट्यूटर (Learn)")
    st.write("यहाँ AI ट्यूटर का कोड रहेगा।")
    # TODO: Add your existing tutor code here
