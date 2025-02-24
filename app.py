import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.mapreduce import MapReduceChain

load_dotenv()

def summarize_pdf_langchain_gpt(pdf_file, prompt_option):
    """
    Summarizes PDF content using Langchain and Google Gemini model,
    with pre-defined prompt options.
    """
    if pdf_file is not None:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        if not text.strip():
            return "Error: No text could be extracted from the PDF"

        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

        # Pre-defined prompt templates
        prompt_templates = {
            "Concise Summary": """You are a highly skilled summarizer. Your task is to create a concise summary of the provided text. Focus on the main points and key ideas.

            Text to summarize:
            {text}

            CONCISE SUMMARY:""",
            
            "Bullet Points Summary": """You are a skilled information extractor. Your task is to identify and list the main points from the provided text in a bullet-point format.

            Text to analyze:
            {text}

            BULLET POINTS:""",
            
            "Detailed Summary": """You are a comprehensive summarizer. Your task is to create a detailed summary of the provided text, including main points, supporting details, and key findings.

            Text to summarize:
            {text}

            DETAILED SUMMARY:""",
            
            "Specific Summary": """You are an analytical summarizer. Your task is to analyze the provided text and summarize the key arguments, findings, and specific details.

            Text to analyze:
            {text}

            SPECIFIC SUMMARY:"""
        }

        # Select prompt template based on user option
        selected_template = prompt_templates.get(prompt_option, prompt_templates["Concise Summary"])

        # Create prompt with the correct input variable
        prompt = PromptTemplate(
            template=selected_template,
            input_variables=["text"]
        )

        try:
            # Create a simple chain
            chain = prompt | llm

            # Run the chain with the text
            result = chain.invoke({"text": text})
            
            return {"output_text": result.content}
            
        except Exception as e:
            return f"Error during summarization: {str(e)}"
    return None

def main():
    st.set_page_config(page_title="PDF Summarizer with Gemini")
    st.title("PDF Summarizing Tool (Powered by Gemini)")
    st.write("Upload a PDF and get an AI-generated summary using different styles.")
    st.divider()

    # Summary type selection
    prompt_options = [
        "Concise Summary",
        "Bullet Points Summary",
        "Detailed Summary",
        "Specific Summary"
    ]
    prompt_option = st.selectbox(
        "Choose summary style:",
        prompt_options,
        help="Select how you want your summary to be formatted"
    )

    # File uploader
    pdf = st.file_uploader('Upload your PDF Document', type='pdf')

    if pdf is not None:
        if st.button("Generate Summary"):
            with st.spinner(f"Generating {prompt_option.lower()}..."):
                summary_result = summarize_pdf_langchain_gpt(pdf, prompt_option)
                
                if summary_result:
                    if isinstance(summary_result, str) and summary_result.startswith("Error"):
                        st.error(summary_result)
                    else:
                        st.success("Summary generated successfully!")
                        st.header(f"{prompt_option}")
                        st.write(summary_result["output_text"])
                else:
                    st.error("Failed to process the PDF. Please try again.")
    else:
        st.info("Please upload a PDF file to begin.")

if __name__ == '__main__':
    main()