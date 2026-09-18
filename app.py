import streamlit as st
from PIL import Image
from aksharamukha import transliterate

st.set_page_config(page_title="कैथी अनुवादक", layout="centered")

st.title("📜 कैथी लिपि अनुवादक")
st.write("दस्तावेज़ की फोटो खींचें या अपलोड करें:")

option = st.radio("इनपुट चुनें:", ("कैमरा (Camera)", "फाइल अपलोड (Upload)"))

image_file = None
if option == "कैमरा (Camera)":
    image_file = st.camera_input("फोटो खींचें")
else:
    image_file = st.file_uploader("इमेज चुनें", type=["jpg", "jpeg", "png"])

if image_file is not None:
    img = Image.open(image_file)
    st.image(img, caption="अपलोड किया गया दस्तावेज़", use_container_width=True)
    st.divider()

kaithi_text = st.text_area("कैथी टेक्स्ट दर्ज करें:", placeholder="कैथी शब्द यहाँ लिखें...")

if st.button("हिंदी में अनुवाद करें"):
    if kaithi_text.strip():
        hindi_result = transliterate.process('Kaithi', 'Devanagari', kaithi_text)
        st.success("अनुवादित हिंदी:")
        st.markdown(f"### {hindi_result}")
    else:
        st.warning("कृपया अनुवाद करने के लिए कुछ टेक्स्ट लिखें।")
