import streamlit as st
from gpt.interface import GPTInterface

# Configuração de página
st.set_page_config(page_title="revAIsor - Revisão de Artigos Científicos", layout="wide")

# Estilo da página
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

# Página inicial - Boas vindas
def main():
    st.title("Bem-vindo ao revAIsor!")
    st.markdown(
        """
        O revAIsor é uma inteligência artificial projetada para auxiliar você na revisão de artigos científicos
        antes de submetê-los a conferências e periódicos. Basta inserir o texto do seu artigo na caixa de texto
        abaixo e o revAIsor irá gerar sugestões e melhorias para o seu conteúdo. Experimente agora mesmo!
        """
    )
    input_text = st.text_area("Insira o texto do seu artigo aqui:")
    if st.button("Revisar"):
        # Define o valor do texto na session_state e redireciona para a segunda página
        st.session_state["text"] = input_text
        st.experimental_rerun()

# Segunda página - Sugestões do revAIsor
def second_page():
    prompt = st.session_state.get("text", "")
    st.title("Sugestões do revAIsor")
    st.write("Texto revisado:")
    st.write(prompt)

    # Chame o modelo ChatGPT e obtenha a resposta
    if prompt:
        st.write("Resposta do revAIsor:")
        st.write(GPTInterface(prompt).response)

    # Opção para submeter outro texto
    if st.button("Submeter outro texto"):
        st.session_state.pop("text")
        st.experimental_rerun()

if __name__ == "__main__":
    # Verifica se a segunda página foi acessada com parâmetros
    if "text" in st.session_state:
        second_page()
    else:
        main()
