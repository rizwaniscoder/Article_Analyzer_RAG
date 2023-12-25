import streamlit as st
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from PyPDF2 import PdfReader
import base64
import tempfile
import os
from io import BytesIO
from llama_index.schema import Node
from llama_index.response_synthesizers import get_response_synthesizer

# Improved Function to extract text from PDF File with error handling
def read_pdf(uploaded_file):
    text = ""
    try:
        pdf = PdfReader(uploaded_file)
        for page in range(len(pdf.pages)):
            text += pdf.pages[page].extract_text()
    except Exception as e:
        st.error(f"Failed to process PDF file: {e}")
    finally:
        return text

# Streamlit app
def main():
    st.title('AI Custom Article Maker')

    # Inputs from User
    st.sidebar.subheader('Input Data')
    
    # Template input options
    template_input_option = st.sidebar.selectbox("Select template input option:", ["Upload PDF", "Enter Text"])
    if template_input_option == "Upload PDF":
        template_pdf = st.sidebar.file_uploader("Upload template PDF (for style and structure)", type=['pdf', 'docx', 'txt'])
        template_article = read_file(template_pdf)
    else:
        template_article = st.sidebar.text_area('Enter Template Text:')
    
    primary_keyword = st.sidebar.text_input('Enter Primary Keyword:')
    article_length = int(st.sidebar.number_input('Enter Article Length:'))
    article_structure = st.sidebar.text_area('Enter Article Structure (Headings):')

    # Data input options
    data_input_option = st.sidebar.selectbox("Select data input option:", ["Upload PDF", "Enter Text"])
    if data_input_option == "Upload PDF":
        data_pdf = st.sidebar.file_uploader("Upload data PDF for this article", type=['pdf', 'docx', 'txt'])
        data_article = read_file(data_pdf)
    else:
        data_article = st.sidebar.text_area('Enter Data Text:')

    # Initialize response outside of the try block
    response = None

    # Handling None, ensures that we do not get a NoneType error.
    if template_article and data_article:
        st.sidebar.write('Template Article:')
        st.sidebar.write(template_article)

        # Create temporary files for the template and data
        with tempfile.TemporaryDirectory() as temp_dir:
            template_file_path = os.path.join(temp_dir, 'template.txt')
            data_file_path = os.path.join(temp_dir, 'data.txt')

            with open(template_file_path, 'w', encoding='utf-8') as template_file:
                template_file.write(template_article)

            with open(data_file_path, 'w', encoding='utf-8') as data_file:
                data_file.write(data_article)

            # Check if the index already exists
            if not os.path.exists("./storage"):
                # Load the documents and create the index
                documents = SimpleDirectoryReader(temp_dir).load_data()
                index = VectorStoreIndex.from_documents(documents)
                # Store it for later
                index.storage_context.persist()
            else:
                # Load the existing index
                storage_context = StorageContext.from_defaults(persist_dir="./storage")
                index = load_index_from_storage(storage_context)

            # Query the index
            query_engine = index.as_query_engine(response_synthesizer=get_response_synthesizer(response_mode="compact"))
            try:
                response = query_engine.query(data_article)
                
                # Check if there are any results
                if response:
                    final_article = get_analysis_result(response)
                    st.write('Generated Article:')
                    st.write(final_article)

                    # Download button for the final result
                    download_button_str = create_download_link(final_article)
                    st.markdown(download_button_str, unsafe_allow_html=True)
                else:
                    st.warning("No matching nodes found in the query response.")

            except Exception as e:
                st.error(f"Failed to generate the article: {e}")
    else:
        st.sidebar.error("Failed to get input data.")

def get_analysis_result(response):
    # Function to get a meaningful representation of the analysis result
    if hasattr(response, 'responsestr'):
        return response.responsestr
    elif hasattr(response, 'response'):
        return response.response
    else:
        return str(response)

def create_download_link(result):
    # Function to create a download link for the analysis result
    b64 = base64.b64encode(result.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="generated_article.txt">Download Generated Article</a>'
    return href

def read_file(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            return read_pdf(uploaded_file)
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
            return uploaded_file.read().decode("utf-8")
        else:
            st.error("Unsupported file format. Please upload a PDF, Word, or Text file.")
    return ""

if __name__ == '__main__':
    main()
