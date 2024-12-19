import sys
import os
import streamlit as st
import logging

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conversational_layer.conversation import ConversationManager
from database.db_utils import init_database

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize session state and database
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
try:
    if 'initialized' not in st.session_state:
        init_database()
        st.session_state.initialized = True
except Exception as e:
    st.error(f"Failed to initialize database: {str(e)}")
    st.stop()

def main():
    if 'conversation_manager' not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()

    # Sidebar with example queries
    with st.sidebar:
        st.title("📝 Example Queries")
        example_queries = [
            "Show me all users",
            "Count total number of orders",
            "Show total amount spent by each user",
            "List users who made orders in the last month",
            "Find users with orders over $100",
            "Show average order amount per user"
        ]
        
        for query in example_queries:
            if st.button(query):
                st.session_state.current_query = query
                st.rerun()

    st.title("💬 Natural Language Data Query System")
    st.write("Ask questions about your data in natural language!")

    # Main query input with keyboard shortcut
    current_query = st.text_area(
        "Enter your question: (Press Cmd/Ctrl+Enter to execute)",
        value=getattr(st.session_state, 'current_query', "Show me all users"),
        height=100,
        key="query_input",
        on_change=lambda: exec('if "query_input" in st.session_state and st.session_state.query_input != getattr(st.session_state, "current_query", ""): st.session_state.current_query = st.session_state.query_input; st.session_state.execute_query = True')
    )
    
    if 'execute_query' not in st.session_state:
        st.session_state.execute_query = False
    
    col1, col2 = st.columns([1, 4])
    with col1:
        execute_button = st.button("Ask Question", type="primary")
    with col2:
        clear_button = st.button("Clear History")
    
    if clear_button:
        st.session_state.chat_history = []
        st.session_state.conversation_manager.clear_history()
        st.rerun()
    
    if execute_button or st.session_state.execute_query:
        st.session_state.execute_query = False
        # Process query through conversation manager
        response, results, viz = st.session_state.conversation_manager.process_query(current_query)
        
        # Add to chat history
        st.session_state.chat_history.append(("user", current_query))
        st.session_state.chat_history.append(("assistant", response))
        
        if results is not None and not results.empty:
            st.dataframe(results, use_container_width=True)
            
            # Generate visualization if available
            if viz:
                st.plotly_chart(viz)
    
    # Display chat history
    st.divider()
    st.subheader("Chat History")
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(message)

if __name__ == "__main__":
    main()