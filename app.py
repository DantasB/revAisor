import streamlit as st

def main():
    st.title("Página Inicial")
    input_text = st.text_area("Digite o texto aqui:")
    if st.button("Enviar"):
        st.session_state['text'] = input_text
        st.experimental_rerun()

def second_page():
    text = st.session_state.get('text', "")
    st.title("Segunda Página")
    st.write(f"Texto enviado: {text}")

if __name__ == "__main__":
    if 'text' in st.session_state:
        second_page()
    else:
        main()
