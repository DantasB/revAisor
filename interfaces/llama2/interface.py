import os
import requests
from interfaces.base import BaseInterface


class LLAMA2Interface(BaseInterface):
    def __init__(self, prompt, max_tokens=40000, temperature=0.5):
        self.ngrok_url = os.getenv("LLAMA2_API_URL")

        self.evaluations = [
            {
                "title": "Grammar",
                "description": "Grammar suggestions for your text.",
                "method": self.evaluate_prompt_grammar
            },
            {
                "title": "Theme",
                "description": "Theme suggestions for your text.",
                "method": self.evaluate_prompt_by_theme
            }
        ]

        super().__init__(prompt=prompt, model=None, evaluations=self.evaluations, max_tokens=max_tokens, temperature=temperature)

    def validate_initialization(self):
        if not requests.get(self.ngrok_url).ok:
            raise ValueError("Ngrok is not running. Please, run it and try again.")

    def evaluate_prompt_by_theme(self):
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

            ---
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
            ---

            Now whats your output to my input:
            [user input]: {self.prompt}
        """

        return requests.post(
            self.ngrok_url + "/generate",
            json={
                "inputs": input,
                "parameters": {
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "top_p": 0.5,
                    "frequency_penalty": 0,
                    "presence_penalty": 0
                }
            }
        ).json()
    
    def evaluate_prompt_grammar(self):
        input = f"""
            [Context]: You are a scientific article revisor and one of the steps is the grammar suggestion tool, giving which word or sentence should I change. Besides, check if the document follows the DoCO, the Document Components Ontology that provides a structured vocabulary written in OWL 2 DL of document components, both structural (e.g. block, inline, paragraph, section, chapter) and rhetorical (e.g. introduction, discussion, acknowledgements, reference list, figure, appendix), enabling these components, and documents composed of them, to be described in RDF.
            --- 
            Example 1:
            [example input]: IoT software systems have made great strides since the new industrial revolution known as Industry 4.0. Its usage has been growing over the years, and research reports indicate the occurrence of exponential growth related to the utilization of these devices, with a forecast of surpassing 30 billion devices by 2024.
            [your output]: 2 additional writing issues. 1 Unclear sentences. 1 Passive voice misuse. 
            - You should remove "known as" in the sentence: "[...] revolution, known as Industry 4.0. [...]"
            - You should remove "in which it was" in the sentence: "[...] systems in which it was applied and the approach [...]"
            ---
            Example 2:
            [example input]: The simulation itself is a snippet code that will run the simulation following the number of data that we want to simulate. In our case we ran triplicates scenarios that would, in each of them, send 80 messages to the broker and consume 80 messages from the broker, evaluating the time of them. We ran the experiment in three scenarios because we wanted to observe the standard deviation and the average.
            [your output]: 1 suggestion. Conciseness.
            - You should replace "run the simulation following" in the sentence: "[...] that will run the simulation following the number [...]" with "simulate". This will bring a non-wordy sentence.
            ---
            Now whats your output to my input:
            [user input]: {self.prompt}
        """
        return requests.post(
            self.ngrok_url + "/generate",
            json={
                "inputs": input,
                "parameters": {
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "top_p": 0.5,
                    "frequency_penalty": 0,
                    "presence_penalty": 0
                }
            }
        ).json()
