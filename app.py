import streamlit as st
import easyocr
import cv2
import os
import tempfile
from symspellpy import SymSpell, Verbosity
from context_correction import correct_text
import language_tool_python

# Streamlit page setup
st.set_page_config(page_title="Handwritten Notes AI", layout="wide")
st.markdown("<h1 style='color:red;text-align:center;'>AI Handwritten Notes Digitizer</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:black;text-align:center;'>Upload or Scan ➤ OCR ➤ Spell ➤ Grammar ➤ Download</h3>", unsafe_allow_html=True)

# Load OCR, grammar, and spell correction tools
reader = easyocr.Reader(['en'])
tool = language_tool_python.LanguageTool('en-US')
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
sym_spell.load_dictionary("frequency_dictionary_en_82_765.txt", 0, 1)

# OCR Function
def perform_ocr(img_path):
    image = cv2.imread(img_path)
    result = reader.readtext(image)
    return " ".join([text for _, text, _ in result])

# Spell correction function
def correct_spelling(text):
    suggestions = sym_spell.lookup_compound(text, max_edit_distance=2)
    return suggestions[0].term if suggestions else text

# Input mode
input_mode = st.radio("Choose Input Type:", ["Upload from Device", "Capture from Camera"])

img_path = None
if input_mode == "Upload from Device":
    file = st.file_uploader("📁 Upload handwritten image", type=["jpg", "jpeg", "png"])
    if file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp.write(file.read())
            img_path = temp.name
            st.image(img_path, caption="Uploaded Image", use_container_width=True)

elif input_mode == "Capture from Camera":
    camera_input = st.camera_input("📸 Take a photo")
    if camera_input:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp.write(camera_input.read())
            img_path = temp.name
            st.image(img_path, caption="Captured Image", use_container_width=True)

# Processing steps
if img_path and st.button("🚀 Start Processing"):
    st.info("🔍 Step 1: OCR in progress...")
    raw_text = perform_ocr(img_path)
    st.code(raw_text, language='markdown')

    st.info("🔤 Step 2: Spell Correction in progress...")
    spell_text = correct_spelling(raw_text)
    st.code(spell_text, language='markdown')

    st.download_button("📥 Download Spell-Corrected Output", spell_text, file_name="spell_corrected.txt", mime="text/plain")

    st.info("🧠 Step 3: Grammar Correction in progress...")
    final_text, errors = correct_text(spell_text)

    st.success("✅ Final Output")
    st.text_area("Corrected Text", final_text, height=200)

    if errors:
        st.warning("⚠️ Grammar Issues Detected:")
        for err in errors:
            st.write(f"- {err}")
    else:
        st.info("🟢 No grammar issues found.")

    st.download_button("📥 Download Final Output", final_text, file_name="final_output.txt", mime="text/plain")
