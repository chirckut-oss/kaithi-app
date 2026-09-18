import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Kaithi Page Translator", page_icon="📜")

# 2. Header & Title
st.title("📜 Kaithi Page Translator (AI Powered)")
st.write("कैथी लिपि का पेज अपलोड करें, और AI उसका ओरिजिनल फॉर्मेट बरकरार रखते हुए अनुवाद करेगा।")

# 3. Settings (API Key)
st.header("⚙️ Settings")
api_key = st.text_input("Enter API Key", type="password")

# 4. Image Upload
uploaded_file = st.file_uploader("कैथी की इमेज अपलोड करें (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# 5. Translate Button and Logic
if st.button("अनुवाद शुरू करें (Translate)"):
    if not api_key:
        st.warning("⚠️ कृपया अनुवाद शुरू करने से पहले अपना Google API Key दर्ज करें।")
    elif uploaded_file is None:
        st.warning("⚠️ कृपया कैथी लिपि की कोई इमेज अपलोड करें।")
    else:
        try:
            with st.spinner("AI अनुवाद कर रहा है, कृपया प्रतीक्षा करें..."):
                # API सेटअप
                genai.configure(api_key=api_key)
                
                # फिक्स किया गया मॉडल नाम
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                # प्रॉम्प्ट (AI को निर्देश)
                prompt = "Read the handwritten Kaithi script in this image and translate it into Hindi. Please maintain the original format, structure, and meaning as accurately as possible."
                
                # AI से रिस्पांस लेना
                response = model.generate_content([prompt, image])
                
                # परिणाम दिखाना
                st.success("अनुवाद सफल!")
                st.markdown("### अनुवादित टेक्स्ट:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"❌ एक समस्या आई: {e}")
