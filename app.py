import streamlit as st
from datetime import datetime
import logging
from main import initialize_agents, process_agent_query

logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Multi-Agent AI System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    
    .agent-response {
        background-color: rgba(28, 131, 225, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #4CAF50;
        color: inherit;
    }
    
    .agent-response h1, .agent-response h2, .agent-response h3,
    .agent-response h4, .agent-response h5, .agent-response h6,
    .agent-response p, .agent-response li, .agent-response td, 
    .agent-response th, .agent-response span {
        color: inherit !important;
    }
    
    .agent-response table {
        color: inherit !important;
        border-collapse: collapse;
        width: 100%;
        margin: 10px 0;
    }
    
    .agent-response table th {
        background-color: rgba(28, 131, 225, 0.2);
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .agent-response table td {
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .query-box {
        background-color: rgba(28, 131, 225, 0.05);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 3px solid #1f77b4;
    }
    
    .agent-card {
        background-color: rgba(76, 175, 80, 0.1);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 3px solid #4CAF50;
    }
    
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'total_queries' not in st.session_state:
    st.session_state.total_queries = 0
if 'process_query' not in st.session_state:
    st.session_state.process_query = False
if 'current_query' not in st.session_state:
    st.session_state.current_query = ""

def render_sidebar():
    """Render sidebar content"""
    with st.sidebar:
        st.markdown("## 🤖 FinSight-AI-Financial-Agent")
        st.markdown("---")
        
        st.markdown("""
        ### 🎯 Agent Team
        This system uses multiple specialized AI agents:
        """)
        
        st.markdown("""
        <div class='agent-card'>
            <strong>🌐 Web Agent</strong><br>
            <small>Searches the web for real-time information</small>
        </div>
        <div class='agent-card'>
            <strong>💰 Finance Agent</strong><br>
            <small>Analyzes financial data and metrics</small>
        </div>
        <div class='agent-card'>
            <strong>🤝 Team Coordinator</strong><br>
            <small>Orchestrates agent collaboration</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📊 Session Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Queries", st.session_state.total_queries)
        with col2:
            st.metric("History", len(st.session_state.chat_history))
        
        st.markdown("---")
        
        st.markdown("""
        ### 👨‍💻 Asadullah Shehbaz
        **AI Engineer**
        """)
        
        st.markdown("---")
        
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.total_queries = 0
            logger.info("Chat history cleared")
            st.rerun()

def render_quick_actions():
    """Render quick action buttons"""
    st.markdown("### 🔥 Quick Analysis")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 NVDA Analysis", use_container_width=True):
            st.session_state.current_query = "Provide detailed analysis and recent information about NVDA stock"
            st.session_state.process_query = True
            logger.info("Quick query: NVDA")
    with col2:
        if st.button("🍎 AAPL Insights", use_container_width=True):
            st.session_state.current_query = "Provide detailed analysis and recent information about AAPL stock"
            st.session_state.process_query = True
            logger.info("Quick query: AAPL")
    with col3:
        if st.button("🔋 TSLA Report", use_container_width=True):
            st.session_state.current_query = "Provide detailed analysis and recent information about TSLA stock"
            st.session_state.process_query = True
            logger.info("Quick query: TSLA")
    
    st.markdown("---")
    
    st.markdown("### 💡 Analysis Types")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📈 Tech Stocks", use_container_width=True):
            st.session_state.current_query = "What are the current trends in major technology stocks?"
            st.session_state.process_query = True
    with col2:
        if st.button("💰 Market Overview", use_container_width=True):
            st.session_state.current_query = "Provide an overview of current stock market conditions"
            st.session_state.process_query = True
    with col3:
        if st.button("🏦 Economic News", use_container_width=True):
            st.session_state.current_query = "What are the latest important economic developments?"
            st.session_state.process_query = True
    with col4:
        if st.button("🌍 Global Markets", use_container_width=True):
            st.session_state.current_query = "Provide information about global stock market performance"
            st.session_state.process_query = True

def render_query_input():
    """Render main query input section"""
    st.markdown("### 🔍 Custom Query")
    col_input, col_button = st.columns([4, 1])
    
    with col_input:
        user_query = st.text_input(
            "Enter your query:",
            value="",
            placeholder="e.g., Analyze NVDA stock and provide recent information",
            label_visibility="collapsed",
            key="user_input"
        )
    
    with col_button:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Analyze", use_container_width=True, type="primary"):
            if user_query:
                st.session_state.current_query = user_query
                st.session_state.process_query = True
                logger.info(f"Custom query submitted: {user_query}")

def process_query():
    """Process the current query"""
    if st.session_state.process_query and st.session_state.current_query:
        query_to_process = st.session_state.current_query
        st.session_state.total_queries += 1
        logger.info(f"Processing query #{st.session_state.total_queries}: {query_to_process}")
        
        # Reset flag
        st.session_state.process_query = False
        
        with st.spinner("🤖 Agent team is analyzing your query..."):
            try:
                # Initialize agents
                logger.info("Initializing agent team...")
                agent_team = initialize_agents()
                
                if agent_team:
                    # Display query
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    st.markdown(f'<div class="query-box"><strong>📝 Query:</strong> {query_to_process}<br><small>⏰ {timestamp}</small></div>', unsafe_allow_html=True)
                    
                    st.markdown("**🤖 Agent Response:**")
                    
                    # Get response with error handling
                    logger.info("Processing query through agent team...")
                    full_response = process_agent_query(agent_team, query_to_process)
                    logger.info(f"Response received: {len(full_response)} characters")
                    
                    # Display response
                    st.markdown(f'<div class="agent-response">', unsafe_allow_html=True)
                    st.markdown(full_response)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "query": query_to_process,
                        "response": full_response,
                        "timestamp": timestamp
                    })
                    logger.info("Query added to chat history")
                    
                    st.success("✅ Analysis complete!")
                    
                else:
                    logger.error("Agent team initialization failed")
                    st.error("❌ Failed to initialize agent team. Check logs for details.")
                    
            except Exception as e:
                logger.error(f"Error processing query: {str(e)}", exc_info=True)
                st.error(f"❌ Error: {str(e)}")
                
                if "tool_use_failed" in str(e):
                    st.warning("⚠️ The web search tool encountered an issue. The agents will try to provide information from their knowledge base.")
                
                st.info("💡 **Troubleshooting Tips:**")
                st.markdown("""
                - Try rephrasing your query more simply
                - Check your GROQ_API_KEY in .env file
                - Verify internet connection
                - Try asking about a single topic instead of multiple topics
                """)

def render_chat_history():
    """Render chat history section"""
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("## 📜 Analysis History")
        
        for idx, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"💬 Query {len(st.session_state.chat_history) - idx}: {chat['query'][:60]}... ({chat['timestamp']})"):
                st.markdown(f"**📝 Query:** {chat['query']}")
                st.markdown(f"**⏰ Timestamp:** {chat['timestamp']}")
                st.markdown("**🤖 Response:**")
                st.markdown(f'<div class="agent-response">', unsafe_allow_html=True)
                st.markdown(chat["response"])
                st.markdown('</div>', unsafe_allow_html=True)

def render_footer():
    """Render footer section"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <p><strong>🚀 Technology Stack</strong></p>
        <p>
            <b>Framework:</b> Streamlit | 
            <b>AI:</b> Phi Agent | 
            <b>LLM:</b> Groq (LLaMA 3.3 70B)
        </p>
        <p style='margin-top: 15px;'>
            <b>Agents:</b> Web Agent + Finance Agent + Team Coordinator
        </p>
        <p style='margin-top: 20px; font-size: 0.9rem;'>
            💡 Multi-Agent AI System for Comprehensive Analysis<br>
            
        </p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    render_sidebar()
    
    st.title("🤖 AI Finance Agent")
    st.markdown("Powered by Web Agent + Finance Agent working together")
    
    render_quick_actions()
    st.markdown("---")
    render_query_input()
    
    process_query()
    render_chat_history()
    render_footer()

if __name__ == "__main__":
    try:
        logger.info("Starting Multi-Agent AI System application")
        main()
    except Exception as e:
        logger.critical(f"Critical error in main application: {str(e)}", exc_info=True)
        st.error(f"❌ Critical Error: {str(e)}")
