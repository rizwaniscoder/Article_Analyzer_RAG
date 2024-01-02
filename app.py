# Import necessary Python Libraries
import streamlit as st
import PyPDF2
import openai
import io
import os
import logging  # For catching general errors

# Function to read PDF files
def read_pdf(file):
    try:
        # Create a PDF object
        pdf_file_obj = PyPDF2.PdfReader(io.BytesIO(file))
        # Extract text from each page
        text = ' '.join(page.extract_text() for page in pdf_file_obj.pages)
    except Exception as e:
        # Log the error and display a user-friendly message
        logging.error("Error in reading PDF: %s", str(e))
        st.error("There was an error reading the PDF file. Make sure the file is a readable PDF file.")
        return ''
    return text

# Function to generate article structure
def generate_article_structure(headings):
    if headings:
        return [heading.strip() for heading in headings.split(',')]
    else:
        return []

# Function to generate article using OpenAI GPT model
def generate_article(input_text, headings, tokens, primary_keyword, openai_api_key):
    try:
        # Guidelines to include in the prompt
        guidelines_prompt = """
        Guidelines
        
        Introduction:
        
        - The intro should ALWAYS be at most 60-80 words and should contain the main keyword.
        
        Text Styling:
        
        - Bold important bits of text or sentences. This makes it easy for one to skim through the post. But, please, don’t overdo this.
        
        - Avoid Italics and underlining words, unless you have to. Bolding is often more than enough.
        
        - Keep your sentences short. When writing most (at least 90%) of your sentences should be less than 20 words long. And there shouldn’t be any sentence that goes beyond 35 words in length.
        
        For example:
        
        “… In my opinion…”
        
        “… I can comfortably say…”
        
        “… If you ask me…”
        
        Paragraphs:
        
        - Keep them short. Your paragraphs should be at most 4 lines (not sentences) long. You want the reader to read through it as easy and fast as possible. So keep them short and punchy – not more than 60 words per paragraph.
        
        - Break down big points into multiple paragraphs. That way your text will look more organized, easy to read, and appealing.
        
        
        Tone and Engagement:
        
        - Always keep the tone light and engaging. Try to make it as conversational as possible to keep the reader actively engaged. This makes reading fun and even more appealing.
        
        - To do so, ask rhetorical questions along the way, use exclamations, and slide in a joke or two.
        
        - You also want to avoid any sensitive topics, words, or names that might make the reader angry. That way you won’t lose their interest in the post mid-way.
        
        - Always maintain a friendly, yet, professional tone. That way the reader not only feels comfortable but also trusts what you’ve written.
        
        
        Points Of View Usage:
        
        - Write from the first-person point of view using pronouns like I, me, and my. E.g. “I’ve done this haircut several times and never felt any difficulty at all…”
        """

        openai.api_key = openai_api_key

        generated_articles = []

        for heading in headings:
            # Merge the input text and guidelines into the prompt
            prompt = f"Please make the Article focusing on the keyword {primary_keyword}\n\nHere is the Heading {heading}\n\n{guidelines_prompt}\n\nHere's the Sample Article {input_text}"
            # Invoke openai API's chat completions for text generation
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=tokens
            )
            text = response.choices[0].message['content']
            generated_articles.append({heading: text})

        return generated_articles
    except Exception as e:
        # Log the error and the input causing it, and return a user-friendly message
        logging.error("Error in generating article: %s", str(e))
        logging.error("Input text causing the issue: %s", input_text)
        return []

# Main Streamlit Application
def main():
    st.title('Perfect Article Generator')

    openai_api_key = st.text_input('Enter your OpenAI API Key', type='password')

    uploaded_pdf_file = st.file_uploader("Choose a PDF file", type="pdf")
    primary_keyword = st.text_input('Enter your primary keyword')
    article_length = st.number_input('Enter desired article length', min_value=500, max_value=10000, step=500)
    article_structure_input = st.text_input('Enter article structure - Headings (separated by comma)')

    if st.button('Generate Article'):
        sample_article = ""
        if uploaded_pdf_file:
            # Extract text from the uploaded PDF file
            sample_article = read_pdf(uploaded_pdf_file.getvalue())
            # Display uploaded document text in the sidebar
            st.sidebar.subheader("Uploaded Document Text:")
            st.sidebar.text(sample_article)

        headings = generate_article_structure(article_structure_input)
        total_headings = len(headings)

        if total_headings:
            tokens = article_length // total_headings
            # Simulate waiting with a loading spinner
            with st.spinner("Generating Articles. Please Wait..."):
                generated_articles = generate_article(sample_article, headings, tokens, primary_keyword, openai_api_key)

            result = "\n\n".join(f"{list(article.keys())[0]}\n{list(article.values())[0]}" for article in generated_articles)

            st.text_area("Generated Article", value=result, height=500)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
