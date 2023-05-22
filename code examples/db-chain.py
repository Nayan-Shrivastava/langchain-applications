from langchain import SQLDatabase, SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from extension import llm

# Set up the database connection parameters
db_user = "postgres"
db_password = "12345"
db_host = "127.0.0.1:5432"
db_name = "dvdrental"

# Create a SQLDatabase object using the connection parameters
db = SQLDatabase.from_uri(f"postgresql+psycopg2://postgres:{db_password}@{db_host}/{db_name}")

# Create a SQLDatabaseChain object using the language model (llm) and the database
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)


# Define the query format for prompting the database
QUERY = """
Given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

{question}
"""

def get_prompt():
    print("Type 'exit' to quit")

    while True:
        prompt = input("Enter a prompt: ")

        if prompt.lower() == 'exit':
            print('Exiting...')
            break
        else:
            try:
                # format the QUERY prompt with out question
                question = QUERY.format(question=prompt)
                print(db_chain.run(question))
            except Exception as e:
                print(e)

# Start the prompt loop
get_prompt()

# Examples of possible questions to ask the database
# question - Which actor starred in film "Alabama Devil"
# question - Which is the most rented movie
# question - Which is the most expensive movie to rent?