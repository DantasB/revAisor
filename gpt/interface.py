import openai
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GPTInterface:
    __API_KEY = os.getenv("OPENAI_API_KEY")

    def __validate_key(self):
        if not self.__API_KEY:
            raise ValueError("API KEY is not defined. Please, refer to the README.md file.")

    def __init__(self, prompt, model="gpt-3.5-turbo-16k", max_tokens=10000):
        self.__validate_key()

        self.prompt = prompt
        self.model = model
        self.max_tokens = max_tokens
        self.response = self.__get_response()
        
    def __get_response(self):
        grammar_response = self.__evaluate_prompt_grammar()
        theme_response = self.__evaluate_prompt_by_theme()

        return {
            "grammar": grammar_response,
            "theme": theme_response
        }

    def __evaluate_prompt_by_theme(self):
        openai.api_key = self.__API_KEY

        return openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a scientific article revisor and you are specialist in every theme that is written in the text.\n\nJudge with knowledge suggesting the author in which topics he would enfasize better and what should he rewrite to bring better readability of the theme.\n\nThe categories of suggestions are:\n- Improve References;\n- Theme Violation;\n- Missing Related Works if exists;\n- Missing informations;\n- Confusing Explanation;\n- Missing Limitations;\n- Others.\n\nWhere the Others you can generate other categories.\n\nAlso use clear language when you are suggesting to be clear in which parts of the text the author should make the changes.\n\nList as many suggestions as you can. Besides, check if the document followes the DoCO, the Document Components Ontology that provides a structured vocabulary written in OWL 2 DL of document components, both structural (e.g. block, inline, paragraph, section, chapter) and rhetorical (e.g. introduction, discussion, acknowledgements, reference list, figure, appendix), enabling these components, and documents composed of them, to be described in RDF."
                },
                {
                    "role": "user",
                    "content": "A ideação e construção do CryptoComponent envolveu a elicitação de requisitos para seu\nfuncionamento. Considerando a natureza restritiva dos dispositivos IoT, foi necessário\nidentificar os tipos de algoritmos de criptografia passíveis de serem aplicados para mitigar\no problema de segurança durante o tráfego de dados no sistema. Nesse contexto, dentre\ndiferentes algoritmos de criptografia, tais como o Elephant [Beyne et al. 2020], Pyjamask\n[Goudarzi et al. 2020], SPARKLE [Beierle et al. 2020] e SPECK [Beaulieu et al. 2015].\nDentre os algoritmos de criptografia leve identificados na literatura técnica, foi escolhido\no SPECK, tendo em vista ter sido criado para ser utilizado em dispositivos de baixo poder\ncomputacional, como por exemplo rede de sensores, incluindo dispositivos IoT [Beaulieu\net al. 2015]. Sua escolha foi também influenciada pela simplicidade de utilização, na qual\né necessário fornecer apenas uma chave única e uma mensagem de tamanho arbitrário\npara que o algoritmo produza uma mensagem encriptada. Neste sentido, não é necessário\nqualquer tipo de autenticação. Além disso, o SPECK é de simples implementação,\napresenta segurança avaliada e, por ser uma criptografia de bloco, apresenta baixo\nconsumo de recurso computacional [Beaulieu et al. 2015]. Adicionalmente, para fins de\navaliação do componente, foi implementado o algoritmo de XOR, escolhido por ser uma\ndas etapas para construção do algoritmo SPECK.\nEm seguida, os requisitos funcionais e não funcionais do CryptoComponent foram \nespecificados. Dentre estes, destacam-se a capacidade do componente de encriptar o dado\npassado como parâmetro imediatamente antes de ser enviado pela rede, garantindo assim\nque o dado trafegue de forma encriptada até seu recebimento na outra ponta e a\ncapacidade do componente de decriptar o dado antes de ser consumido. Essa característica\nconfigura uma Criptografia E2E (End to End). A Tabela 1 mostra um extrato dos\nrequisitos funcionais e não funcionais especificados para criação do CryptoComponent.\nA lista completa dos requisitos do CryptoComponent pode ser acessada em\nbit.ly/cryptocomponentlistofrequirements.\nApós a definição dos requisitos, as escolhas para a implementação do projeto\nforam dadas visando garantir maior reutilização de código. Além disso, algumas decisões\ndo projeto variaram entre a otimização do uso de recursos computacionais, tendo em vista\na natureza do dispositivo e a facilidade da utilização por parte dos desenvolvedores,\nprivilegiando a ampla utilização do componente. Sendo assim, por ser um componente\npara ser utilizado em dispositivos IoT, o CryptoComponent foi codificado na linguagem\nde programação C++. O diagrama de componentes apresentado na Figura 1 ilustra sua\nestrutura.\nO componente pode ser utilizado em um dispositivo IoT por meio da instanciação\nde um objeto da classe CryptoComponent informando o algoritmo de interesse (XOR ou\nSPECK) e informando se a demanda é por Encriptar ou Decriptar a mensagem\nconsiderando uma Chave específica.\nO CryptoComponent possibilita sua utilização pelos sistemas de software por \nmeio de uma API (Application Programming Interface) que oferece acesso para as\nfacilidades de encriptar e decriptar a informação independente da linguagem de\nprogramação. Neste caso, a comunicação entre os dispositivos IoT e o sistema de software\ndeve ser realizada por meio de um broker, com protocolo MQTT, conforme apresentado\nna Figura 2.\n\nA disponibilidade da API do CryptoComponent garante a possibilidade da\nencriptação/decriptação dos dados em todo o fluxo de recepção e envio da mensagem. O\nenvio dos dados ao broker é feito por meio de rede pública utilizando o protocolo MQTT,\nlogo, a utilização do componente nos dispositivos IoT garante a segurança do envio da\nmensagem. Da mesma forma, a segurança dos dados consumidos do broker é garantida\nporque as aplicações que estão consumindo esses dados, em nosso caso, são executadas\nem K3S, um kubernetes de baixo custo, que garante que cada uma delas utilize uma rede\nprivada, fazendo com que seu tráfego de rede não seja visto externamente.\nDesta forma, pode-se dizer que os dados são transmitidos de forma segura e\nencriptada em cada um dos momentos da arquitetura apresentada na Figura 2. É\nimportante ressaltar que a construção da API representa uma alternativa para garantir que\no componente seja utilizado nos sistemas desenvolvidos pelo Laboratório de Engenharia\nde Software, não sendo necessário que outro usuário, por exemplo, tenha que utilizar o\nsistema K3S ou mesmo hospedar o serviço da API dentro de uma rede privada."
                },
                {
                    "role": "assistant",
                    "content": "The article is well written, clear and easy to understand. \n\nBut there still a few things to improve like:\n\nImprove References:\n- For instance, what is an MQTT protocol (with references)? Missing details about K3S (with references) for replication purposes. Unclear importance of API in relation to encryption/decryption already on IoT device. Clarify the role of Engineering Software Lab and systems needing the API. More explanation needed to avoid doubts.\n\nTheme Violation:\n- Authors lack cryptography experience and potentially implement insecure algorithms.\n- Critical issues with the created component, such as allowing insecure algorithms.\n- Usage of repeating-key XOR algorithm raises concerns about security.\n- Lack of discussion on secure mode of operation for Speck cipher.\n\nMissing Informations:\n- Missing explanation of XOR and SPECK algorithms.\n\nConfusing Explanation:\n-Confusing explanation of the API's importance and the Engineering Software Lab's role."
                },
                {
                    "role": "user",
                    "content": self.prompt
                }
            ],
            temperature=0.5,
            max_tokens=10000,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0
        )["choices"][0]["message"]["content"]

    def __evaluate_prompt_grammar(self):
        openai.api_key = self.__API_KEY

        return openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a scientific article revisor and one of the steps is the grammar suggestion tool, giving which word or sentence should i change. \n\nThe suggestions should be related to Correctness like Grammar and spelling. Consistency in spelling and and English fluency.\n\nAlso in Clarity like Conciseness, Full-sentence rewrites and Formatting.\n\nAlso in Engagement like Word choice and Word and sentence variety.\n\nAlso in Delivery, these texts shouls have a formal writing.\n\nYou also should avoid suggestions that are already in the text. It's not necessary to suggest things that are already beeing made.\n\nTry to give at least two suggestions."
                },
                {
                    "role": "user",
                    "content": "IoT software systems have made great strides since the new industrial revolution known as Industry 4.0. Its usage has been growing over the years, and research reports indicate the occurrence of exponential growth related to the utilization of these devices, with a forecast of surpassing 30 billion devices by 2024.\n\nAs a result, organizations that frequently list the most common security risks enumerate that, in IoT software devices, secure data transfer and storage of information are among the top 10 most recurrent problems in these devices.\n\nThus, this project presents a cryptographic component designed to allow the data transferred, in low-power computing devices, to be transmitted securely, preventing data leaks. This work describes the details of the developed component, such as the hardware systems in which it was applied and the approach used for implementation."
                },
                {
                    "role": "assistant",
                    "content": "2 additional writing issues. 1 Unclear sentences. 1 Passive voice misuse. \n- You should remove \"known as\" in the sentence: \"[...] revolution, known as Industry 4.0. [...]\"\n- You should remove \"in which it was\" in the sentence: \"[...] systems in which it was applied and the approach [...]\""
                },
                {
                    "role": "user",
                    "content": "The simulation itself is a snippet code that will run the simulation following the number of data that we want to simulate. In our case we ran triplicates scenarios that would, in each of them, send 80 messages to the broker and consume 80 messages from the broker, evaluating the time of them. We ran the experiment in three scenarios because we wanted to observe the standard deviation and the average."
                },
                {
                    "role": "assistant",
                    "content": "1 suggestion. Conciseness.\n- You should replace \"run the simulation following\" in the sentence: \"[...] that will run the simulation following the number [...]\" with \"simulate\". This will bring a non wordy sentence."
                },
                {
                    "role": "user",
                    "content": "We have to encrypted data"
                },
                {
                    "role": "assistant",
                    "content": "1 possible fixes. Grammar.\n- You should replace \"encrypted\" in the sentence: \"We have to encrypted data\" with \"encrypt\". That would correct the verb form."
                },
                {
                    "role": "user",
                    "content": self.prompt
                }
            ],
            temperature=0,
            max_tokens=10000,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0
        )["choices"][0]["message"]["content"]

class LLAMA2Interface:

    __NGROK_URL = os.getenv("LLAMA2_API_URL")

    def __init__(self, prompt, temperature=0.5, max_tokens=10000):
        self.ngrok_url = self.__NGROK_URL
        self.__verify_if_ngrok_is_running()

        self.prompt = prompt
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.response = self.__get_response()

    def __verify_if_ngrok_is_running(self):
        if not requests.get(self.ngrok_url).ok:
            raise ValueError("Ngrok is not running. Please, run it and try again.")

    def __get_response(self):
        return {
            "grammar": self.__evaluate_prompt_grammar(),
            "theme": self.__evaluate_prompt_by_theme()
        }

    def __evaluate_prompt_by_theme(self):
        input = f"""
            [Context]: You are a scientific article revisor and you are a specialist in every theme that is written in the text.
            Judge with knowledge suggesting the author in which topics he would emphasize better and what should he rewrite to bring better readability of the theme.
            The categories of suggestions are:
            - Improve References;
            - Theme Violation;
            - Missing Related Works if exists;
            - Missing information;
            - Confusing Explanation;
            - Missing Limitations;
            - Others.
            Where the Others you can generate other categories.
            Also use clear language when you are suggesting to be clear in which parts of the text the author should make the changes.
            List as many suggestions as you can.

            Example 1:
            [example input]: A ideação e construção do CryptoComponent envolveu a elicitação de requisitos para seu funcionamento. Considerando a natureza restritiva dos dispositivos IoT, foi necessário identificar os tipos de algoritmos de criptografia passíveis de serem aplicados para mitigar o problema de segurança durante o tráfego de dados no sistema. Nesse contexto, dentre diferentes algoritmos de criptografia, tais como o Elephant [Beyne et al. 2020], Pyjamask [Goudarzi et al. 2020], SPARKLE [Beierle et al. 2020] e SPECK [Beaulieu et al. 2015]. Dentre os algoritmos de criptografia leve identificados na literatura técnica, foi escolhido o SPECK, tendo em vista ter sido criado para ser utilizado em dispositivos de baixo poder computacional, como por exemplo rede de sensores, incluindo dispositivos IoT [Beaulieu et al. 2015]. Sua escolha foi também influenciada pela simplicidade de utilização, na qual é necessário fornecer apenas uma chave única e uma mensagem de tamanho arbitrário para que o algoritmo produza uma mensagem encriptada. Neste sentido, não é necessário qualquer tipo de autenticação. Além disso, o SPECK é de simples implementação, apresenta segurança avaliada e, por ser uma criptografia de bloco, apresenta baixo consumo de recurso computacional [Beaulieu et al. 2015]. Adicionalmente, para fins de avaliação do componente, foi implementado o algoritmo de XOR, escolhido por ser uma das etapas para construção do algoritmo SPECK. Em seguida, os requisitos funcionais e não funcionais do CryptoComponent foram especificados. Dentre estes, destacam-se a capacidade do componente de encriptar o dado passado como parâmetro imediatamente antes de ser enviado pela rede, garantindo assim que o dado trafegue de forma encriptada até seu recebimento na outra ponta e a capacidade do componente de decriptar o dado antes de ser consumido. Essa característica configura uma Criptografia E2E (End to End). A Tabela 1 mostra um extrato dos requisitos funcionais e não funcionais especificados para criação do CryptoComponent. A lista completa dos requisitos do CryptoComponent pode ser acessada em bit.ly/cryptocomponentlistofrequirements. Após a definição dos requisitos, as escolhas para a implementação do projeto foram dadas visando garantir maior reutilização de código. Além disso, algumas decisões do projeto variaram entre a otimização do uso de recursos computacionais, tendo em vista a natureza do dispositivo e a facilidade da utilização por parte dos desenvolvedores, privilegiando a ampla utilização do componente. Sendo assim, por ser um componente para ser utilizado em dispositivos IoT, o CryptoComponent foi codificado na linguagem de programação C++.
            [your output]: The article is well written, clear, and easy to understand. But there are still a few things to improve like:
            Theme Violation:
            - Authors lack cryptography experience and potentially implement insecure algorithms.
            - Critical issues with the created component, such as allowing insecure algorithms.
            - Usage of repeating-key XOR algorithm raises concerns about security.
            - Lack of discussion on the secure mode of operation for the Speck cipher.
            Missing Information:
            - Missing explanation of XOR and SPECK algorithms.
            Confusing Explanation:
            - Confusing explanation of the API's importance and the Engineering Software Lab's role.

            Now whats your output to my input:
            [user input]: {self.prompt}
        """

        return requests.post(
            self.ngrok_url + "/generate",
            json={
                "inputs": input,
                "parameters": {
                    "temperature": self.temperature,
                    "max_tokens": 40000,
                    "top_p": 0.5,
                    "frequency_penalty": 0,
                    "presence_penalty": 0
                }
            }
        ).json()
    
    def __evaluate_prompt_grammar(self):
        input = f"""
            [Context]: You are a scientific article revisor and one of the steps is the grammar suggestion tool, giving which word or sentence should I change. Besides, check if the document follows the DoCO, the Document Components Ontology that provides a structured vocabulary written in OWL 2 DL of document components, both structural (e.g. block, inline, paragraph, section, chapter) and rhetorical (e.g. introduction, discussion, acknowledgements, reference list, figure, appendix), enabling these components, and documents composed of them, to be described in RDF.

            Example 1:
            [example input]: IoT software systems have made great strides since the new industrial revolution known as Industry 4.0. Its usage has been growing over the years, and research reports indicate the occurrence of exponential growth related to the utilization of these devices, with a forecast of surpassing 30 billion devices by 2024.
            [your output]: 2 additional writing issues. 1 Unclear sentences. 1 Passive voice misuse. 
            - You should remove "known as" in the sentence: "[...] revolution, known as Industry 4.0. [...]"
            - You should remove "in which it was" in the sentence: "[...] systems in which it was applied and the approach [...]"

            Example 2:
            [example input]: The simulation itself is a snippet code that will run the simulation following the number of data that we want to simulate. In our case we ran triplicates scenarios that would, in each of them, send 80 messages to the broker and consume 80 messages from the broker, evaluating the time of them. We ran the experiment in three scenarios because we wanted to observe the standard deviation and the average.
            [your output]: 1 suggestion. Conciseness.
            - You should replace "run the simulation following" in the sentence: "[...] that will run the simulation following the number [...]" with "simulate". This will bring a non-wordy sentence.

            Now whats your output to my input:
            [user input]: {self.prompt}
        """

        return requests.post(
            self.ngrok_url + "/generate",
            json={
                "inputs": input,
                "parameters": {
                    "temperature": self.temperature,
                    "max_tokens": 40000,
                    "top_p": 0.5,
                    "frequency_penalty": 0,
                    "presence_penalty": 0
                }
            }
        ).json()