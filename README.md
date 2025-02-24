# Smart PDF Summarizer

**Smart PDF Summarizer** is a Streamlit web application that lets you upload PDF documents and generate summaries using Google's advanced generative AI. It extracts text from your PDF and provides summaries in various formats, including concise, bullet points, detailed, or executive style, all while allowing you to control the maximum word count.

## Features

- **PDF Upload:** Easily upload your PDF documents (up to 10MB).
- **Custom Summary Styles:** Choose from Concise, Bullet Points, Detailed, or Executive summaries.
- **Word Limit Control:** Set the maximum number of words for the summary.
- **History & Downloads:** View previous summaries and download them as text files.
- **User-Friendly UI:** Clean and modern design with custom CSS.
- **Easy Deployment:** Run locally or deploy seamlessly on Streamlit Cloud.

## Technologies Used

- **Python** – Core programming language.
- **Streamlit** – For creating the interactive web interface.
- **PyPDF2** – To extract text from PDFs.
- **Langchain & ChatGoogleGenerativeAI** – For integrating Google's generative AI.
- **Custom CSS** – Enhances UI elements.

## Installation

1. **Clone the Repository:**
   git clone https://github.com/yourusername/smart-pdf-summarizer.git
   cd smart-pdf-summarizer
2. **Install Dependencies:Create a requirements.txt file with the following content**
   streamlit
   PyPDF2
   langchain_google_genai
   langchain
   Then run:
   pip install -r requirements.txt
3. **Set up Google API key:**
   GOOGLE_API_KEY = "your_google_api_key_here"
4. **Run locally by:**
   streamlit run app.py


