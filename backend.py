from pydantic import BaseModel
from typing import List, Optional


class RequestModel(BaseModel): 
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool
    use_multi_agent: Optional[bool] = False  # New parameter


from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent
from multi_agent import MultiAgentOrchestrator

ALLOWED_MODEL_NAMES=["llama3-70b-8192", "groq/compound-mini", "llama-3.3-70b-versatile", "gpt-4o-mini", "gemini-1.5-flash", "gemini-2.5-pro"]

app = FastAPI(title="AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestModel):
    """
    API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Model not allowed. Please choose a valid model."}
    
    llm_id = request.model_name
    query = request.messages[0]  # Get first message
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider
    use_multi_agent = request.use_multi_agent

    # Use multi-agent system if requested
    if use_multi_agent:
        orchestrator = MultiAgentOrchestrator(llm_id, provider, allow_search)
        result = orchestrator.process_query(query)
        return result
    else:
        # Use single agent (existing functionality)
        response = get_response_from_ai_agent(llm_id, request.messages, allow_search, system_prompt, provider)
        return {"final_response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)