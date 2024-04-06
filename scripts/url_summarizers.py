from typing import List, Dict, Any
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.chains.summarize import load_summarize_chain
import json

def summarize_urls(response_dict: Dict[Any, Any]) -> str:
    urls = extract_urls_from_response(response_dict)
    print(len(urls))
    urls = urls[:10]
    loader = UnstructuredURLLoader(urls=urls)
    docs = loader.load()

    llm = ChatOpenAI(temperature=0, model_name="gpt-4-0125-preview")
    chain = load_summarize_chain(llm, chain_type="stuff")

    return chain.run(docs)

def extract_urls_from_response(response_dict: Dict[Any, Any]):
    search_results = response_dict["results"]
    urls = [result["url"] for result in search_results]
    return urls    

if __name__ == "__main__":
    with open("assets/search_result_20240406_230103.json", 'r') as f:
        response = json.load(f)
    summary = summarize_urls(response)
    print(summary)