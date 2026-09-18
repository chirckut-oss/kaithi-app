import streamlit as st
import google.generativeai as genai
from PIL import Image

# पेज टाइटल और डिस्क्रिप्शन
st.title("📜 Kaithi Page Translator (AI Powered)")
st.write("कैथी लिपि का पेज अपलोड करें, और AI उसका ओरिजिनल फॉर्मेट बरकरार रखते हुए अनुवाद करेगा।")

# सेटिंग्स और API Key इनपुट
st.header("⚙️ Settings")
api_key = st.text_input("Enter API Key", type="password")

# इमेज अपलोडर
uploaded_file = st.file_uploader("कैथी की इमेज अपलोड करें (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # इमेज को लोड करना
    image = Image.open(uploaded_file)
    
    # पुरानी एरर (use_column_width) को फिक्स कर दिया गया है
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    # ट्रांसलेट बटन
    if st.button("Translate to Hindi/English"):
        if not api_key:
            st.error("⚠️ कृपया ऊपर Settings में अपनी Google API Key डालें।")
        else:
            try:
                # Google Gemini API से कनेक्शन (Google Server)
                genai.configure(api_key=api_key)
                
                # इमेज और टेक्स्ट दोनों को प्रोसेस करने के लिए gemini-1.5-flash सबसे बेहतर है
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                with st.spinner("Google Server से कनेक्ट हो रहा है और अनुवाद किया जा रहा है..."):
                    # AI को निर्देश (Prompt)
                    prompt = "This image contains handwritten text in Kaithi script. Please translate the Kaithi text into Hindi, maintaining the original structure and format as much as possible."
                    
                    # API कॉल
                    response = model.generate_content([prompt, image])
                    
                    # रिजल्ट दिखाना
                    st.success("अनुवाद सफल!")
                    st.subheader("Translation Result:")
                    st.write(response.text)
                    
            except Exception as e:
                # अगर Google server या API key में कोई दिक्कत आती है, तो यह एरर दिखाएगा
                st.error(f"❌ Google Server Connection Error: {e}")
                st.info("कृपया चेक करें कि आपकी API Key सही है और आपके पास इंटरनेट कनेक्शन है।")
