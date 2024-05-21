import google.generativeai as genai
import streamlit as st


# Function to configure sidebar to verify and get the model  api key
def configure_apikey_sidebar():
    api_key = st.sidebar.text_input(f'Enter your Gemini model API Key', type='password',
                                    help='Get API Key from: https://aistudio.google.com/app/apikey')
    if api_key == '':
        st.sidebar.warning('Enter the API key')
        file_uploader = False
    elif api_key.startswith('AI') and (len(api_key) == 39):
        st.sidebar.success('Proceed to uploading the image!', icon='️👉')
        file_uploader = True
    else:
        st.sidebar.warning('Please enter the correct credentials!', icon='⚠️')
        file_uploader = False

    return api_key, file_uploader


# Function to load Gemini Pro model
def get_gemini_response(api_key, prompt, u_image):
    image_data = input_image_details(u_image)
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    model_response = model.generate_content([prompt, image_data[0]])
    return model_response.text


# Function to extract details from the uploaded image which is compatible with the model format
def input_image_details(uploaded_file):
    if uploaded_file is not None:

        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": 'image/png',
                "data": bytes_data
            }
        ]
        return image_parts

    else:
        exit(1)
