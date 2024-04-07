# Perfect Article Generator

This Streamlit application generates perfect articles based on a PDF file input using OpenAI's GPT-4 model.

## Features

- **PDF Input**: Upload a PDF file containing the text for article generation.
- **Keyword Focused**: Generate articles focusing on a primary keyword.
- **Custom Structure**: Define the structure of the article using headings.
- **Article Length**: Control the length of the generated article.
- **OpenAI Integration**: Utilizes OpenAI's GPT-4 model for text generation.

## Prerequisites

Before running the application, make sure you have the following:

- Python installed on your machine
- OpenAI API key
- Streamlit library
- PyPDF2, logging Python libraries

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your_username/perfect-article-generator.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd perfect-article-generator
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the project directory and add your OpenAI API key:

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

1. **Run the application:**

    ```bash
    streamlit run main.py
    ```

2. **Access the application:**

    Open your web browser and go to `http://localhost:8501`.

3. **Provide OpenAI API Key:**

    Enter your OpenAI API key in the provided text input.

4. **Upload PDF File:**

    - Upload a PDF file containing the text for article generation.

5. **Enter Primary Keyword:**

    - Enter the primary keyword around which the article will be focused.

6. **Define Article Structure:**

    - Enter the headings for the article structure separated by commas.

7. **Specify Article Length:**

    - Choose the desired length of the generated article.

8. **Generate Article:**

    - Click on the "Generate Article" button to start the article generation process.

9. **View Generated Article:**

    - Once the generation is complete, view the generated article in the text area.

## License

This project is licensed under the [MIT License](LICENSE).
