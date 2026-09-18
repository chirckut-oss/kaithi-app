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
            with st.spinner("AI model check kiya ja raha hai aur anuvad ho raha hai..."):
                try:
                    # 1. Pehle check karte hain ki aapki API key par kaunse models available hain
                    models_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
                    models_res = requests.get(models_url).json()
                    
                    best_model = "models/gemini-1.5-flash" # Default fallback
                    
                    if "models" in models_res:
                        for m in models_res["models"]:
                            # Aisa model dhundho jo text/image generate kar sake
                            if "generateContent" in m.get("supportedGenerationMethods", []) and "1.5" in m.get("name", ""):
                                best_model = m["name"]
                                if "flash" in best_model:  # Flash sabse fast hai
                                    break
                    
                    # 2. Image ko base64 format me convert karna
                    base64_image = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                    mime_type = uploaded_file.type

                    # 3. Direct Google API ko request bhejna (Bina kisi library ke)
                    url = f"https://generativelanguage.googleapis.com/v1beta/{best_model}:generateContent?key={api_key}"
                    headers = {'Content-Type': 'application/json'}
                    payload = {
                        "contents": [{
                            "parts": [
                                {"text": "यह कैथी (Kaithi) लिपि में लिखा गया एक दस्तावेज़ है। कृपया इस इमेज को ध्यान से पढ़ें और इसका शुद्ध हिंदी में अनुवाद करें।"},
                                {"inline_data": {"mime_type": mime_type, "data": base64_image}}
                            ]
                        }]
                    }
                    
                    response = requests.post(url, headers=headers, json=payload)
                    data = response.json()

                    # 4. Result display karna
                    if response.status_code == 200:
                        st.success(f"✅ अनुवाद सफल रहा! (Model used: {best_model})")
                        st.write(data['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"Google Server Error: {data.get('error', {}).get('message', 'Unknown Error')}")
                        
                except Exception as e:
                    st.error(f"System Error: {e}")
