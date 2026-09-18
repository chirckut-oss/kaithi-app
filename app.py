import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("📜 Kaithi Page Translator (AI Powered)")
st.write("कैथी लिपि का पेज अपलोड करें, और AI उसका ओरिजिनल फॉर्मेट बरकरार रखते हुए अनुवाद करेगा।")

st.header("⚙️ Settings")
api_key = st.text_input("Enter API Key", type="password")

uploaded_file = st.file_uploader("कैथी की इमेज अपलोड करें (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, use_container_width=True)
    
    if st.button("अनुवाद शुरू करें (Translate)"):
        if api_key == "":
            st.error("⚠️ कृपया सेटिंग्स में अपनी API Key दर्ज करें!")
        else:
            with st.spinner("अनुवाद किया जा रहा है... कृपया प्रतीक्षा करें..."):
                try:
                    # API Key सेट करें
                    genai.configure(api_key=api_key)
                    
                    # सीधा नया मॉडल इस्तेमाल करें (कोई फालतू लॉजिक नहीं)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    img = Image.open(uploaded_file)
                    
                    prompt = "यह कैथी (Kaithi) लिपि में लिखा गया एक दस्तावेज़ है। कृपया इस इमेज को ध्यान से पढ़ें और इसका शुद्ध हिंदी में अनुवाद करें।"
                    
                    # रिज़ल्ट मँगवाना
                    response = model.generate_content([prompt, img])
                    
                    st.success("✅ अनुवाद सफल रहा!")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"एरर आ गया: {e}")
