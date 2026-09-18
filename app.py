import streamlit as st
from PIL import Image

# 1. UI Setup aur Title
st.title("📜 Kaithi Page Translator (AI Powered)")
st.write("कैथी लिपि का पेज अपलोड करें, और AI उसका ओरिजिनल फॉर्मेट और पैराग्राफ स्टाइल बरकरार रखते हुए अनुवाद करेगा।")

# 2. Settings Section
st.header("⚙️ Settings")
ai_choice = st.radio("अनुवाद के लिए AI चुनें:", ("Google Gemini (Free)", "ChatGPT (OpenAI - GPT-4o)"))
api_key = st.text_input("Enter Google Gemini API Key", type="password")
st.markdown("[Get Free Gemini API Key](#)")

# 3. File Uploader
uploaded_file = st.file_uploader("कैथी की इमेज या पेज यहाँ अपलोड करें (JPG, PNG)", type=["jpg", "jpeg", "png"])

# 4. Displaying the Image (Error fix is here)
st.header("Original Kaithi Page")

# Condition check: Jab file upload hogi, tabhi image display hogi
if uploaded_file is not None:
    # Image ko PIL ke through open karein
    image = Image.open(uploaded_file)
    
    # Image ko display karein (Ab yahan line 47 par error nahi aayega)
    st.image(image, use_column_width=True)
    
    # Yahan aap apne AI translation ka aage ka code likh sakte hain
    # st.write("Translating...")
else:
    # Agar file upload nahi hui hai, toh ek message dikhayein
    st.info("कृपया अनुवाद शुरू करने के लिए कैथी लिपि की इमेज अपलोड करें।")
