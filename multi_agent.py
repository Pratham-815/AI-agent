import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage
from langchain_core.messages import HumanMessage

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

class MultiAgentOrchestrator:
    def __init__(self, llm_id, provider, allow_search=True):
        """Initialize the multi-agent system with specified LLM"""
        self.llm = self._get_llm(llm_id, provider)
        self.allow_search = allow_search
        
    def _get_llm(self, llm_id, provider):
        """Get the appropriate LLM based on provider"""
        if provider == "Groq":
            return ChatGroq(model=llm_id)
        elif provider == "OpenAI":
            return ChatOpenAI(model=llm_id)
        elif provider == "Gemini":
            return ChatGoogleGenerativeAI(model=llm_id, google_api_key=GEMINI_API_KEY)
    
    def research_agent(self, query):
        """Agent specialized in researching and gathering information"""
        research_prompt = """You are a Research Specialist. Your job is to:
        1. Gather comprehensive information about the query
        2. Use web search when needed to find latest information
        3. Identify key facts, data, and relevant details
        4. Present findings in a structured format
        
        Be thorough but concise."""
        
        tools = [TavilySearch(max_results=3)] if self.allow_search else []
        
        agent = create_agent(
            model=self.llm,
            tools=tools,
            system_prompt=research_prompt
        )
        
        state = {"messages": [query]}
        response = agent.invoke(state)
        messages = response.get("messages")
        ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
        
        return ai_messages[-1] if ai_messages else "No research data found."
    
    def analyzer_agent(self, research_data, original_query):
        """Agent specialized in analyzing information"""
        analysis_prompt = """You are an Analysis Expert. Your job is to:
        1. Analyze the research data provided
        2. Identify patterns, insights, and key takeaways
        3. Connect different pieces of information
        4. Evaluate credibility and relevance
        5. Provide critical thinking and deeper understanding
        
        Be analytical and insightful."""
        
        agent = create_agent(
            model=self.llm,
            tools=[],
            system_prompt=analysis_prompt
        )
        
        analysis_query = f"""Original Query: {original_query}
        
Research Data:
{research_data}

Please analyze this information and provide key insights."""
        
        state = {"messages": [analysis_query]}
        response = agent.invoke(state)
        messages = response.get("messages")
        ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
        
        return ai_messages[-1] if ai_messages else "No analysis available."
    
    def writer_agent(self, analysis, original_query):
        """Agent specialized in writing the final response"""
        writer_prompt = """You are a Professional Writer. Your job is to:
        1. Create a clear, well-structured response
        2. Make the information accessible and engaging
        3. Organize content logically with proper formatting
        4. Ensure accuracy while being comprehensive
        5. Add relevant examples or explanations where needed
        
        Write in a friendly yet professional tone."""
        
        agent = create_agent(
            model=self.llm,
            tools=[],
            system_prompt=writer_prompt
        )
        
        writing_query = f"""Original Query: {original_query}

Analysis:
{analysis}

Please write a comprehensive, well-formatted final response."""
        
        state = {"messages": [writing_query]}
        response = agent.invoke(state)
        messages = response.get("messages")
        ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
        
        return ai_messages[-1] if ai_messages else "Unable to generate response."
    
    def process_query(self, query):
        """Main orchestration method that coordinates all agents"""
        steps = []
        
        # Step 1: Research
        steps.append("🔍 **Research Agent** is gathering information...")
        research_result = self.research_agent(query)
        steps.append(f"✅ Research completed")
        
        # Step 2: Analysis
        steps.append("🧠 **Analyzer Agent** is processing the data...")
        analysis_result = self.analyzer_agent(research_result, query)
        steps.append(f"✅ Analysis completed")
        
        # Step 3: Writing
        steps.append("✍️ **Writer Agent** is crafting the final response...")
        final_result = self.writer_agent(analysis_result, query)
        steps.append(f"✅ Response ready!")
        
        return {
            "final_response": final_result,
            "research_data": research_result,
            "analysis": analysis_result,
            "steps": steps
        }