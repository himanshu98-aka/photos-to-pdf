import streamlit as st
from PIL import Image
import io

st.title("Image to PDF Converter")

# Upload multiple images
uploaded_files = st.file_uploader("Upload JPG or PNG images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    images = []
    for file in uploaded_files:
        img = Image.open(file).convert("RGB")
        images.append(img)
    name = st.text_input("output file name :")
    if name:
        if st.button("Convert to PDF"):
            pdf_bytes = io.BytesIO()
            images[0].save(pdf_bytes, format="PDF", save_all=True, append_images=images[1:])
            pdf_bytes.seek(0)

            st.success("PDF generated successfully!")
            
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"{name}.pdf",
                mime="application/pdf"
            )
