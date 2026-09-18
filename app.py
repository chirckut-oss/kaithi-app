import google.generativeai as genai
import streamlit as st
from PIL import Image

# पेज कॉन्फिगरेशन
st.set_page_config(page_title="Kaithi Page Translator", layout="wide")

st.title("📜 Kaithi Page Translator (AI Powered)")
st.write(
    "कैथी लिपि का पेज अपलोड करें, और AI उसका ओरिजिनल फॉर्मेट बरकरार रखते हुए अनुवाद करेगा।"
)

# साइडबार या सेटिंग्स में API Key इनपुट
st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("Enter API Key", type="password")

# स्थानीय सुधार निर्देश (Custom Prompts)
st.sidebar.markdown("### 📝 स्थानीय सुधार निर्देश (Custom Prompts)")
custom_prompt = st.sidebar.text_area(
    "यहाँ सही नाम दर्ज करें (यदि कोई हो):",
    value="विशेष निर्देश: पुराने दस्तावेजों के आधार पर 'जगdv' या मिलते-जुलते नाम को हमेशा 'जगदेव सिंह' पढ़ें, और उत्तर दिशा के मकान के लिए 'शिवशरण सिंह' का संदर्भ लें।",
)

# इमेज अपलोड करने का विकल्प
uploaded_file = st.file_uploader(
    "कैथी की इमेज अपलोड करें (JPG, PNG)", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image, caption="Uploaded Image", use_column_width=True)

# अनुवाद बटन
if st.button("Translate to Hindi/English"):
  if not api_key:
    st.error("कृपया पहले अपनी API Key दर्ज करें!")
  elif not uploaded_file:
    st.error("कृपया अनुवाद के लिए कोई इमेज अपलोड करें!")
  else:
  try:
    # Google GenAI कॉन्फिगरेशन
    genai.configure(api_key=api_key)

    # मॉडल का नाम अपडेट करके gemini-3.6-flash किया गया है
    model_name = "models/gemini-3.6-flash"
    model = genai.GenerativeModel(model_name)

    # प्रॉम्प्ट तैयार करना
    prompt = f"""
            आप कैथी लिपि (Kaithi script) के पुराने दस्तावेजों को पढ़ने और अनुवाद करने में माहिर हैं।
            दिए गए निर्देश और कस्टम प्रॉम्प्ट का पालन करें:
            {custom_prompt}
            
            कृपया इस इमेज में दी गई कैथी लिपि को समझकर उसका सटीक हिंदी (या अंग्रेजी, जैसी आवश्यकता हो) में अनुवाद करें और उसका फॉर्मेट बनाए रखें।
            """

    with st.spinner("अनुवाद किया जा रहा है... कृपया प्रतीक्षा करें"):
      response = model.generate_content([prompt, image])

    st.subheader("अनुवाद परिणाम (Translation Result):")
    st.write(response.text)

  except Exception as e:
    st.error(f"त्रुटि (Error) आई है: {e}")
