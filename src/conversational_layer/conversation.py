from dataclasses import dataclass
from typing import List, Optional
from vanna_integration.vanna_wrapper import VannaWrapper
from vllm_integration.vllm_client import VLLMClient
from visualizations.plot_results import create_visualization
import pandas as pd

@dataclass
class Message:
    role: str
    content: str

class ConversationManager:
    def __init__(self):
        self.history: List[Message] = []
        self.vanna = VannaWrapper()
        self.vllm = VLLMClient()
        self.logger = logging.getLogger(__name__) # Added logger for debugging

    def add_message(self, role: str, content: str):
        self.history.append(Message(role=role, content=content))

    def process_query(self, user_query: str) -> tuple[str, Optional[pd.DataFrame], Optional[str]]:
        """
        Process a natural language query and return the response, results, and visualization
        """
        self.add_message("user", user_query)
        
        try:
            # Generate SQL from natural language query
            sql = self.vanna.generate_sql(user_query, self.history)
            self.logger.info(f"Generated SQL: {sql}")
            # Execute the generated SQL
            results = self.vanna.execute_sql(sql)
            
            # Create simple response
            if results is not None and not results.empty:
                response = f"Query executed successfully. Found {len(results)} results."
            else:
                response = "No results found or there was an error executing the query."
            
            # Create visualization if appropriate
            viz = None
            if results is not None and not results.empty:
                viz = create_visualization(results, user_query)
            
            self.add_message("assistant", response)
            return response, results, viz
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            self.add_message("assistant", error_msg)
            return error_msg, None, None

    def clear_history(self):
        self.history.clear()

import logging
logging.basicConfig(level=logging.INFO)