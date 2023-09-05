import streamlit as st
from interfaces.gpt.interface import GPTInterface
from interfaces.llama2.interface import LLAMA2Interface

st.set_page_config(page_title="revAIsor - Scientific Article Review", layout="wide")

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


def main():
    st.title("Welcome to revAIsor!")
    st.markdown(
        """
        revAIsor is an AI designed to assist you in reviewing scientific articles before 
        submitting them to conferences and journals. Just paste your article text in the text 
        box below, and revAIsor will generate suggestions and improvements for your content. 
        Give it a try!
        """
    )

    selected_model = st.radio("Select a model", ("GPT", "LLAMA2"))

    input_text = st.text_area("Insert your article text here:")
    if st.button("Review"):
        st.session_state["text"] = input_text
        st.session_state["model"] = selected_model
        st.experimental_rerun()


def second_page():
    prompt = st.session_state.get("text", "")
    selected_model = st.session_state.get("model", "")
    st.title("revAIsor Suggestions")
    st.write("Revised text:")
    st.write(prompt)

    if selected_model == "GPT":
        interface = GPTInterface(prompt)
    elif selected_model == "LLAMA2":
        interface = LLAMA2Interface(prompt)
    else:
        st.error("Invalid model selected. Please, try again.")
        st.stop()

    if prompt:
        st.write("revAIsor Response:")
        st.write(interface.response)

    if st.button("Submit another text"):
        st.session_state.pop("text")
        st.session_state.pop("model")
        st.experimental_rerun()


if __name__ == "__main__":
    if "text" in st.session_state:
        second_page()
    else:
        main()
