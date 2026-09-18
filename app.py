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
st.markdown("[Get Free API Key](https://aistudio.google.com/app/apikey)")

# 3. File Uploader
uploaded_file = st.file_uploader("कैथी की इमेज या पेज यहाँ अपलोड करें (JPG, PNG)", type=["jpg", "jpeg", "png"])

# 4. Displaying the Image and Translation logic
st.header("Original Kaithi Page")

# Condition check: Jab file upload hogi, tabhi aage ka kaam hoga
if uploaded_file is not None:
    # Image dikhane ka code
    st.image(uploaded_file, use_container_width=True)
    
    # 5. Translation Button
    if st.button("अनुवाद शुरू करें (Translate)"):
        # चेक करें कि API Key डाली गई है या नहीं
        if api_key == "":
            st.error("⚠️ कृपया सेटिंग्स में अपनी API Key दर्ज करें!")
        else:
            # लोडिंग स्पिनर दिखाना
            with st.spinner(f"{ai_choice} द्वारा अनुवाद किया जा रहा है... कृपया प्रतीक्षा करें..."):
                try:
                    # Image को AI के लिए तैयार करना
                    img = Image.open(uploaded_file)
                    
                    # Gemini API को सेट करना
                    genai.configure(api_key=api_key)
                    
                    # 404 Error से बचने के लिए लेटेस्ट मॉडल का इस्तेमाल
                    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
                    
                    # AI को निर्देश (Prompt) देना
                    prompt = "यह कैथी (Kaithi) लिपि में लिखा गया एक पुराना दस्तावेज़ है। कृपया इस इमेज को ध्यान से पढ़ें और इसका शुद्ध हिंदी में अनुवाद करें। अनुवाद करते समय ओरिजिनल फॉर्मेट बरकरार रखें।"
                    
                    # AI से जवाब (Translation) मँगवाना
                    response = model.generate_content([prompt, img])
                    
                    # असली रिजल्ट स्क्रीन पर दिखाना
                    st.success("✅ अनुवाद सफल रहा!")
                    st.subheader("Translated Text:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"अनुवाद के दौरान एरर आ गया। कृपया अपनी API Key चेक करें। एरर डिटेल: {e}")
else:
    st.info("कृपया अनुवाद शुरू करने के लिए कैथी लिपि की इमेज अपलोड करें।")
