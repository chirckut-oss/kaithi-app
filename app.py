import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. UI Setup aur Title
st.title("📜 Kaithi Page Translator (AI Powered)")
st.write("कैथी लिपि का पेज अपलोड करें, और AI उसका ओरिजिनल फॉर्मेट और पैराग्राफ स्टाइल बरकरार रखते हुए अनुवाद करेगा।")

# 2. Settings Section
st.header("⚙️ Settings")
ai_choice = st.radio("अनुवाद के लिए AI चुनें:", ("Google Gemini (Free)", "ChatGPT (OpenAI - GPT-4o)"))
api_key = st.text_input("Enter API Key", type="password")

# 3. File Uploader
uploaded_file = st.file_uploader("कैथी की इमेज या पेज यहाँ अपलोड करें (JPG, PNG)", type=["jpg", "jpeg", "png"])

# 4. Displaying the Image and Translation logic
st.header("Original Kaithi Page")

if uploaded_file is not None:
    st.image(uploaded_file, use_container_width=True)
    
    # 5. Translation Button
    if st.button("अनुवाद शुरू करें (Translate)"):
        if api_key == "":
            st.error("⚠️ कृपया सेटिंग्स में अपनी API Key दर्ज करें!")
        else:
            with st.spinner("अनुवाद किया जा रहा है... कृपया प्रतीक्षा करें..."):
                try:
                    # इमेज को तैयार करना
                    img = Image.open(uploaded_file)
                    genai.configure(api_key=api_key)
                    
                    # 💡 SMART MODEL SELECTOR: यह खुद ढूंढेगा कि आपकी API Key पर कौन सा मॉडल चलेगा
                    best_model = "gemini-pro-vision" # Default fallback
                    
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            # अगर नया फ्लैश या प्रो मॉडल मिला, तो उसे चुन लेगा
                            if '1.5-flash' in m.name:
                                best_model = m.name.replace('models/', '')
                                break
                            elif '1.5-pro' in m.name or 'pro-vision' in m.name:
                                best_model = m.name.replace('models/', '')
                    
                    # सही मॉडल लोड करना
                    model = genai.GenerativeModel(best_model)
                    
                    # AI को निर्देश देना
                    prompt = "यह कैथी (Kaithi) लिपि में लिखा गया एक पुराना दस्तावेज़ है। कृपया इस इमेज को ध्यान से पढ़ें और इसका शुद्ध हिंदी में अनुवाद करें। अनुवाद करते समय ओरिजिनल फॉर्मेट बरकरार रखें।"
                    
                    # अनुवाद मँगवाना
                    response = model.generate_content([prompt, img])
                    
                    # फाइनल रिज़ल्ट स्क्रीन पर दिखाना
                    st.success(f"✅ अनुवाद सफल रहा! (Model used: {best_model})")
                    st.subheader("Translated Text:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"अनुवाद के दौरान एरर आ गया। कृपया अपनी API Key चेक करें। डिटेल: {e}")
else:
    st.info("कृपया अनुवाद शुरू करने के लिए कैथी लिपि की इमेज अपलोड करें।")
