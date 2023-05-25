from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI
from langchain.utilities import ArxivAPIWrapper
from extension import llm



# llm = ChatOpenAI(temperature=0) # Initialize the LLM to be used

arxiv = ArxivAPIWrapper()

# Create tool
arxiv_tool = Tool(
    name="arxiv_search",
    # Setting Objective
    description="Search on arxiv. The tool can search a keyword on arxiv for the top papers. It will return publishing date, title, authors, and summary of the papers.",
    func=arxiv.run
)

# tools array
tools = [arxiv_tool]


# initialize the agent
agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

response = agent_chain.run("What is GPT4 and why is it so popular?")
print('\nRESPONSE >>>>>> ',response)