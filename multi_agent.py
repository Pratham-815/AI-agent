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
        """Agent specialized in RAW DATA COLLECTION ONLY"""
        research_prompt = """You are a Data Collector. Your ONLY job is to:
        1. Find and extract RAW facts, statistics, and information
        2. List sources and URLs when using web search
        3. Present data in bullet points WITHOUT any interpretation
        4. Include dates, numbers, quotes, and concrete details
        5. DO NOT analyze, summarize, or give opinions - just collect raw data
        
        Format: Return ONLY factual data points with sources."""
        
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
        """Agent specialized in CRITICAL ANALYSIS ONLY"""
        analysis_prompt = """You are a Critical Analyst. Your job is to:
        1. Identify PATTERNS and TRENDS in the raw data
        2. Compare and CONTRAST different data points
        3. Find CONTRADICTIONS or gaps in the information
        4. Evaluate CREDIBILITY and potential biases
        5. Generate INSIGHTS and deeper meanings
        6. DO NOT write final answers - only provide analytical observations
        
        Format: Return analysis in structured sections:
        - Key Patterns:
        - Important Insights:
        - Contradictions/Gaps:
        - Credibility Assessment:"""
        
        agent = create_agent(
            model=self.llm,
            tools=[],
            system_prompt=analysis_prompt
        )
        
        analysis_query = f"""Original Query: {original_query}

Raw Research Data:
{research_data}

Analyze this data critically. DO NOT answer the question - just analyze the data."""
        
        state = {"messages": [analysis_query]}
        response = agent.invoke(state)
        messages = response.get("messages")
        ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
        
        return ai_messages[-1] if ai_messages else "No analysis available."
    
    def writer_agent(self, research_data, analysis, original_query):
        """Agent specialized in SYNTHESIS and COMMUNICATION"""
        writer_prompt = """You are a Professional Communicator. Your job is to:
        1. SYNTHESIZE the research data and analysis into a coherent answer
        2. Answer the original question DIRECTLY and COMPLETELY
        3. Use proper formatting (headings, bullet points, bold text)
        4. Make it engaging and easy to understand
        5. Include examples and actionable takeaways
        6. Cite sources when relevant
        
        Format: Write a complete, well-structured response that actually answers the user's question."""
        
        agent = create_agent(
            model=self.llm,
            tools=[],
            system_prompt=writer_prompt
        )
        
        writing_query = f"""Original User Question: {original_query}

Raw Research Data:
{research_data}

Critical Analysis:
{analysis}

Now write a comprehensive answer to the user's question using the research and analysis above."""
        
        state = {"messages": [writing_query]}
        response = agent.invoke(state)
        messages = response.get("messages")
        ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
        
        return ai_messages[-1] if ai_messages else "Unable to generate response."
    
    def process_query(self, query):
        """Main orchestration method that coordinates all agents"""
        steps = []
        
        # Step 1: Research (Raw Data Collection)
        steps.append({
            "phase": "research",
            "status": "in_progress",
            "message": "🔍 **Research Agent** is collecting raw data and facts..."
        })
        research_result = self.research_agent(query)
        steps.append({
            "phase": "research",
            "status": "completed",
            "message": "✅ **Research Agent** collected data from multiple sources"
        })
        
        # Step 2: Analysis (Pattern Recognition & Critical Thinking)
        steps.append({
            "phase": "analysis",
            "status": "in_progress",
            "message": "🧠 **Analyzer Agent** is finding patterns and insights..."
        })
        analysis_result = self.analyzer_agent(research_result, query)
        steps.append({
            "phase": "analysis",
            "status": "completed",
            "message": "✅ **Analyzer Agent** identified key insights and patterns"
        })
        
        # Step 3: Writing (Synthesis & Communication)
        steps.append({
            "phase": "writing",
            "status": "in_progress",
            "message": "✍️ **Writer Agent** is synthesizing the final response..."
        })
        final_result = self.writer_agent(research_result, analysis_result, query)
        steps.append({
            "phase": "writing",
            "status": "completed",
            "message": "✅ **Writer Agent** completed the comprehensive response"
        })
        
        return {
            "final_response": final_result,
            "research_data": research_result,
            "analysis": analysis_result,
            "steps": steps,
            "metadata": {
                "total_agents": 3,
                "search_enabled": self.allow_search
            }
        }