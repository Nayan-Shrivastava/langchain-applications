from langchain.document_loaders.base import Document
from langchain.document_loaders import TextLoader
from langchain.utilities import ApifyWrapper
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from extension import llm
from dotenv import load_dotenv
load_dotenv()

# Set your OpenAI API key and Apify API token
# os.environ["OPENAI_API_KEY"] = "Your OpenAI API key"
# os.environ["APIFY_API_TOKEN"] = "Your Apify API token"

def append_text_to_file(file_path, text):
    try:
        with open(file_path, 'a') as file:
            file.write(text)
            file.write('\n')
    except IOError:
        print(f"Error: Unable to append text to the file '{file_path}'.")

# to be called for each data item received by crawler
def map_function(item):
    append_text_to_file('./files/chat_bot.txt',item["text"] or "")
    return Document(page_content=item["text"] or "", metadata={"source": item["url"]})

# Load the TEXT Document
def loadTextDocument(file_path):
    loader = TextLoader(file_path)
    documents = loader.load()
    return documents


def ask(query):
    # load the text file containing scraped information and split into Documents.
    documents = loadTextDocument('./files/chat_bot.txt')
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    if not docs:
        return ''

    # Load the documents into vector Store and search for similar source documents for given query
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    docs = db.similarity_search(query)

    # Call QA Chain with relevant docs and run chain.
    chain = load_qa_chain(llm, chain_type="stuff", verbose=False)
    res = chain.run(input_documents=docs, question=query)
    print("\nQuestion: ", query, "\n")
    print("Answer:",res)

def crawl(url):
    # Initialize ApifyWrapper
    apify = ApifyWrapper()

    # Call the Website Content Crawler Actor and fetch the results
    apify.call_actor(
        actor_id="apify/website-content-crawler",
        run_input={"startUrls": [{"url": url}]},
        dataset_mapping_function=map_function
    ).load()


ask("who is CEO of rapid innovation")

# crawl("https://www.rapidinnovation.io/")