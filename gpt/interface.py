import openai
import os
from dotenv import load_dotenv

load_dotenv()

class GPTInterface:
    __API_KEY = os.getenv("OPENAI_API_KEY")

    def __init__(self, prompt, model="gpt-3.5-turbo-16k", max_tokens=10000):
        self.prompt = prompt
        self.model = model
        self.max_tokens = max_tokens
        self.response = self.__get_response()
        
    def __get_response(self):
        response = self.__evaluate_prompt_correctness()
        return response

    def __evaluate_prompt_correctness(self):
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
            temperature=0.5,
            max_tokens=10000,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0
        )["choices"][0]["message"]["content"]