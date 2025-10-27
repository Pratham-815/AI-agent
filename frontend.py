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
    
    if agent_mode == "Multi-Agent System":
        st.info("""
        **How Multi-Agent Works:**
        
        🔍 **Research Agent**
        - Collects raw data & facts
        - Uses web search
        - No interpretation
        
        🧠 **Analyzer Agent**
        - Finds patterns
        - Critical thinking
        - Identifies insights
        
        ✍️ **Writer Agent**
        - Synthesizes everything
        - Creates final answer
        - Proper formatting
        """)
    
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
        placeholder="Try: 'What are the latest AI trends in 2025?' or 'Compare Python vs JavaScript for web development'"
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
                            
                            # Show workflow with icons
                            with st.expander("🔄 Agent Workflow Process", expanded=False):
                                for step in response_data.get("steps", []):
                                    if isinstance(step, dict):
                                        if step.get("status") == "in_progress":
                                            st.info(step.get("message"))
                                        else:
                                            st.success(step.get("message"))
                                    else:
                                        st.write(step)
                            
                            st.divider()
                            
                            # Create three distinct sections with clear labeling
                            st.markdown("### 📊 Agent Outputs Comparison")
                            
                            tab1, tab2, tab3 = st.tabs([
                                "📄 Final Answer (Writer Agent)", 
                                "🔍 Raw Data (Research Agent)", 
                                "🧠 Critical Analysis (Analyzer Agent)"
                            ])
                            
                            with tab1:
                                st.markdown("**This is the synthesized, user-friendly answer:**")
                                st.markdown("---")
                                st.markdown(response_data.get("final_response", "No response"))
                            
                            with tab2:
                                st.markdown("**This is raw data collected without interpretation:**")
                                st.markdown("---")
                                st.markdown(response_data.get("research_data", "No research data"))
                                st.caption("ℹ️ Notice: Just facts and data points, no opinions")
                            
                            with tab3:
                                st.markdown("**This is critical analysis of the raw data:**")
                                st.markdown("---")
                                st.markdown(response_data.get("analysis", "No analysis"))
                                st.caption("ℹ️ Notice: Patterns, insights, and critical thinking")
                            
                            # Show metadata
                            if "metadata" in response_data:
                                st.divider()
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.metric("Agents Used", response_data["metadata"].get("total_agents", 3))
                                with col_b:
                                    search_status = "✅ Enabled" if response_data["metadata"].get("search_enabled") else "❌ Disabled"
                                    st.metric("Web Search", search_status)
                        else:
                            # Show single agent response
                            st.markdown(response_data.get("final_response", response_data))
            else:
                st.error(f"Error: {response.status_code}")
    else:
        st.warning("Please enter a query!")