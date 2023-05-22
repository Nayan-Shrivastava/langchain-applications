from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate
import extension
# Set up the prompt template
template = """You are a chatbot having a conversation with a human.

{chat_history}
Human: {human_input}
Chatbot:"""

# Define the prompt template with input variables
prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"],
    template=template
)

# Create a ConversationBufferMemory instance
memory = ConversationBufferMemory(memory_key="chat_history")

# Create an LLMChain with memory
llm_chain = LLMChain(
    llm=OpenAI(),
    prompt=prompt,
    # verbose=True,
    memory=memory
)

# ANSI escape sequence for green color
GREEN_COLOR = "\033[92m"

# Start the conversation with the chatbot
while True:
    human_input = input("Human Input: ")
    
    if human_input.lower() == 'exit':
        print('Exiting...')
        break
    
    response = llm_chain.predict(human_input=human_input)
    print(f"{GREEN_COLOR}{response}\033[0m")
