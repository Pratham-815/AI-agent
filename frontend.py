import streamlit as st
import requests

st.set_page_config(page_title="LangGraph Agent UI", layout="wide")
st.title("🤖 AI Agent System")
st.write("Create and Interact with Single or Multi-Agent AI Systems!")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Agent Mode Selection
    agent_mode = st.radio(
        "Select Agent Mode:",
        ("Single Agent", "Multi-Agent System"),
        help="Multi-Agent uses specialized agents for research, analysis, and writing"
    )
    
    st.divider()
    
    # Provider and Model Selection
    MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "groq/compound-mini"]
    MODEL_NAMES_OPENAI = ["gpt-4o-mini"]
    MODEL_NAMES_GEMINI = ["gemini-1.5-flash", "gemini-2.5-pro"]
    
    provider = st.radio("Select Provider:", ("Groq", "OpenAI", "Gemini"))
    
    if provider == "Groq":
        selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
    elif provider == "OpenAI":
        selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)
    elif provider == "Gemini":
        selected_model = st.selectbox("Select Gemini Model:", MODEL_NAMES_GEMINI)
    
    allow_web_search = st.checkbox("Allow Web Search", value=True)
    
    if selected_model == "groq/compound-mini" and allow_web_search:
        st.warning("⚠️ Web search is not supported with compound-mini model.")
        allow_web_search = False

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Input")
    
    if agent_mode == "Single Agent":
        system_prompt = st.text_area(
            "Define your AI Agent:", 
            height=100, 
            placeholder="Type your system prompt here...",
            value="Act as an AI chatbot who is smart and friendly"
        )
    else:
        st.info("💡 Multi-Agent mode uses specialized agents with pre-defined roles")
        system_prompt = ""
    
    user_query = st.text_area(
        "Enter your query:", 
        height=200, 
        placeholder="Ask anything!"
    )

with col2:
    st.subheader("💬 Response")
    response_container = st.container()

API_URL = "http://127.0.0.1:9999/chat"

if st.button("🚀 Ask Agent!", type="primary", use_container_width=True):
    if user_query.strip():
        with st.spinner("Processing your query..."):
            payload = {
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_web_search,
                "use_multi_agent": (agent_mode == "Multi-Agent System")
            }
            
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                response_data = response.json()
                
                if "error" in response_data:
                    st.error(response_data["error"])
                else:
                    with response_container:
                        if agent_mode == "Multi-Agent System":
                            # Show multi-agent process
                            st.success("✅ Multi-Agent Processing Complete!")
                            
                            with st.expander("🔍 Agent Workflow", expanded=True):
                                for step in response_data.get("steps", []):
                                    st.write(step)
                            
                            st.divider()
                            
                            # Tabs for different outputs
                            tab1, tab2, tab3 = st.tabs(["📄 Final Response", "🔬 Research Data", "📊 Analysis"])
                            
                            with tab1:
                                st.markdown(response_data.get("final_response", "No response"))
                            
                            with tab2:
                                st.markdown(response_data.get("research_data", "No research data"))
                            
                            with tab3:
                                st.markdown(response_data.get("analysis", "No analysis"))
                        else:
                            # Show single agent response
                            st.markdown(response_data.get("final_response", response_data))
            else:
                st.error(f"Error: {response.status_code}")
    else:
        st.warning("Please enter a query!")