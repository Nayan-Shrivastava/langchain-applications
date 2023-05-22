from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0.2,model_name='gpt-3.5-turbo')
# llm = OpenAI(temperature=0.2,model_name='text-davinci-003')
