import google.generativeai as genai
import streamlit as st
from PIL import Image

# पेज की सेटिंग
st.set_page_config(
    page_title="Kaithi Page Translator · Streamlit", page_icon="📜"
)

st.title("📜 Kaithi Page Translator (AI Powered)")
st.write(
    "कैथी लिपि का पेज अपलोड करें, और AI उसका ओरिजिनल फॉर्मेट बरकरार रखते हुए अनुवाद करेगा।"
)

# साइडबार या सेटिंग्स सेक्शन
st.sidebar.header("⚙️ Settings")
api_key = st.sidebar.text_input("Enter API Key", type="password")

# उपयोगकर्ता की सुविधा के लिए कस्टम निर्देश (Custom Glossary/Instructions) बॉक्स
st.sidebar.header("📝 स्थानीय सुधार निर्देश (Custom Prompts)")
custom_notes = st.sidebar.text_area(
    "यहाँ सही नाम दर्ज करें (यदि कोई हो):",
    value=(
        "विशेष निर्देश: पुराने दस्तावेजों के आधार पर 'जगdv' या मिलते-जुलते नाम"
        " को हमेशा 'जगदेव सिंह' पढ़ें, और उत्तर दिशा के मकान के लिए 'शिवशरण"
        " सिंह' का संदर्भ लें।"
    ),
    help="AI को सही नाम और संदर्भ सिखाने के लिए यहाँ बदलाव कर सकते हैं।",
)

# इमेज अपलोड करने का विकल्प
uploaded_file = st.file_uploader(
    "कैथी की इमेज अपलोड करें (JPG, PNG)", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image, caption="Uploaded Image", use_container_width=True)

if st.button("Translate to Hindi/English"):
  if not api_key:
    st.error("कृपया पहले अपनी Gemini API Key दर्ज करें!")
  elif uploaded_file is None:
    st.error("कृपया अनुवाद के लिए पहले कोई इमेज अपलोड करें!")
  else:
    with st.spinner("अनुवाद हो रहा है, कृपया प्रतीक्षा करें..."):
      try:
        # API Key कॉन्फ़िगर करें
        genai.configure(api_key=api_key)

        # मजबूत सिस्टम प्रॉम्ट और स्थानीय संदर्भ जोड़ना
        system_instruction = (
            "आप कैथी लिपि (Kaithi Script) के ऐतिहासिक दस्तावेजों, खतियान"
            " और चौहद्दी (boundaries) को पढ़ने के विशेषज्ञ हैं। पुराने"
            " दस्तावेजों में हाथ से लिखे गए शब्द अस्पष्ट हो सकते हैं। "
            f"अतिरिक्त निर्देश और स्थानीय संदर्भ: {custom_notes}\n\n"
            "दस्तावेज का लाइन-बाय-लाइन लिप्यंतरण (Transcription in"
            " Devanagari) और हिंदी/अंग्रेज़ी अनुवाद करें, मूल लेआउट और फॉर्मेट"
            " को बरकरार रखते हुए।"
        )

        # Gemini मॉडल सेट करें (gemini-2.5-flash या उपयुक्त मॉडल)
        generation_config = {"temperature": 0.2}
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction,
            generation_config=generation_config,
        )

        # इमेज के साथ प्रॉम्ट भेजना
        prompt = (
            "इस कैथी लिपि के पेज का सटीक लिप्यंतरण और अनुवाद देवनागरी और"
            " अंग्रेजी में करें।"
        )
        response = model.generate_content([image, prompt])

        st.success("अनुवाद पूरा हुआ!")
        st.markdown("## Translation Result:")
        st.write(response.text)

      except Exception as e:
        st.error(f"त्रुटि (Error) आई है: {e}")
