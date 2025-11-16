import streamlit as st
from PIL import Image
import io
import PyPDF2

# Initialize session state
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None

# Simple and clean CSS
st.markdown("""
<style>
    /* Reduce top padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Main background */
    .stApp {
        background: #1a1a2e;
    }
    
    /* Title styling */
    h1 {
        color: #eee;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    /* Subheader styling */
    h2, h3 {
        color: #16c79a;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Button styling - Simple and clean */
    .stButton > button {
        background: #16c79a;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 15px;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: 0.3s;
    }
    
    .stButton > button:hover {
        background: #19e3b4;
        transform: scale(1.02);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: #4a5fff;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 30px;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
    }
    
    .stDownloadButton > button:hover {
        background: #6677ff;
    }
    
    /* Text input */
    .stTextInput > div > div > input {
        background: #2a2a3e;
        border: 1px solid #16c79a;
        border-radius: 8px;
        color: white;
        padding: 10px;
    }
    
    .stTextInput label {
        color: white !important;
    }
    
    /* File uploader */
    .stFileUploader {
        background: #2a2a3e;
        border-radius: 8px;
        padding: 15px;
        border: 2px dashed #16c79a;
    }
    
    .stFileUploader label {
        color: #16c79a !important;
    }
    
    /* Success message */
    .stSuccess {
        background: #2a2a3e;
        border-left: 4px solid #16c79a;
        color: #16c79a;
    }
    
    /* Info message */
    .stInfo {
        background: #2a2a3e;
        border-left: 4px solid #4a5fff;
        color: #4a5fff;
    }
    
    /* Reduce spacing between elements */
    .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Column gap */
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    /* Horizontal line */
    hr {
        margin: 1rem 0;
        border-color: #16c79a;
    }
</style>
""", unsafe_allow_html=True)

st.title("📁 PDF & Image Tool")

# Create two columns for the card sections
col1, col2 = st.columns(2)

# Card 1: Images to PDF Converter
with col1:
    if st.button("📸 Images to PDF", key="card1", use_container_width=True):
        st.session_state.selected_option = "Images to PDF"

# Card 2: PDF Merger
with col2:
    if st.button("📄 PDF Merger", key="card2", use_container_width=True):
        st.session_state.selected_option = "PDF Merger"

st.markdown("---")

# Show selected option functionality
if st.session_state.selected_option == "Images to PDF":
    st.subheader("📸 Convert Images to PDF")
    
    uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="image_uploader")
    
    if uploaded_files:
        st.info(f"✅ {len(uploaded_files)} image(s) uploaded")
        images = []
        for file in uploaded_files:
            img = Image.open(file).convert("RGB")
            images.append(img)
        
        file_name = st.text_input("PDF file name", "output")
        
        if st.button("Convert to PDF", key="convert_btn"):
            pdf_bytes = io.BytesIO()
            images[0].save(pdf_bytes, format="PDF", save_all=True, append_images=images[1:])
            pdf_bytes.seek(0)

            st.success("✅ PDF created successfully!")
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_bytes,
                file_name=f"{file_name}.pdf",
                mime="application/pdf"
            )

elif st.session_state.selected_option == "PDF Merger":
    st.subheader("📄 Merge Multiple PDFs")
    
    uploaded_pdfs = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True, key="pdf_uploader")
    
    if uploaded_pdfs:
        st.info(f"✅ {len(uploaded_pdfs)} PDF(s) uploaded")
        
        merge_file_name = st.text_input("Merged file name", "merged_output")
        
        if st.button("Merge PDFs", key="merge_btn"):
            merger = PyPDF2.PdfMerger()
            
            for pdf in uploaded_pdfs:
                merger.append(pdf)
            
            merged_pdf_bytes = io.BytesIO()
            merger.write(merged_pdf_bytes)
            merged_pdf_bytes.seek(0)
            
            st.success("✅ PDFs merged successfully!")
            st.download_button(
                label="⬇️ Download Merged PDF",
                data=merged_pdf_bytes,
                file_name=f"{merge_file_name}.pdf",
                mime="application/pdf"
            )
else:
    st.info("👆 Click a button above to get started")
