import streamlit as st
from PIL import Image
import pytesseract
import requests

# Configure page
st.set_page_config(page_title="Classroom OCR + Groq AI", layout="centered")

# Title
st.title("📸 OCR + 🧠 Groq AI (Mistral)")

# File uploader
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

# Process image
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded", use_container_width=True)  # fixed deprecated param

    # OCR
    with st.spinner("🧾 Extracting text from image..."):
        text = pytesseract.image_to_string(image)
        st.text_area("📝 OCR Result", text, height=200)

    # Ask Groq AI
    if st.button("Ask AI to explain it"):
        if not text.strip():
            st.warning("OCR result is empty. Please upload a clearer image.")
        else:
            with st.spinner("🧠 Groq AI thinking..."):

                headers = {
                    "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": "llama3-70b-8192",  # ✅ Valid Groq model
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful teacher who explains OCR-extracted content clearly to students."
                        },
                        {
                            "role": "user",
                            "content": f"Please explain the following extracted text in simple terms:\n\n{text}"
                        }
                    ]
                }

                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload
                )

                # Handle response
                if response.status_code == 200:
                    result = response.json()["choices"][0]["message"]["content"]
                    st.success("🧠 Groq AI's Response:")
                    st.markdown(result)
                else:
                    st.error(f"Groq API Error {response.status_code}")
                    st.code(response.text)  # Show full error
