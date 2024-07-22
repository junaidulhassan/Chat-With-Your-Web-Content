from langchain_community.llms import HuggingFaceHub
from api_token import LargeLanguageModel
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory import ConversationBufferMemory


class ChatModel: 
    
    
    def __init__(self):
        self.token = LargeLanguageModel()
        self.api_key = self.token.get_Key()
        
        self.memory = ConversationBufferWindowMemory(
            k=3,
            memory_key='chat_history', 
            return_messages=False, 
            human_prefix='Human',
            ai_prefix='Faraz',
            verbose=False
        )
        
        
        huggingfaceHub_rep_id = 'mistralai/Mistral-7B-Instruct-v0.3'
        
        self.llm = HuggingFaceEndpoint(
            name="Web-Pilot",
            repo_id= huggingfaceHub_rep_id,
            task="text-generation",
            huggingfacehub_api_token=self.api_key,
            verbose=False,
            streaming=True,
            temperature=0.9,
            return_full_text=True,
            max_new_tokens=100,
            stop_sequences=['**Human**:','Human:','**Human:**'],
            repetition_penalty=1.1
            )
    
    def PromptEngineering(self):
        
        prompt_template = """
        * Your name is **Max** chat design to help **Human**.
        * Respond with honesty and clarity. 
        * Don't create any questions or answers on your own. 
        * Keep your responses to one sentence max.

        {chat_history}
        **Human**: {context}
        **You**:
        """
        
        prompt = PromptTemplate(
            input_variables=["chat_history","context"],
            template=prompt_template
        )
        

        
        chain = LLMChain(
            llm = self.llm,
            prompt = prompt,
            memory = self.memory,
            verbose=False
        )
                
        return chain
        
    def clean_string(self, input_text):
        terms = ['**Hassan**:','Hassan:',"**Hassan:**"]
        earliest_position = len(input_text)
        for term in terms:
            position = input_text.find(term)
            if position != -1 and position < earliest_position:
                earliest_position = position
        
        return input_text[:earliest_position].strip()
    

    def generateResponse(self, prompt):
        response = self.PromptEngineering().invoke(prompt)
        response = response['text']
        print("BEFORE: ",response)
        response = self.clean_string(response)
        print("AFTER: ",response)
        return response
    