from langchain import LangChain
from langgraph import LangGraph
from langsmith import LangSmith
from agents.agent import AgentExecutor
from agents.output_parsers.json import JSONAgentOutputParser
import requests
import os
import asyncio

def validate_and_format_response(response: dict, tool_name: str) -> dict:
    """Valida y formatea la respuesta de cada herramienta."""
    if not response:
        return {"error": f"No response from {tool_name}"}
    return {"tool": tool_name, "output": response}

async def fetch_tavily_data(topic: str) -> dict:
    """Integra Tavily para obtener datos adicionales."""
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    response = requests.get(
        f"https://api.tavily.com/search",
        params={"query": topic},
        headers={"Authorization": f"Bearer {tavily_api_key}"}
    )
    if response.status_code != 200:
        return {"error": "Failed to fetch Tavily data"}
    return response.json()

async def process_with_lang_tools(prompt: str):
    """Ejecuta las herramientas de LangChain, LangGraph y LangSmith."""
    langchain = LangChain(api_key=os.getenv("LANGCHAIN_API_KEY"))
    langgraph = LangGraph(api_key=os.getenv("LANGGRAPH_API_KEY"))
    langsmith = LangSmith(api_key=os.getenv("LANGSMITH_API_KEY"))

    # Ejecutar herramientas en paralelo
    langchain_task = asyncio.to_thread(langchain.process, prompt)
    langgraph_task = asyncio.to_thread(langgraph.analyze, prompt)
    langsmith_task = asyncio.to_thread(langsmith.optimize, prompt)

    langchain_response, langgraph_response, langsmith_response = await asyncio.gather(
        langchain_task, langgraph_task, langsmith_task
    )

    return {
        "langchain": validate_and_format_response(langchain_response, "LangChain"),
        "langgraph": validate_and_format_response(langgraph_response, "LangGraph"),
        "langsmith": validate_and_format_response(langsmith_response, "LangSmith")
    }

async def integrate_with_lang_tools(input_data: str, language: str, personal_info: str = None):
    """Integra múltiples herramientas y Tavily."""
    # Construir el prompt personalizado
    prompt = f"Generate content in {language} for {input_data}"
    if personal_info:
        prompt += f" including details about {personal_info}"

    # Procesar herramientas LangChain, LangGraph y LangSmith
    lang_tools_response = await process_with_lang_tools(prompt)

    # Obtener datos adicionales de Tavily
    tavily_data = await fetch_tavily_data(input_data)

    # Preparar el agente y el parser
    agent_executor = AgentExecutor()
    output_parser = JSONAgentOutputParser()
    parsed_langchain_output = output_parser.parse(lang_tools_response["langchain"]["output"])

    # Consolidar respuestas
    return {
        "langchain": parsed_langchain_output,
        "langgraph": lang_tools_response["langgraph"],
        "langsmith": lang_tools_response["langsmith"],
        "tavily": tavily_data
    }
