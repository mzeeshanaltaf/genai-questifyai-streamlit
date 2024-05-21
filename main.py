from PIL import Image
from io import BytesIO
from util import *
import json

agriculture_topics = {
    'Agriculture': 'topics/1_Agriculture.jpg',
    'Farming Methods/Organic Farming in Pakistan': 'topics/2_fm_ofp.jpg',
    'Smart Farms': 'topics/3_smart_farms.jpg',
    'Irrigation': 'topics/4_Irrigation.jpg',
    'Arable Farming': 'topics/5_ArableFarming.jpg',
    'Wheat': 'topics/6_wheat.jpg',
}
world_bank_topics = {
    'Role of World Bank/IMF': 'topics/wb_imf_role.jpg',
    'Role of Global Economic Systems': 'topics/global_economic_system.jpg',
    'Importance of Exporting Finished Goods': 'topics/finished_goods.jpg',
}

# --- PAGE SETUP ---
# Initialize streamlit app
page_title = "Questify AI"
page_icon = ":robot_face:"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")
st.image('logo.jpg', width=400)
st.title(page_title)
st.write(":blue[***Transforming Text into Thought-Provoking Questions***]")
st.write("Generate questions (along with answers) related to specific topic. One can select number of questions and "
         "difficulty level")
st.write("Generate Questions button and Questify AI will do the rest.")
# ---- SETUP SIDEBAR ----
st.sidebar.title("Configuration")
api_key, file_uploader = configure_apikey_sidebar()
st.subheader('Select the Chapter')
chapter = st.selectbox("Select the Chapter", ('Agriculture', 'WorldBank/IMF'),
                       label_visibility="collapsed", disabled=not file_uploader)

st.subheader('Select the Topic')
uploaded_image = ''
if chapter == 'Agriculture':
    keys = agriculture_topics.keys()
    topic = st.selectbox("Select the Topic", keys,
                         label_visibility="collapsed", disabled=not file_uploader)
    uploaded_image = agriculture_topics[topic]
elif chapter == 'WorldBank/IMF':
    keys = world_bank_topics.keys()
    topic = st.selectbox("Select the Topic", keys,
                         label_visibility="collapsed", disabled=not file_uploader)
    uploaded_image = world_bank_topics[topic]

image = Image.open(uploaded_image)
byte_arr = BytesIO()
image.save(byte_arr, format='PNG')
# st.header("Upload Image")
# uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], disabled=not file_uploader,
#                                   label_visibility='collapsed')

st.subheader("Select Difficulty Level:")
difficulty = st.selectbox("Select the difficult level", ('Easy', 'Medium', 'Difficult'),
                          label_visibility="collapsed", disabled=not file_uploader)
st.subheader("Select the Number of Questions:")
questions = st.slider("Number of Questions", 1, 10, 5, label_visibility="collapsed", disabled=not file_uploader)

# Input Prompt
input_prompt = f"""
You are a proficient text reader from an image. 
We will upload an image of a text. After extracting text from the image, generate {questions} questions of 
difficulty level: {difficulty}. Besides questions, also generate an answer to those questions. Type answers after all
the questions. You don't need to respond with original text of the image. Your response should include only 
questions and answers.

Your response format should be a list of python dictionary with dictionary keys and values enclosed in double quotes. 
When generating a list, don't start the list with word python.

If image is not consisted of text, respond that there is no text in the image or similar. 
"""

col1, col2 = st.columns(2)

with col2:
    container1 = st.container(height=500, border=True)
    with container1:
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.subheader("Reference Chapter Image")
            if file_uploader:
                st.image(image, use_column_width='auto')
with col1:
    container2 = st.container(height=500, border=True)
    submit = st.button("Generate Questions", type="primary", disabled=not file_uploader)

    # if submit:
    if submit:
        with container2:
            st.subheader("Generated Questions:")
            with st.spinner(":blue[Processing...]"):
                response = get_gemini_response(api_key, input_prompt, byte_arr)
                print(response)
                response_list = json.loads(response)
                for index in range(len(response_list)):
                    expander = st.expander(response_list[index]['question'])
                    expander.write(response_list[index]['answer'])
