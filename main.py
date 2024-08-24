import streamlit as st
import requests
import re
import json
import os
import base64

apiKey = "ee7a4bbf-c19c-4900-8025-7014e28daac5"

# Function to encode image to base64
def get_base64_image(image_file):
    try:
        with open(image_file, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {image_file}")
        return None

# Function to generate UI code from API
def apiFunction(usersInputObj):
    inputsArray = [{"id": "{input_1}", "label": "Enter requirements", "type": "text"}]
    prompt = "Generate a user interface in Streamlit based on the requirements {input_1} and the provided code "
    filesData, textData = {}, {}
    
    for inputObj in inputsArray:
        inputId = inputObj['id']
        if inputObj['type'] == 'text':
            prompt = prompt.replace(inputId, usersInputObj[inputId])
        elif inputObj['type'] == 'file':
            path = usersInputObj[inputId]
            try:
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

    try:
        response = requests.post('https://apiappstore.guvi.ai/api/output', data=textData, files=filesData)
        response.raise_for_status()
        output = response.json()
        return output['output']
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to get a response from the API: {e}")
        return None

# Function to download generated code
def download_code(code, filename="generated_ui.py"):
    b64 = base64.b64encode(code.encode()).decode()  # Encode the code to base64
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}" class="download-button">Download .py file</a>'
    st.markdown(href, unsafe_allow_html=True)

# Get base64 of the background image
img_base64 = get_base64_image("images/back.png")

# Streamlit App
st.title("Streamlit UI Generator")

# Adding custom CSS with background image, black fade, and white text
if img_base64:
    st.markdown(
        f"""
        <style>
        /* General App Styling */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        .stApp {{
            background: linear-gradient(to bottom, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9)),
                        url("data:image/png;base64,{img_base64}");
            background-size: cover;
            color: #ffffff; /* Default text color */
        }}

        .stTextInput input {{
            color: #ffffff; /* White text color inside input fields */
            background: rgba(0, 0, 0, 0.5); /* Slightly transparent black background for input fields */
            border: 1px solid #ffffff; /* White border */
            border-radius: 5px; /* Rounded corners for input fields */
            padding: 10px; /* Padding inside input fields */
        }}

        .stButton button {{
            background-color: #007bff; /* Button background color */
            color: #ffffff; /* Button text color */
            border: none; /* No border for button */
            border-radius: 5px; /* Rounded corners for button */
            padding: 10px 20px; /* Padding inside button */
            cursor: pointer; /* Pointer cursor on hover */
        }}

        .stButton button:hover {{
            background-color: #0056b3; /* Darker button background color on hover */
        }}

        /* Title, h3, and Label Styling */
        .stApp h1, .stApp h3, .stApp label {{
            color: #ffffff !important; /* White color for titles, h3, and labels */
        }}

        /* Download Button Styling */
        .download-button {{
            display: inline-block;
            background-color: #28a745; /* Green background color */
            color: #ffffff; /* White text color */
            padding: 10px 20px; /* Padding inside button */
            text-decoration: none; /* Remove underline from link */
            border-radius: 5px; /* Rounded corners for button */
            font-weight: bold; /* Bold text */
            transition: background-color 0.3s ease; /* Smooth transition for hover effect */
        }}

        .download-button:hover {{
            background-color: #218838; /* Darker green on hover */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Text Input
requirements = st.text_area("Enter your requirements (Markdown supported):")

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
                
                # Allow downloading the code
                download_code(replaced_string)
            else:
                st.warning("No output generated. Please check your requirements and try again.")
        else:
            st.warning("Please enter your requirements before generating the UI.")

# About the Page
st.markdown("""
---
### About This Page
This tool is designed to help you quickly generate Streamlit UI code based on your requirements. 
You can customize the interface, generate the code, and download it directly as a `.py` file.

For more information or if you encounter any issues, feel free to reach out.
""")
