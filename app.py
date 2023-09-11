from random import shuffle
from typing import List

import streamlit as st

from interfaces import AVAILABLE_MODELS

st.set_page_config(page_title="revAIsor - Scientific Article Review", layout="wide")


@st.cache_resource
def randomized_models() -> List[str]:
    models = ["Modelo 2", "Modelo 1"]
    shuffle(models)
    return models


st.markdown(
    """
    <style>
    .main-container {
        background-color: #f9f9f9;
        padding: 2rem;
    }
    .stButton>button {
        background-color: #2a70c7;
        color: #ffffff;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #296cad;
    }
    .stTextArea textarea {
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def main() -> None:
    st.title("Welcome to revAIsor!")
    st.markdown(
        """
        revAIsor is an AI designed to assist you in reviewing scientific articles before 
        submitting them to conferences and journals. Just paste your article text in the text 
        box below, and revAIsor will generate suggestions and improvements for your content. 
        Give it a try!
        """
    )

    selected_model = st.radio("Select a model", randomized_models())

    context_text = st.text_area(
        "Explain what is the objective of your article and what is the context of your work:"
    )

    input_text = st.text_area("Insert your article text here:")
    if st.button("Review"):
        st.session_state["context"] = context_text
        st.session_state["text"] = input_text
        st.session_state["model"] = selected_model
        st.experimental_rerun()


def second_page() -> None:
    prompt = st.session_state.get("text", "")
    selected_model = st.session_state.get("model", "")
    context = st.session_state.get("context", "")
    st.title("revAIsor Suggestions")
    st.write("Revised text:")
    st.write(prompt)

    model = AVAILABLE_MODELS[selected_model]
    if not model:
        st.error("Invalid model selected. Please, try again.")
        st.stop()

    if prompt:
        st.write("revAIsor Response:")
        st.write(model(context, prompt).response)

    if st.button("Submit another text"):
        st.session_state.pop("text")
        st.session_state.pop("model")
        st.session_state.pop("context")
        st.experimental_rerun()


if __name__ == "__main__":
    if all(parameter in st.session_state for parameter in ["text", "context", "model"]):
        second_page()
    else:
        main()
