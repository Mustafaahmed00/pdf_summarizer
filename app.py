import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Smart PDF Summarizer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load API key from Streamlit secrets
os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]

# Custom CSS
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            height: 3em;
            background-color: #4CAF50;
            color: white;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .upload-text {
            text-align: center;
            padding: 2rem;
            border: 2px dashed #ccc;
            border-radius: 10px;
        }
        .success-box {
            padding: 1rem;
            background-color: #f0f8f0;
            border-radius: 10px;
            border-left: 5px solid #4CAF50;
        }
        .error-box {
            padding: 1rem;
            background-color: #fff0f0;
            border-radius: 10px;
            border-left: 5px solid #ff0000;
        }
        .stProgress > div > div {
            background-color: #4CAF50;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # Model parameters
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.1,
                          help="Higher values make the output more creative")
    
    # Word limit
    max_words = st.number_input("Maximum words in summary", 100, 1000, 300)
    
    # Clear history button
    if st.button("Clear History"):
        st.session_state.history = []
        st.success("History cleared!")

def process_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        total_pages = len(reader.pages)
        
        progress_bar = st.progress(0)
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text
            progress_bar.progress((i + 1) / total_pages)
        return text.strip()
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def get_prompt_template(prompt_option, max_words):
    templates = {
        "Concise Summary": f"""As a professional summarizer, create a clear and concise summary of the following text in no more than {max_words} words.
Focus on the key points and main ideas.

TEXT:
{{text}}

CONCISE SUMMARY:""",
        
        "Bullet Points Summary": f"""Extract and list the main points from the following text in bullet points.
Limit the total response to {max_words} words and ensure each point is clear and informative.

TEXT:
{{text}}

BULLET POINTS:""",
        
        "Detailed Summary": f"""Create a comprehensive summary of the following text, including main points,
supporting details, and key findings. Limit the summary to {max_words} words.

TEXT:
{{text}}

DETAILED SUMMARY:""",
        
        "Executive Summary": f"""Provide an executive summary of the following text, highlighting strategic points,
key findings, and recommendations. Keep the summary under {max_words} words and maintain a professional tone.

TEXT:
{{text}}

EXECUTIVE SUMMARY:"""
    }
    return templates.get(prompt_option, templates["Concise Summary"])

def check_file_size(file):
    MAX_SIZE = 10 * 1024 * 1024  # 10MB
    if file.size > MAX_SIZE:
        st.error("File size exceeds 10MB limit. Please upload a smaller file.")
        return False
    return True

def summarize_text(text, prompt_option, temperature, max_words):
    try:
        if not os.getenv('GOOGLE_API_KEY'):
            st.error("Please enter your Google API Key in the sidebar.")
            return None
            
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=temperature
        )
        
        prompt = PromptTemplate(
            template=get_prompt_template(prompt_option, max_words),
            input_variables=["text"]
        )
        
        # Create chain
        chain = prompt | llm
        
        # Run chain
        result = chain.invoke({"text": text})
        return result.content
        
    except Exception as e:
        st.error(f"Error during summarization: {str(e)}")
        return None

def main():
    st.title("📚 Smart PDF Summarizer")
    st.markdown("---")
    
    # Summary type selection
    prompt_options = [
        "Concise Summary",
        "Bullet Points Summary",
        "Detailed Summary",
        "Executive Summary"
    ]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        prompt_option = st.selectbox(
            "Choose summary style:",
            prompt_options,
            help="Select how you want your summary to be formatted"
        )
    
    # File upload
    pdf_file = st.file_uploader(
        "Upload your PDF Document",
        type='pdf',
        help="Maximum file size: 10MB"
    )
    
    if pdf_file is not None:
        if not check_file_size(pdf_file):
            return
            
        if st.button("Generate Summary"):
            if not os.getenv('GOOGLE_API_KEY'):
                st.error("Please enter your Google API Key in the sidebar first.")
                return
                
            with st.spinner("Processing your PDF..."):
                text = process_pdf(pdf_file)
                
                if text:
                    with st.spinner("Generating summary..."):
                        summary = summarize_text(text, prompt_option, temperature, max_words)
                        
                        if summary:
                            st.session_state.history.append({
                                'filename': pdf_file.name,
                                'summary_type': prompt_option,
                                'summary': summary,
                                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                            })
                            
                            st.markdown("### 📝 Summary")
                            st.markdown(f"<div class='success-box'>{summary}</div>",
                                        unsafe_allow_html=True)
                            
                            word_count = len(summary.split())
                            st.info(f"Word count: {word_count}")
                            
                            st.download_button(
                                "Download Summary",
                                summary,
                                file_name=f"summary_{pdf_file.name}.txt",
                                mime="text/plain"
                            )
    else:
        st.markdown(
            "<div class='upload-text'>📤 Drag and drop your PDF here</div>",
            unsafe_allow_html=True
        )
    
    if st.session_state.history:
        st.markdown("### 📚 Previous Summaries")
        for item in reversed(st.session_state.history):
            with st.expander(f"{item['filename']} - {item['summary_type']} ({item['timestamp']})"):
                st.write(item['summary'])

if __name__ == '__main__':
    main()
