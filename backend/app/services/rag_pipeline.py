from app.models.schemas import ContentRequest, ContentResponse
import openai
import requests
import os
from .graph_rag_agent import GraphRAGAgent  # Custom knowledge graph agent

def fetch_scientific_documents(topic: str) -> str:
    """Fetch scientific documents from arXiv."""
    arxiv_api_url = "http://export.arxiv.org/api/query"
    query = {"search_query": f"all:{topic}", "start": 0, "max_results": 5}
    
    response = requests.get(arxiv_api_url, params=query)
    if response.status_code != 200:
        raise Exception("Failed to fetch scientific documents from arXiv")
    
    return response.text

def enrich_with_graph_rag(documents: str, topic: str) -> str:
    """Enrich content with Graph RAG agent."""
    agent = GraphRAGAgent()
    enriched_data = agent.build_graph_from_documents(documents, topic)
    return enriched_data

def generate_scientific_content(request: ContentRequest) -> ContentResponse:
    """Generate scientific content using RAG and knowledge graphs."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    # Step 1: Fetch scientific documents from arXiv
    documents = fetch_scientific_documents(request.topic)
    
    # Step 2: Use Graph RAG to enrich documents
    enriched_data = enrich_with_graph_rag(documents, request.topic)
    
    # Step 3: Integrate Tavily for additional validation
    tavily_response = requests.post(
        "https://api.tavily.com/enrich",
        json={"data": enriched_data, "topic": request.topic},
        headers={"Authorization": f"Bearer {tavily_api_key}"}
    )
    if tavily_response.status_code != 200:
        raise Exception("Failed to enrich content using Tavily")
    tavily_data = tavily_response.json()
    
    # Step 4: Generate final content using OpenAI
    prompt = (
        f"Summarize the following enriched scientific content into an easy-to-understand article "
        f"for {request.audience}:\n\n{tavily_data['enriched_content']}\n"
    )
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        temperature=0.7,
        n=1,
        stop=None
    )
    
    return ContentResponse(
        content=response.choices[0].text.strip(),
        image_url=tavily_data.get("related_image_url", "")
    )
