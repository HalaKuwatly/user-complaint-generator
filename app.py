
# Import from standard library
import logging
import random

# Import from 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
# Import modules
import oai
from time import sleep
# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


recently_purchased_replacements = ["", "recently purchased","recently bought", "bought", 
"purchased", "orderded", "recently ordered", "just bought", 
"just recieved", "have recieved", "got", "just got", "made an order of", 
]

openai = oai.Openai()
            
# Define functions
def generate_text(persons:list, items: str, issue: str):
    """Generate text."""

    st.session_state.texts = []
    st.session_state.text_error = ""
    st.session_state.n_requests = 0

    items=items.split(",")
    items = [i.strip() for i in items]
    with text_spinner_placeholder:
        with st.spinner("Please wait while your texts are being generated..."):
            for item in items:
                if st.session_state.n_requests > 5:
                    st.session_state.n_requests = 0
                    sleep(2)
                person = random.choice(persons)
                if person == "User":
                    prompt = f"Write a user complaint about {item} that caused {issue}"
                else:
                    prompt = f"Write a user complaint about user's {person}'s {item} that caused {issue}"
                
                st.session_state.text_error = ""
                texts = openai.complete(prompt)
                st.session_state.n_requests+=1
                if texts:
                    for text in texts:
                        text = text.strip().replace('"', "")
                        text = text.replace("recently purchased", random.choice(recently_purchased_replacements))
                        st.session_state.texts.append(text)
                        logging.info(
                            f"Prompt: {prompt}\n"
                            f"Text: {text}"
                        )


# Configure Streamlit page and state
st.set_page_config(page_title="Complaint Generation", page_icon="🤖")

if "texts" not in st.session_state:
    st.session_state.texts = []
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
st.title("Generate Complaints")
st.markdown(
    "This mini-app generates user complaints using OpenAI's GPT-3 based [Davinci model](https://beta.openai.com/docs/models/overview) for texts."
)

persons = st.multiselect("Person", ('User', 'Daughter', 'Son', 'Mother', 'Father', 'Husband', 'Wife', 'Child', 'Baby', 'Newborn') , default="User")
item = st.text_input(label="Products (shirt, shoes, jacket, ...): You can provide multiple", placeholder="Shoes, sandals")
issue = st.text_input(
    label="Safety or Quality Issue (strangulation, broken ankle, suffocation, .. ): Only provide one",
    placeholder="broken ankle",
)

st.button(
    label="Generate texts",
    type="primary",
    on_click=generate_text,
    args=(persons, item, issue),
)

text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.texts:
    print(len(st.session_state.texts))
    df = pd.DataFrame({"texts": st.session_state.texts})
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    st.table(df)

