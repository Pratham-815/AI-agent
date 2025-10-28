import streamlit as st

st.set_page_config(page_title="Model Guide", layout="wide", page_icon="📚")

st.title("📚 AI Model Selection Guide")
st.write("Choose the right model for your needs")

# Introduction
st.markdown("""
This guide helps you understand the capabilities, strengths, and ideal use cases 
for each available AI model in our system.
""")

st.divider()

# Groq Models Section
st.header("🚀 Groq Models (Ultra-Fast Inference)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🦙 llama-3.3-70b-versatile")
    
    st.markdown("""
    **Provider:** Groq  
    **Size:** 70 billion parameters  
    **Speed:** ⚡⚡⚡ Very Fast (2-5 seconds)
    
    ### ✅ Best For:
    - General conversational AI
    - Complex reasoning tasks
    - Multi-turn conversations
    - Creative writing
    - Code generation
    
    ### 💪 Strengths:
    - Balanced performance across all tasks
    - Excellent reasoning capabilities
    - Fast response times
    - Good at following instructions
    
    ### ⚠️ Limitations:
    - May hallucinate on very recent events
    - Not specialized for any specific domain
    
    ### 🎯 Recommended Use Cases:
    ```
    ✓ "Explain quantum computing"
    ✓ "Write a Python function for..."
    ✓ "Help me plan a trip to Japan"
    ✓ "Debug this code..."
    ✓ Multi-Agent Sequential Mode
    ```
    
    ### 💡 Pro Tip:
    This is the **best all-around model** for most tasks. Great default choice!
    """)

with col2:
    st.subheader("⚡ groq/compound-mini")
    
    st.markdown("""
    **Provider:** Groq  
    **Size:** Smaller, optimized model  
    **Speed:** ⚡⚡⚡⚡ Ultra Fast (1-2 seconds)
    
    ### ✅ Best For:
    - Simple questions
    - Quick responses
    - Basic conversations
    - When speed is critical
    
    ### 💪 Strengths:
    - Fastest response times
    - Low latency
    - Efficient token usage
    - Good for simple tasks
    
    ### ⚠️ Limitations:
    - ❌ **No web search support**
    - Limited reasoning capabilities
    - Shorter context window
    - Less creative outputs
    
    ### 🎯 Recommended Use Cases:
    ```
    ✓ "What is 2+2?"
    ✓ "Define photosynthesis"
    ✓ "Translate 'hello' to Spanish"
    ✓ Simple Q&A
    ✗ Complex research questions
    ✗ Multi-Agent modes
    ```
    
    ### 💡 Pro Tip:
    Use this when you need **speed over depth**. Not recommended for multi-agent.
    """)

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.subheader("🌐 openai/gpt-oss-120b")
    
    st.markdown("""
    **Provider:** Groq (OpenAI-compatible)  
    **Size:** 120 billion parameters  
    **Speed:** ⚡⚡ Fast (3-6 seconds)
    
    ### ✅ Best For:
    - Advanced reasoning
    - Complex analysis
    - Professional writing
    - Technical documentation
    
    ### 💪 Strengths:
    - Largest Groq model available
    - Superior reasoning capabilities
    - Excellent for technical content
    - High-quality outputs
    
    ### ⚠️ Limitations:
    - Slightly slower than other Groq models
    - Higher token costs
    
    ### 🎯 Recommended Use Cases:
    ```
    ✓ "Analyze this business proposal"
    ✓ "Write technical documentation"
    ✓ "Explain complex algorithms"
    ✓ Multi-Agent Debate Mode
    ✓ Professional content creation
    ```
    
    ### 💡 Pro Tip:
    Best choice for **professional or academic** work requiring deep analysis.
    """)

with col4:
    st.info("**💡 Groq Summary:**\n\n"
            "- **Speed Champions:** All Groq models are ultra-fast\n"
            "- **Infrastructure:** Specialized hardware (LPU)\n"
            "- **Best For:** Real-time applications, demos\n"
            "- **Pricing:** Very cost-effective")

st.divider()

# Google Gemini Models Section
st.header("🤖 Google Gemini Models (Multimodal AI)")

col5, col6 = st.columns(2)

with col5:
    st.subheader("✨ gemini-2.0-flash")
    
    st.markdown("""
    **Provider:** Google  
    **Generation:** Latest (2.0)  
    **Speed:** ⚡⚡ Medium (5-10 seconds)
    
    ### ✅ Best For:
    - Balanced performance
    - Real-time interactions
    - Multimodal understanding
    - Cost-effective solutions
    
    ### 💪 Strengths:
    - Latest Google AI technology
    - Good balance of speed/quality
    - Handles complex queries well
    - Free tier available
    
    ### ⚠️ Limitations:
    - ⚠️ Slower than Groq models
    - Response time varies with load
    - May have API rate limits
    
    ### 🎯 Recommended Use Cases:
    ```
    ✓ "Summarize this research paper"
    ✓ "Compare different approaches to..."
    ✓ "Create a detailed analysis of..."
    ✓ Single Agent mode (faster)
    ✓ When Groq is unavailable
    ```
    
    ### 💡 Pro Tip:
    Good **alternative to Groq** when you need Google's reasoning style.
    """)

with col6:
    st.subheader("🧠 gemini-2.5-pro")
    
    st.markdown("""
    **Provider:** Google  
    **Generation:** Advanced (2.5)  
    **Speed:** ⚡ Slower (8-15 seconds)
    
    ### ✅ Best For:
    - Complex reasoning tasks
    - Academic research
    - Professional analysis
    - High-quality content
    
    ### 💪 Strengths:
    - Most advanced reasoning
    - Superior analysis quality
    - Excellent for research
    - Handles nuanced queries
    
    ### ⚠️ Limitations:
    - ⚠️ **Slowest model** (8-15s single, 30-60s multi-agent)
    - Higher API costs
    - May hit rate limits faster
    - Not ideal for real-time use
    
    ### 🎯 Recommended Use Cases:
    ```
    ✓ "Conduct thorough analysis of..."
    ✓ "Research the implications of..."
    ✓ Academic papers and research
    ✓ When quality > speed
    ✗ Real-time demos (too slow)
    ✗ Simple questions (overkill)
    ```
    
    ### 💡 Pro Tip:
    Use for **final analysis** or when **quality is paramount**. Not for demos!
    """)

st.divider()

st.info("**⏱️ Gemini Performance Note:**\n\n"
        "Gemini models are slower than Groq, especially in Multi-Agent mode:\n"
        "- **Single Agent:** 5-15 seconds\n"
        "- **Multi-Agent Sequential:** 20-45 seconds\n"
        "- **Multi-Agent Debate:** 30-60 seconds\n\n"
        "💡 Tip: Use Groq for demos and presentations!")

st.divider()

# Quick Decision Guide
st.header("🎯 Quick Decision Guide")

decision_col1, decision_col2, decision_col3 = st.columns(3)

with decision_col1:
    st.markdown("""
    ### 🏃 Need Speed?
    
    **Choose:**
    - ⚡ `groq/compound-mini` (fastest)
    - ⚡ `llama-3.3-70b-versatile` (fast + quality)
    
    **Avoid:**
    - ❌ `gemini-2.5-pro` (slow)
    """)

with decision_col2:
    st.markdown("""
    ### 🎓 Need Quality?
    
    **Choose:**
    - 🧠 `openai/gpt-oss-120b` (best reasoning)
    - 🧠 `gemini-2.5-pro` (deep analysis)
    
    **Avoid:**
    - ❌ `compound-mini` (basic only)
    """)

with decision_col3:
    st.markdown("""
    ### ⚖️ Need Balance?
    
    **Choose:**
    - 🦙 `llama-3.3-70b-versatile` (all-rounder)
    - ✨ `gemini-2.0-flash` (good balance)
    
    **Best for:**
    - ✅ Most use cases
    """)

st.divider()

# Mode-Specific Recommendations
st.header("🔧 Mode-Specific Recommendations")

tab1, tab2, tab3 = st.tabs(["Single Agent", "Sequential Multi-Agent", "Debate Mode"])

with tab1:
    st.markdown("""
    ## Single Agent Mode
    
    ### ⚡ Fastest Setup:
    - **Model:** `groq/compound-mini`
    - **Web Search:** Disabled
    - **Use For:** Simple questions, definitions
    
    ### 🎯 Best General Purpose:
    - **Model:** `llama-3.3-70b-versatile`
    - **Web Search:** Enabled
    - **Use For:** Most questions, code help, explanations
    
    ### 🧠 Best Quality:
    - **Model:** `openai/gpt-oss-120b`
    - **Web Search:** Enabled
    - **Use For:** Professional work, analysis
    """)

with tab2:
    st.markdown("""
    ## Sequential Multi-Agent Mode
    
    ### ⚡ Recommended (Fast):
    - **Model:** `llama-3.3-70b-versatile`
    - **Web Search:** Enabled
    - **Time:** ~10-15 seconds
    - **Use For:** Research questions, explanations
    
    ### 🧠 Advanced (Slower):
    - **Model:** `openai/gpt-oss-120b`
    - **Web Search:** Enabled
    - **Time:** ~15-25 seconds
    - **Use For:** Deep research, academic work
    
    ### ❌ Not Recommended:
    - `compound-mini` (no web search support)
    - `gemini-2.5-pro` (too slow: 30-45s)
    """)

with tab3:
    st.markdown("""
    ## Debate Multi-Agent Mode
    
    ### ⚡ Recommended (Fast):
    - **Model:** `llama-3.3-70b-versatile`
    - **Web Search:** Enabled
    - **Time:** ~15-20 seconds
    - **Use For:** Controversial questions, decisions
    
    ### 🧠 Best Quality (Slower):
    - **Model:** `openai/gpt-oss-120b`
    - **Web Search:** Enabled
    - **Time:** ~20-30 seconds
    - **Use For:** Important decisions, critical analysis
    
    ### ❌ Not Recommended:
    - `compound-mini` (no web search)
    - `gemini-2.5-pro` (very slow: 30-60s)
    
    ### 💡 Perfect Questions for Debate:
    ```
    "Should I learn Python or JavaScript?"
    "Is remote work better than office?"
    "Should students use AI for homework?"
    "Is cryptocurrency a good investment?"
    ```
    """)

st.divider()

# Comparison Table
st.header("📊 Model Comparison Table")

comparison_data = {
    "Model": [
        "llama-3.3-70b-versatile",
        "groq/compound-mini",
        "openai/gpt-oss-120b",
        "gemini-2.0-flash",
        "gemini-2.5-pro"
    ],
    "Provider": ["Groq", "Groq", "Groq", "Google", "Google"],
    "Speed": ["⚡⚡⚡", "⚡⚡⚡⚡", "⚡⚡", "⚡⚡", "⚡"],
    "Quality": ["⭐⭐⭐⭐", "⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
    "Web Search": ["✅", "❌", "✅", "✅", "✅"],
    "Multi-Agent": ["✅ Recommended", "❌ Not Supported", "✅ Best", "⚠️ Slow", "❌ Too Slow"],
    "Best For": ["General use", "Speed", "Quality", "Balance", "Research"]
}

st.table(comparison_data)

st.divider()

# Footer with tips
st.success("""
### 🎯 Final Recommendations:

**For Demos/Presentations:**  
Use `llama-3.3-70b-versatile` or `groq/compound-mini` (Groq models are fast!)

**For Academic Work:**  
Use `openai/gpt-oss-120b` or `gemini-2.5-pro` (higher quality)

**For Real-Time Chat:**  
Use any Groq model with Single Agent mode

**For Important Decisions:**  
Use Debate Mode with `openai/gpt-oss-120b` or `llama-3.3-70b-versatile`

**When Unsure:**  
Start with `llama-3.3-70b-versatile` - it's the best all-rounder! 🦙
""")

st.divider()

# Back button
if st.button("⬅️ Back to Main App", type="primary", use_container_width=True):
    st.switch_page("D:/Mini Project/AI Agent/AI-agent/frontend.py")