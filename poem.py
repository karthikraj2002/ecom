# poeticloveai_app.py

import streamlit as st
from fpdf import FPDF
import google.generativeai as genai
from io import BytesIO

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyBJJM78BQX51IYLYMq995g7lVWw-Bkpsoo")
model = genai.GenerativeModel("gemini-1.5-flash")  # You can use "gemini-pro" if needed

# --- Streamlit App Setup ---
st.set_page_config(page_title="PoeticLoveAI", page_icon="💘", layout="centered")
st.title("💖 PoeticLoveAI")
st.markdown("Create beautiful poems and lyrics for your loved ones 💌")

# --- User Input Area ---
prompt = st.text_area(
    "What would you like your poem or lyrics to be about?",
    placeholder="e.g., My first date under the stars"
)
format_type = st.selectbox("Choose Format", ["Poem", "Lyrics"])
tone = st.radio("Choose Tone", ["Romantic", "Sad", "Fun", "Dramatic", "Short & Cute"])

# --- Initialize Session State ---
if 'last_input' not in st.session_state:
    st.session_state['last_input'] = ''
    st.session_state['output'] = ''

# --- Generate/Regenerate Button ---
if st.button("💘 Generate" if st.session_state['last_input'] == '' else "🔁 Regenerate"):
    if prompt.strip() == "":
        st.warning("Please enter something to write about.")
    else:
        prompt_text = f"Write a {tone.lower()} {format_type.lower()} about: {prompt}"
        try:
            response = model.generate_content(prompt_text)
            content = response.text if response.text else "⚠️ Unable to generate content."
            st.session_state['output'] = content
            st.session_state['last_input'] = prompt
        except Exception as e:
            st.error(f"API Error: {e}")

# --- Show Output & Download ---
if st.session_state['output']:
    st.subheader("🎶 Your AI-Generated Masterpiece")
    st.write(st.session_state['output'])

    # --- Generate PDF in memory ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in st.session_state['output'].split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf_buffer = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_buffer.write(pdf_bytes)
    pdf_buffer.seek(0)
