import streamlit as st
import google.generativeai as genai
from openai import OpenAI
from PIL import Image
import base64

# पेज की सेटिंग
st.set_page_config(page_title="Kaithi Translator", layout="wide")
st.title("📜 Kaithi Page Translator (AI Powered)")
st.write("कैथी लिपि का पेज अपलोड करें, और AI उसका ओरिजिनल फॉर्मेट और पैराग्राफ स्टाइल बरकरार रखते हुए अनुवाद करेगा।")

# साइडबार में सेटिंग्स और API Keys
with st.sidebar:
    st.header("⚙️ Settings")
    
    # AI चुनने का विकल्प
    ai_choice = st.radio("अनुवाद के लिए AI चुनें:", ("Google Gemini (Free)", "ChatGPT (OpenAI - GPT-4o)"))
    
    st.markdown("---")
    
    # API Key इनपुट
    if ai_choice == "Google Gemini (Free)":
        gemini_api_key = st.text_input("Enter Google Gemini API Key", type="password")
        st.markdown("[Get Free Gemini API Key](https://aistudio.google.com/app/apikey)")
    else:
        openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
        st.markdown("[Get OpenAI API Key](https://platform.openai.com/api-keys)")

# फाइल अपलोड करने का ऑप्शन
uploaded_file = st.file_uploader("कैथी की इमेज या पेज यहाँ अपलोड करें (JPG, PNG)", type=["jpg", "jpeg", "png"])

# प्रॉम्प्ट (AI के लिए निर्देश)
prompt = """
You are an expert in reading historical Indian scripts, specifically Kaithi. 
Please carefully read the text in this uploaded image. 
Translate and transliterate the text into modern Hindi. 
CRITICAL: Maintain the exact same formatting, paragraph structure, lists, and line breaks as seen in the original image. Do not summarize. Just provide the translated text in the original layout.
"""

if uploaded_file:
    # इमेज को स्क्रीन पर दिखाना
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Kaithi Page")
        st.image(image, use_column_width=True)

    with col2:
        st.subheader("Translated Text (Hindi)")
        
        # बटन दबाने पर अनुवाद शुरू
        if st.button("Translate Text", type="primary"):
            
            # ---------------- GEMINI LOGIC ----------------
            if ai_choice == "Google Gemini (Free)":
                if not gemini_api_key:
                    st.warning("⚠️ कृपया अनुवाद शुरू करने के लिए साइडबार में Gemini API Key डालें।")
                else:
                    try:
                        with st.spinner("Gemini AI पेज को पढ़ रहा है..."):
                            genai.configure(api_key=gemini_api_key)
                            model = genai.GenerativeModel('gemini-1.5-flash') 
                            response = model.generate_content([prompt, image])
                            
                        st.success("अनुवाद पूरा हुआ!")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Gemini Error: {e}")
                        
            # ---------------- OPENAI LOGIC ----------------
            elif ai_choice == "ChatGPT (OpenAI - GPT-4o)":
                if not openai_api_key:
                    st.warning("⚠️ कृपया अनुवाद शुरू करने के लिए साइडबार में OpenAI API Key डालें।")
                else:
                    try:
                        with st.spinner("ChatGPT पेज को पढ़ रहा है..."):
                            # OpenAI के लिए इमेज को Base64 में बदलना पड़ता है
                            base64_image = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                            
                            client = OpenAI(api_key=openai_api_key)
                            response = client.chat.completions.create(
                                model="gpt-4o",
                                messages=[
                                    {
                                        "role": "user",
                                        "content": [
                                            {"type": "text", "text": prompt},
                                            {
                                                "type": "image_url",
                                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                            }
                                        ]
                                    }
                                ],
                                max_tokens=1500
                            )
                            
                        st.success("अनुवाद पूरा हुआ!")
                        st.write(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"OpenAI Error: {e}")
