import streamlit as st
import google.generativeai as genai
from PIL import Image

# पेज की सेटिंग
st.set_page_config(page_title="Kaithi Page Translator", page_icon="📜")

# टाइटल और जानकारी
st.title("📜 Kaithi Page Translator (AI Powered)")
st.write("कैथी लिपि का पेज अपलोड करें, और AI उसका ओरिजिनल फॉर्मेट बरकरार रखते हुए अनुवाद करेगा।")

st.header("⚙️ Settings")
# API Key इनपुट
api_key = st.text_input("Enter API Key", type="password")

# इमेज अपलोडर
uploaded_file = st.file_uploader("कैथी की इमेज अपलोड करें (JPG, PNG)", type=["jpg", "jpeg", "png"])

# इमेज दिखाना
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# अनुवाद बटन
if st.button("Translate to Hindi/English"):
    if not api_key:
        st.warning("कृपया पहले अपनी API Key दर्ज करें।")
    elif uploaded_file is None:
        st.warning("कृपया अनुवाद के लिए कैथी लिपि की इमेज अपलोड करें।")
    else:
        try:
            # API Key कॉन्फ़िगरेशन
            genai.configure(api_key=api_key)
            
            # अपडेटेड मॉडल (gemini-2.5-flash) का उपयोग
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            with st.spinner("अनुवाद किया जा रहा है, कृपया प्रतीक्षा करें..."):
                # AI के लिए प्रॉम्प्ट
                prompt = """
                This is an image containing text written in Kaithi script. 
                Please transcribe and translate this text into both Hindi and English. 
                Try to maintain the original format and layout as much as possible.
                """
                
                # API कॉल
                response = model.generate_content([prompt, image])
                
                st.success("अनुवाद पूरा हुआ!")
                
                # परिणाम दिखाना
                st.markdown("### Translation Result:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Google Server Connection Error: {e}")
            st.info("कृपया चेक करें कि आपकी API Key सही है और आपके पास इंटरनेट कनेक्शन है।")
