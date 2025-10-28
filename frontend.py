import streamlit as st
import requests

st.set_page_config(page_title="AI Agent", layout="wide")
st.title("🤖 AI Agent System")
st.write("Create and Interact with Single or Multi-Agent AI Systems!")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Agent Mode Selection
    agent_mode = st.radio(
        "Select Agent Mode:",
        ("Single Agent", "Multi-Agent (Sequential)", "Multi-Agent (Debate)"),
        help="Choose how agents collaborate"
    )
    
    if agent_mode == "Multi-Agent (Sequential)":
        st.info("""
        **Sequential Multi-Agent:**
        
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
    elif agent_mode == "Multi-Agent (Debate)":
        st.success("""
        **🆕 Debate Mode:**
        
        💭 **3 Agents Debate:**
        - 🌟 Optimist (positive view)
        - ⚠️ Skeptic (critical view)  
        - 📊 Neutral (balanced view)
        
        ⚖️ **Mediator** synthesizes consensus
        
        Perfect for controversial questions!
        """)
    
    st.divider()
    
    # Provider and Model Selection
    MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "groq/compound-mini", "openai/gpt-oss-120b"]
    MODEL_NAMES_GEMINI = ["gemini-2.0-flash", "gemini-2.5-pro"]

    provider = st.radio("Select Provider:", ("Groq", "Gemini"))
    
    if provider == "Groq":
        selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
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
        placeholder="Try: 'Should I learn Python or JavaScript?' or 'Is AI going to replace programmers?'"
    )

with col2:
    st.subheader("💬 Response")
    response_container = st.container()

API_URL = "http://127.0.0.1:9999/chat"

if st.button("🚀 Ask Agent!", type="primary", use_container_width=True):
    if user_query.strip():
        with st.spinner("Processing your query..."):
            # Determine agent mode for backend
            use_multi_agent = agent_mode in ["Multi-Agent (Sequential)", "Multi-Agent (Debate)"]
            backend_mode = "debate" if agent_mode == "Multi-Agent (Debate)" else "sequential"
            
            payload = {
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_web_search,
                "use_multi_agent": use_multi_agent,
                "agent_mode": backend_mode
            }
            
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                response_data = response.json()
                
                if "error" in response_data:
                    st.error(response_data["error"])
                else:
                    with response_container:
                        # DEBATE MODE OUTPUT
                        if response_data.get("metadata", {}).get("mode") == "debate":
                            st.success("✅ Multi-Agent Debate Complete!")
                            
                            # Show debate process
                            with st.expander("🗣️ Debate Process", expanded=False):
                                for step in response_data.get("steps", []):
                                    if step.get("status") == "in_progress":
                                        st.info(step.get("message"))
                                    else:
                                        st.success(step.get("message"))
                            
                            st.divider()
                            
                            # Show individual perspectives in columns
                            st.markdown("### 💭 Individual Agent Perspectives")
                            
                            debate_responses = response_data.get("debate_responses", [])
                            
                            col1, col2, col3 = st.columns(3)
                            columns = [col1, col2, col3]
                            
                            for idx, debate_resp in enumerate(debate_responses):
                                with columns[idx]:
                                    agent_name = debate_resp.get("agent", "Agent")
                                    emoji = debate_resp.get("emoji", "🤖")
                                    
                                    # Colored headers based on agent type
                                    if "Optimist" in agent_name:
                                        st.success(f"{emoji} **{agent_name} Agent**")
                                    elif "Skeptic" in agent_name:
                                        st.warning(f"{emoji} **{agent_name} Agent**")
                                    else:
                                        st.info(f"{emoji} **{agent_name} Agent**")
                                    
                                    with st.container(border=True, height=300):
                                        st.markdown(debate_resp.get("response", "No response"))
                            
                            st.divider()
                            
                            # Show consensus
                            st.markdown("### ⚖️ Mediator's Consensus")
                            with st.container(border=True):
                                st.markdown(response_data.get("final_response", "No consensus reached"))
                            
                            # Show metadata
                            st.divider()
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.metric("Agents Participated", response_data["metadata"].get("agents_participated", 4))
                            with col_b:
                                search_status = "✅ Enabled" if response_data["metadata"].get("search_enabled") else "❌ Disabled"
                                st.metric("Web Search", search_status)
                        
                        # SEQUENTIAL MULTI-AGENT OUTPUT
                        elif agent_mode == "Multi-Agent (Sequential)":
                            st.success("✅ Multi-Agent Processing Complete!")
                            
                            # Show workflow steps
                            with st.expander("🔄 Agent Workflow", expanded=False):
                                for step in response_data.get("steps", []):
                                    if step.get("status") == "in_progress":
                                        st.info(step.get("message"))
                                    else:
                                        st.success(step.get("message"))
                            
                            st.divider()
                            
                            # Tabs for each agent output
                            tab1, tab2, tab3 = st.tabs(["✍️ Final Response", "🧠 Analysis", "🔍 Research"])
                            
                            with tab1:
                                st.markdown("### Writer Agent Output")
                                st.markdown(response_data.get("final_response", "No response"))

                            with tab2:
                                st.markdown("### Analyzer Agent Output")
                                st.markdown(response_data.get("analysis", "No analysis"))
                            
                            with tab3:
                                st.markdown("### Research Agent Output")
                                st.markdown(response_data.get("research", "No research data"))
                            
                            # Show metadata
                            st.divider()
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.metric("Agents Used", response_data.get("metadata", {}).get("total_agents", 3))
                            with col_b:
                                search_status = "✅ Enabled" if response_data.get("metadata", {}).get("search_enabled") else "❌ Disabled"
                                st.metric("Web Search", search_status)
                        
                        # SINGLE AGENT OUTPUT
                        else:
                            st.success("✅ Response Generated!")
                            st.markdown(response_data.get("final_response", "No response"))
            else:
                with response_container:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
    else:
        st.warning("Please enter a query!")