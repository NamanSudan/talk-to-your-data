SQL_GENERATION_TEMPLATE = """
Given the following user query and conversation history, generate a SQL query that answers the question.
The query should be compatible with SQLite syntax.

User Query: {query}

Conversation History:
{history}

Schema Information:
{schema}

Generate only the SQL query without any additional text or explanation.
"""

RESPONSE_GENERATION_TEMPLATE = """
Given the user's question, the SQL query used, and the results, provide a natural language response
that explains the findings in a clear and concise way.

Question: {question}
SQL Query: {sql}
Results: {results}

Response should be informative and friendly, highlighting key insights from the data.
"""
