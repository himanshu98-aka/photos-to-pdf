import streamlit as st
from PIL import Image
import io
import PyPDF2

st.title("PDF & Image Tool")

# Ask user to choose between PDF merger or image converter
option = st.radio("Choose an option:", ["Images to PDF Converter", "PDF Merger"])

if option == "Images to PDF Converter":
    st.subheader("Convert Images to PDF")
    
    # Upload multiple images
    uploaded_files = st.file_uploader("Upload JPG or PNG images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files:
        images = []
        for file in uploaded_files:
            img = Image.open(file).convert("RGB")
            images.append(img)
        
        # Ask user for file name
        file_name = st.text_input("Enter file name (without .pdf extension)", "output")
        
        if st.button("Convert to PDF"):
            pdf_bytes = io.BytesIO()
            images[0].save(pdf_bytes, format="PDF", save_all=True, append_images=images[1:])
            pdf_bytes.seek(0)

            st.success("PDF generated successfully!")
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"{file_name}.pdf",
                mime="application/pdf"
            )

elif option == "PDF Merger":
    st.subheader("Merge Multiple PDFs")
    
    # Upload multiple PDF files
    uploaded_pdfs = st.file_uploader("Upload PDF files to merge", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_pdfs:
        # Ask user for merged file name
        merge_file_name = st.text_input("Enter merged file name (without .pdf extension)", "merged_output")
        
        if st.button("Merge PDFs"):
            merger = PyPDF2.PdfMerger()
            
            for pdf in uploaded_pdfs:
                merger.append(pdf)
            
            merged_pdf_bytes = io.BytesIO()
            merger.write(merged_pdf_bytes)
            merged_pdf_bytes.seek(0)
            
            st.success("PDFs merged successfully!")
            st.download_button(
                label="Download Merged PDF",
                data=merged_pdf_bytes,
                file_name=f"{merge_file_name}.pdf",
                mime="application/pdf"
            )
