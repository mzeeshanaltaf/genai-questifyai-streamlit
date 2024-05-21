from PIL import Image
from util import *

# --- PAGE SETUP ---
# Initialize streamlit app
page_title = "Questify AI"
page_icon = ":robot_face:"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")
st.image('logo.jpg', width=400)
st.title(page_title)
st.write(":blue[***Transforming Text into Thought-Provoking Questions***]")
st.write("Upload an image of a text paragraph, select number of questions to be generated and difficulty leve"
         " and then click Generate Questions button. Questify AI will do the rest.")
# ---- SETUP SIDEBAR ----
st.sidebar.title("Configuration")
api_key, file_uploader = configure_apikey_sidebar()

st.header("Upload Image")
uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], disabled=not file_uploader,
                                  label_visibility='collapsed')

st.subheader("Select Difficulty Level:")
difficulty = st.selectbox("Select the difficult level", ('Easy', 'Medium', 'Difficult'),
                          label_visibility="collapsed", disabled=not uploaded_image)
st.subheader("Select the Number of Questions:")
questions = st.slider("Number of Questions", 1, 10, 5, label_visibility="collapsed", disabled=not uploaded_image)

# Input Prompt
input_prompt = f"""
You are a proficient text reader from an image. 
We will upload an image of a text. After extracting text from the image, generate {questions} questions of 
difficulty level: {difficulty}. If image is not consisted of text, respond that there is no text in the image or similar. 
"""

col1, col2 = st.columns(2)

with col2:
    container1 = st.container(height=500, border=True)
    with container1:
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.subheader("Uploaded Image")
            st.image(image, use_column_width='auto')
with col1:
    container2 = st.container(height=500, border=True)

    submit = st.button("Generate Questions", type="primary")

    # if submit:
    if submit:
        with container2:
            st.subheader("Generated Questions:")
            with st.spinner(":blue[Processing...]"):
                response = get_gemini_response(api_key, input_prompt, uploaded_image)
                st.write(response)
