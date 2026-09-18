import streamlit as st
import requests
import base64

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
                    # इमेज को बाइनरी (Base64) में बदलना
                    base64_image = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                    mime_type = uploaded_file.type

                    # Google API को सीधा कॉल करना (बिना किसी लाइब्रेरी के)
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    headers = {'Content-Type': 'application/json'}
                    payload = {
                        "contents": [{
                            "parts": [
                                {"text": "यह कैथी (Kaithi) लिपि में लिखा गया एक दस्तावेज़ है। कृपया इस इमेज को ध्यान से पढ़ें और इसका शुद्ध हिंदी में अनुवाद करें।"},
                                {"inline_data": {"mime_type": mime_type, "data": base64_image}}
                            ]
                        }]
                    }
                    
                    # रिज़ल्ट मँगवाना
                    response = requests.post(url, headers=headers, json=payload)
                    data = response.json()

                    # रिज़ल्ट स्क्रीन पर दिखाना
                    if response.status_code == 200:
                        st.success("✅ अनुवाद सफल रहा!")
                        st.write(data['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"Google Server Error: {data['error']['message']}")
                        
                except Exception as e:
                    st.error(f"System Error: {e}")
