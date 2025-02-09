from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import TokenTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
import os
from langchain.prompts import PromptTemplate


qa = None


def initialize_langchat_model(openai_api_key, url):
    global qa

    try:
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

        if os.path.exists("chroma_db/"+url.split('/')[-1]) or os.path.exists("../chroma_db/"+url.split('/')[-1]):
            docsearch = Chroma(persist_directory="chroma_db/"+url.split('/')[-1], embedding_function=embeddings)
        else:
            directory = "data/" + url.split('/')[-1]
            if not os.path.exists(directory):
                directory = "../data/" + url.split('/')[-1]
            loader = DirectoryLoader(directory, silent_errors=True)
            documents = loader.load()

            text_splitter = TokenTextSplitter(chunk_size=350, chunk_overlap=20)
            texts = text_splitter.split_documents(documents)

            docsearch = Chroma.from_documents(texts, embeddings, persist_directory="chroma_db/"+url.split('/')[-1])
            # docsearch.persist()

        template = """You are an AI assistant for a software repository QA task, Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, can I help with anything else, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible.
                                Context: {context}
                                Question: {question}
                                Answer:"""

        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
        llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=openai_api_key, temperature=0)

        qa = RetrievalQA.from_chain_type(llm=llm,
                                         chain_type="stuff",
                                         retriever=docsearch.as_retriever(search_type="mmr"),
                                         return_source_documents=True,
                                         chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    except Exception as e:
        print(f"An exception occurred while initializing: {str(e)}")
        qa = None


async def generate_response_langchat(user_input, openai_api_key, url):
    global qa

    if qa is None:
        initialize_langchat_model(openai_api_key, url)

    if qa is None:
        return {"status": "error", "message": f"Failed to initialize model"}

    try:
        result = qa({"query": user_input})

        return result['result'], result['source_documents']
    except Exception as e:
        return {"status": "error", "message": f"Exception occurred: {str(e)}"}
