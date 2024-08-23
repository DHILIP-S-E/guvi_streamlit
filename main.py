import streamlit as st
import requests
import re
import json
import os
import time
import base64
from io import BytesIO

apiKey = "ee7a4bbf-c19c-4900-8025-7014e28daac5"

# Function to encode image to base64
def get_base64_image(image_file):
    with open(image_file, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Function to generate UI code from API
def apiFunction(usersInputObj):
    inputsArray = [{"id": "{input_1}", "label": "Enter requirements", "type": "text"}]
    prompt = "Generate a user interface in Streamlit based on the requirements {input_1} and the provided code "
    filesData, textData = {}, {}
    
    for inputObj in inputsArray:
        inputId = inputObj['id']
        if inputObj['type'] == 'text':
            prompt = prompt.replace(inputId, usersInputObj.get(inputId, ''))
        elif inputObj['type'] == 'file':
            path = usersInputObj[inputId]
            try:
                file_name = os.path.basename(path)
                with open(path, 'rb') as f:
                    filesData[inputId] = f.read()
            except FileNotFoundError:
                st.error(f"File not found: {path}")
                return None

    textData['details'] = json.dumps({
        'appname': 'streamlit ui generator',
        'prompt': prompt,
        'documentId': 'no-embd-type',
        'appId': '66c8a3b164d827b744a2a0f4',
        'memoryId': '',
        'apiKey': apiKey
    })

    response = requests.post('https://apiappstore.guvi.ai/api/output', data=textData, files=filesData)
    
    if response.status_code == 200:
        output = response.json()
        return output['output']
    else:
        st.error("Failed to get a response from the API.")
        return None

# Function to download generated code
def download_code(code, filename="generated_ui.py"):
    b64 = base64.b64encode(code.encode()).decode()  # Encode the code to base64
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download .py file</a>'
    st.markdown(href, unsafe_allow_html=True)

# Get base64 of the background image
img_base64 = get_base64_image("images/back.png")

# Streamlit App
st.title("Streamlit UI Generator")

# Text Input
requirements = st.text_area("Enter your requirements (Markdown supported):")

# History of Generated UIs
st.sidebar.title("Generated UIs")
generated_ui_history = st.sidebar.text_area("Generated UIs", height=200)

# Loading Spinner
with st.spinner('Generating UI...'):
    # Button to Generate UI
    if st.button("Generate UI"):
        if requirements:
            usersInputObj = {'{input_1}': requirements}
            output = apiFunction(usersInputObj)

            if output:
                # Replace local URLs with production URLs
                url_regex = r'http://localhost:7000/'
                replaced_string = re.sub(url_regex, 'https://apiappstore.guvi.ai/', output)
                
                # Display the output
                st.code(replaced_string, language='python')
                
                # Add to history
                generated_ui_history += f"\n\n---\n\n{replaced_string}"
                st.sidebar.text_area("Generated UIs", generated_ui_history, height=200)
                
                # Allow downloading the code
                download_code(replaced_string)
            else:
                st.warning("No output generated. Please check your requirements and try again.")
        else:
            st.warning("Please enter your requirements before generating the UI.")
    time.sleep(1)

# Adding custom CSS with animation effects and white paragraph text
st.markdown(
    f"""
    <style>
    /* General App Styling */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    .stApp {{
        background: linear-gradient(to bottom, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9)),
                    url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        font-family: 'Roboto', sans-serif;
        color: #ffffff;  /* White text color for all elements */
    }}
    
    /* Title Styling */
    h1 {{
        color: #ffffff !important; 
        text-align: center;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-out;
    }}
    
    /* Input Box Styling */
    .stTextArea > div > div > textarea {{
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff;  /* White text color for input */
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 8px;
        padding: 10px;
        font-size: 1rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }}

    .stTextArea > div > div > textarea:focus {{
        border-color: #ffffff;
        box-shadow: 0 0 5px rgba(255, 255, 255, 0.7);
    }}
    
    /* Button Styling */
    .stButton > button {{
        background: linear-gradient(135deg, #f79533, #f37055, #ef4e7b, #a166ab, #5073b8, #1098ad, #07b39b, #6fba82);
        color: #ffffff;  /* White text color for button */
        border: none;
        padding: 10px 20px;
        border-radius: 50px;
        font-size: 1rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        animation: buttonPulse 1s infinite;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
    }}
    
    .stButton > button:active {{
        transform: translateY(1px);
    }}

    /* Card-Like Container Styling */
    .stTextArea, .stButton {{
        margin: 0 auto;
        max-width: 600px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-out;
    }}
    
    /* Code Block Styling */
    .stCodeBlock {{
        background-color: rgba(0, 0, 0, 0.8);
        color: #ffffff;  /* White text color for code block */
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 15px;
        border-radius: 8px;
        font-size: 1rem;
        animation: fadeIn 1s ease-out;
    }}

    /* Paragraph Styling */
    p {{
        color: #ffffff;  /* White text color for paragraphs */
        animation: fadeIn 1s ease-out;
    }}
    
    /* Animation Keyframes */
    @keyframes fadeIn {{
        from {{
            opacity: 0;
        }}
        to {{
            opacity: 1;
        }}
    }}

    @keyframes buttonPulse {{
        0% {{
            transform: scale(1);
        }}
        50% {{
            transform: scale(1.05);
        }}
        100% {{
            transform: scale(1);
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)
