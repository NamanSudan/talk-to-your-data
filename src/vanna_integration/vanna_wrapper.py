
import pandas as pd
import sqlite3
import logging
from vanna.remote import VannaDefault
from .schema_definition import get_schema_definition
from vllm_integration.vllm_client import VLLMClient
from conversational_layer.prompt_templates import SQL_GENERATION_TEMPLATE

class VannaWrapper:
    def __init__(self):
        self.schema = get_schema_definition()
        self.connection = None
        self.vanna = None
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        self.initialize_vanna()

    def initialize_vanna(self):
        """Initialize Vanna with configuration and schema"""
        try:
            self.logger.info("Initializing Vanna...")
            
            # Initialize with your specific model and API key
            api_key = 'ec06a61c6fde4d6a9fb0208f51f6a222'
            model_name = 'thepunisher'
            
            self.vanna = VannaDefault(model=model_name, api_key=api_key)
            self.vanna.train(ddl=self.schema)
            self.logger.info("Vanna initialized successfully with model %s", model_name)
        except Exception as e:
            self.logger.error(f"Failed to initialize Vanna: {e}")
            raise

    def get_connection(self):
        """Get SQLite connection"""
        if not self.connection:
            try:
                self.connection = sqlite3.connect('data.db')
                self.connection.execute('PRAGMA foreign_keys = ON')
            except sqlite3.Error as e:
                self.logger.error(f"Database connection error: {e}")
                raise
        return self.connection

    def generate_sql(self, query: str, conversation_history: list) -> str:
        """Generate SQL from natural language using Vanna"""
        try:
            self.logger.info(f"Processing query: {query}")
            if not self.vanna:
                self.logger.warning("Vanna not initialized, attempting to initialize...")
                self.initialize_vanna()
            
            self.logger.debug(f"Context: {len(conversation_history)} messages in history")
            sql = self.vanna.generate_sql(query)
            
            if not sql:
                raise ValueError("Generated SQL is empty")
                
            self.logger.info(f"Generated SQL: {sql}")
            return sql.strip("'").strip('"')  # Remove any quotes from the SQL
        except Exception as e:
            self.logger.error(f"Error generating SQL: {e}")
            raise

    def execute_sql(self, sql_query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        try:
            conn = self.get_connection()
            self.logger.info(f"Executing SQL: {sql_query}")
            return pd.read_sql_query(sql_query, conn)
        except Exception as e:
            self.logger.error(f"Error executing SQL: {e}")
            raise
