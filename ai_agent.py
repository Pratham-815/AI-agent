import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch 

openai_llm=ChatOpenAI(model="gpt-4o-mini")
groq_llm=ChatGroq(model="llama-3.3-70b-versatile")

search_tool=TavilySearch(max_results=2)

from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage

system_prompt="Act as an AI chatbot who is smart and friendly"

agent = create_agent(
    model=groq_llm,
    tools=[search_tool],
    system_prompt=system_prompt,
)

query = "Tell me about the trends in AI"
state = {"messages": query}
response = agent.invoke(state)
messages = response.get("messages")
ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
print(ai_messages[-1])
