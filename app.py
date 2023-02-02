
# Import from standard library
import logging
import random
import re

# Import from 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components

# Import modules
import oai

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


# Define functions
def generate_text(item: str, issue: str, given_prompt: str = None):
    """Generate text."""
    if st.session_state.n_requests >= 5:
        st.session_state.text_error = "Too many requests. Please wait a few seconds before generating another text."
        logging.info(f"Session request limit reached: {st.session_state.n_requests}")
        st.session_state.n_requests = 1
        return

    st.session_state.text = ""
    st.session_state.text_error = ""

    if not item:
        st.session_state.text_error = "Please enter a topic"
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while your text is being generated..."):
           
            prompt = given_prompt if given_prompt else f"Write a user complaint about a {item} that caused {issue}"
            print(prompt)
            openai = oai.Openai()
            
            st.session_state.text_error = ""
            st.session_state.n_requests += 1
            st.session_state.text = (
                openai.complete(prompt).strip().replace('"', "")
            )
            logging.info(
                f"Topic: {item}, {issue}\n"
                f"Text: {st.session_state.text}"
            )


# Configure Streamlit page and state
st.set_page_config(page_title="Complaint Generation", page_icon="🤖")

if "text" not in st.session_state:
    st.session_state.text = ""
if "text_error" not in st.session_state:
    st.session_state.text_error = ""
if "image_error" not in st.session_state:
    st.session_state.image_error = ""
if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0

# Force responsive layout for columns also on mobile
st.write(
    """<style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>""",
    unsafe_allow_html=True,
)

# Render Streamlit page
st.title("Generate Complains")
st.markdown(
    "This mini-app generates user complaints using OpenAI's GPT-3 based [Davinci model](https://beta.openai.com/docs/models/overview) for texts."
)

item = st.text_input(label="Product (shirt, shoes, jacket, ...)", placeholder="Shoes")
issue = st.text_input(
    label="Safety or Quality Issue (strangulation, broken ankle, suffocation, .. )",
    placeholder="broken ankle",
)
prompt = st.text_input(
    label="You can also write the prompt yourself (optional)",
    placeholder="Generate a user complaint about a sweater that caused an allergic reaction",
)

st.button(
    label="Generate text",
    type="secondary",
    on_click=generate_text,
    args=(item, issue, prompt),
)

text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.text:
    st.markdown("""---""")
    st.text_area(label="Text", value=st.session_state.text, height=150)
