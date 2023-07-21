# revAIsor

Este é um aplicativo que será o seu revisor de artigos.

## Pré-requisitos

- Python 3.10 ou superior instalado
- poetry (gerenciador de pacotes Python)

### Como executar o aplicativo

1. Clone o repositório para sua máquina local:

```bash
git clone https://github.com/seu_usuario/nome_do_repositorio.git
cd nome_do_repositorio
```

2. Certifique-se de que o Poetry esteja instalado. Caso não esteja, siga o tutorial de [como instalar o poetry](https://python-poetry.org/docs/)

3. Instale as dependências do projeto com o Poetry:

```bash
poetry install
```

4. Inicialize o ambiente virtual do Poetry (se ainda não estiver ativado) com o seguinte comando:

```bash
poetry shell
```

5. Agora que o ambiente virtual está ativo, você pode executar o aplicativo Streamlit normalmente usando o comando `streamlit run`:

```bash
streamlit run app.py
```

6. O aplicativo será iniciado e abrirá automaticamente uma página no navegador.


### Estrutura do projeto

- `app.py`: Este é o arquivo principal do aplicativo que contém o código do projeto
- `README.md`: Este arquivo com instruções sobre como executar o aplicativo.

### Contribuição

Sinta-se à vontade para contribuir com melhorias, correções de bugs ou adição de novos recursos. Basta abrir uma issue ou enviar um pull request.

### Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

### Agradecimentos

Este aplicativo foi desenvolvido com base na biblioteca Streamlit. Agradecimentos à equipe do Streamlit por criar uma ferramenta tão útil e fácil de usar.