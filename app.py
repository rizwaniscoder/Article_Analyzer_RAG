import streamlit as st
import os
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from PyPDF2 import PdfReader
import base64
from io import BytesIO

# Improved Function to extract text from PDF File with error handling
def read_pdf(uploaded_file):
    text = ""
    try:
        pdf = PdfReader(uploaded_file)
        # Use len(reader.pages) instead of deprecated getNumPages
        for page in range(len(pdf.pages)):
            text += pdf.pages[page].extract_text()
    except Exception as e:
        st.error(f"Failed to process PDF file: {e}")
    finally:
        return text

# Streamlit app
def main():
    st.title('Article Analyzer App')

    # Initialize index at app start
    path = os.getcwd() + "/storage"
    if not os.path.exists(path):
        documents = SimpleDirectoryReader("data").load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist()
    else:
        storage_context = StorageContext.from_defaults(persist_dir=path)
        index = load_index_from_storage(storage_context)

    # Inputs from User
    st.sidebar.subheader('Input Data')
    uploaded_file = st.sidebar.file_uploader("Upload your PDF file", type=['pdf'])
    primary_keyword = st.sidebar.text_input('Enter Primary Keyword:')
    # Convert article_length to integer
    article_length = int(st.sidebar.number_input('Enter Article Length:'))
    article_structure = st.sidebar.text_area('Enter Article Structure (Headings):')

    # Initialize response outside of the try block
    response = None

    # Handling None, ensures that we do not get a NoneType error.
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.sidebar.write(file_details)

        if st.sidebar.button('Analyze'):
            st.sidebar.write('Analyzing...')
            
            # Handle NoneType error when no file is uploaded
            sample_article = read_pdf(uploaded_file)
            if sample_article:
                st.sidebar.write('Sample Article:')
                st.sidebar.write(sample_article)

                # LlamaIndex and Analysis
                query_engine = index.as_query_engine()
                try:
                    response = query_engine.query(sample_article)
                    st.write('Analysis Result:')
                    st.write(get_analysis_result(response))
                except Exception as e:
                    st.error(f"Failed to analyze the article: {e}")
            else:
                st.sidebar.error("Failed to extract text from the PDF file.")

    # Download button for the final result
    if response:
        download_button_str = create_download_link(get_analysis_result(response))
        st.markdown(download_button_str, unsafe_allow_html=True)

def get_analysis_result(response):
    # Function to get a meaningful representation of the analysis result
    if hasattr(response, 'responsestr'):
        return response.responsestr
    elif hasattr(response, 'response'):
        return response.response
    elif hasattr(response, '__iter__'):
        return "\n".join(map(str, response))
    else:
        return str(response)

def create_download_link(result):
    # Function to create a download link for the analysis result
    b64 = base64.b64encode(result.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="analysis_result.txt">Download Analysis Result</a>'
    return href

if __name__ == '__main__':
    main()
