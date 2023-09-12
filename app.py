from random import shuffle
from typing import List

import streamlit as st

from interfaces import AVAILABLE_MODELS

st.set_page_config(page_title="revAIsor - Scientific Article Review", layout="wide")


@st.cache_resource
def randomized_models() -> List[str]:
    models = list(AVAILABLE_MODELS.keys())
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

    abstract_text = st.text_area("Insert your abstract text here:")
    introduction_text = st.text_area("Insert your introduction text here:")
    conclusion_text = st.text_area("Insert your conclusion text here:")

    if st.button("Review"):
        if not (abstract_text and introduction_text and conclusion_text):
            st.error("Please fill in all three fields: Abstract, Introduction, and Conclusion.")
        else:
            st.session_state["context"] = context_text
            st.session_state["abstract"] = abstract_text
            st.session_state["introduction"] = introduction_text
            st.session_state["conclusion"] = conclusion_text
            st.session_state["model"] = selected_model
            st.experimental_rerun()


def second_page() -> None:
    abstract = st.session_state.get("abstract", "")
    introduction = st.session_state.get("introduction", "")
    conclusion = st.session_state.get("conclusion", "")
    selected_model = st.session_state.get("model", "")
    context = st.session_state.get("context", "")
    st.title("revAIsor Suggestions")

    model = AVAILABLE_MODELS[selected_model]
    if not model:
        st.error("Invalid model selected. Please, try again.")
        st.stop()

    if abstract and introduction and conclusion:
        # Use the selected model to evaluate prompts
        prompts = {
            "abstract": abstract,
            "introduction": introduction,
            "conclusion": conclusion,
        }

        # Get suggestions from the model
        suggestions = model(context, prompts).response

        st.write("revAIsor Response:")
        st.write(suggestions)

    if st.button("Submit another text"):
        st.session_state.pop("abstract")
        st.session_state.pop("introduction")
        st.session_state.pop("conclusion")
        st.session_state.pop("model")
        st.session_state.pop("context")
        st.experimental_rerun()


if __name__ == "__main__":
    if all(
        parameter in st.session_state
        for parameter in ["abstract", "introduction", "conclusion", "context", "model"]
    ):
        second_page()
    else:
        main()
