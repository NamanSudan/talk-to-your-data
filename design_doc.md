---

## Project Title: Conversational Data Interaction POC

### Document Version

- **Version:** 1.0
- **Date:** December 18, 2024
- **Author:** Naman Sudan

### Executive Summary

This project implements a conversational interface that allows users to query and visualize data using natural language. Users interact in a chat-like environment, pose questions about underlying datasets, and receive answers or visualizations. Behind the scenes, the system uses a Large Language Model (LLM) to convert user queries into SQL statements and execute them against a relational database. We leverage:

- **Vanna** for Text-to-SQL conversion and SQL execution orchestration.
- **vLLM** as an efficient inference engine for open-source LLM models (e.g., Mistral or LLaMA).
- A database (e.g., SQLite) as the data source.

The end goal is a minimal but functional POC that can be extended into a production-grade system with additional optimizations.

---

## Goals and Non-Goals

**Goals:**

1. Provide a chat-like interface where users can ask natural language questions.
2. Automatically translate user queries into SQL using an LLM.
3. Execute SQL queries against a known relational database schema.
4. Return and display results to the user, optionally including a basic visualization.
5. Demonstrate the feasibility and performance of using vLLM and Vanna together.

**Non-Goals:**

- Production-level security, authentication, and authorization.
- Handling highly complex SQL queries or large, complex databases.
- Advanced error handling and self-correction of malformed queries beyond basic POC handling.
- Full integration into enterprise environments or deployment pipelines.

---

## Architecture Overview

**High-Level Architecture:**

```
          ┌──────────────────┐           ┌───────────────────┐
          │                  │  user Q   │                   │
          │   User Interface │──────────▶│ Conversational    │
          │  (CLI/Web UI)    │  user A   │  Layer (Wrapper)  │
          │                  │◀──────────│                   │
          └─────▲───────────┘           └───────────────────┘
                │
                │ user Q
                │
          ┌─────▼──────────┐
          │                │
          │   Vanna        │───▶ SQL Query
          │(Text-to-SQL)   │
          └─────▲─────────┘
                │ LLM Prompt
                │ & Response
          ┌─────▼────────────────┐
          │                      │
          │        vLLM          │───▶ LLM inference (Mistral/LLaMA)
          │   (Model Backend)    │
          └─────▲────────────────┘
                │ SQL results
          ┌─────▼─────────┐
          │                │
          │   Database     │───▶ Actual data execution
          │(SQLite, etc.) │
          └───────────────┘

```

**Data Flow Overview:**

1. User inputs a natural language query (e.g., "What were total sales by region in 2021?").
2. The query is passed to Vanna, which generates a prompt for the LLM.
3. The prompt is sent to the vLLM inference server running the chosen LLM model.
4. The LLM returns a SQL query string.
5. Vanna executes the SQL query against the database.
6. Results are returned to the user and optionally visualized.

---

## Components and Responsibilities

1. **User Interface (UI):**
    - Can be a CLI prompt, web-based UI (Streamlit, Gradio), or a command-line loop.
    - Collects user queries and displays answers and visualizations.
2. **Conversational Layer (Integration Wrapper):**
    - Orchestrates the flow between user queries and Vanna.
    - May provide additional context or instructions to the LLM.
3. **Vanna (Text-to-SQL):**
    - Responsible for taking a user’s natural language request, preparing a prompt, and sending it to the LLM.
    - Interprets the LLM response as SQL.
    - Executes the SQL on the target database.
    - Returns results to the UI.
4. **vLLM (LLM Inference Engine):**
    - Hosts a selected model (e.g., Mistral or LLaMA).
    - Receives prompts and returns generated text.
    - Offers low-latency, efficient inference serving.
5. **Database Layer:**
    - A relational database (e.g., SQLite) with defined schema and sample data.
    - Executes SQL queries from Vanna.

---

## Technology Stack

- **Programming Language:** Python 3.9+
- **LLM Inference Engine:** vLLM
    - Model: Mistral or LLaMA 2 (7B/13B), locally hosted.
- **Text-to-SQL Orchestration:** Vanna (from GitHub: [vanna-ai/vanna](https://github.com/vanna-ai/vanna))
- **Database:** SQLite (for POC simplicity)
- **Visualization (Optional):** Plotly for basic charts.
- **UI Framework (Optional):**
    - CLI via `input()` and `print()`
    - Potential upgrade to Streamlit or Gradio for a richer interface.

---

## Data Flow & Sequence

**Detailed Steps:**

1. **Initialization:**
    - Load the database schema into Vanna.
    - Start vLLM server with Mistral or LLaMA model.
    - Initialize Vanna with a custom LLM backend that calls the vLLM endpoint.
2. **Processing a User Query:**
    - User: "What were the total sales by region in 2021?"
    - System (Vanna): Takes the query, formats a prompt including schema details.
    - System (Vanna → vLLM): Sends the prompt to vLLM.
    - vLLM: Generates a SQL query, e.g., `SELECT region, SUM(sales_amount) FROM sales WHERE sales_date BETWEEN '2021-01-01' AND '2021-12-31' GROUP BY region;`
    - Vanna executes the SQL on the SQLite database.
    - Returns results to the UI.
3. **Results Display:**
    - The UI prints the results in a table format.
    - Optionally generate a bar chart if the user desires visualization.

---

## Prompting and Few-Shot Examples

To improve accuracy, we might provide a prompt template to Vanna that guides the LLM, including a few-shot set of examples. For instance:

```
"You are a helpful SQL assistant. The database schema is: sales(region TEXT, product TEXT, sales_amount FLOAT, sales_date DATE).
Generate SQL queries that accurately reflect the user's request.

Example:
User: 'What is the total sales by product last year?'
SQL: SELECT product, SUM(sales_amount) FROM sales WHERE sales_date BETWEEN '2023-01-01' AND '2023-12-31' GROUP BY product;

User: {user_query}
SQL:"

```

Vanna can inject the user_query and send this prompt to vLLM.

---

## Performance Considerations

- **Latency:**
    - vLLM is chosen for efficient inference, reducing response time.
    - Caching: The POC may not implement caching, but it’s considered for future iterations.
- **Scalability:**
    - For POC, single-node deployment with a small model (7B).
    - Future: Horizontal scaling of vLLM or a more optimized database.

---

## Error Handling and Logging

- **Error Handling:**
    - If the LLM produces invalid SQL, the code should catch the SQL error and return a helpful message.
    - If vLLM fails or times out, return an error message to the user.
- **Logging:**
    - Basic logging of user queries, generated SQL, and execution results.
    - Debug logs for LLM responses can be stored to refine prompts.

---

## Security Considerations

- For POC, minimal security.
- Future improvements:
    - SQL injection protection or using parameterized queries.
    - Authentication and authorization for users.
    - Proper sandboxing of LLM and database access.

---

## Testing Strategy

- **Unit Tests:**
    - Test the LLM wrapper to ensure prompt/response handling works.
    - Test Vanna’s to_sql and run_sql methods with mock data.
- **Integration Tests:**
    - Test end-to-end from user query → LLM → SQL → DB → results.
- **User Acceptance Tests:**
    - Manually verify that queries return expected results.
    - Adjust prompt strategies if accuracy is low.

---

## Future Enhancements

- Add semantic understanding to handle ambiguous queries.
- Integrate multiple data sources and schemas.
- Implement a richer web-based UI with chat history and suggested queries.
- Introduce caching layers or vector databases for schema retrieval.
- Improve prompt engineering or fine-tune the LLM model specifically for text-to-SQL tasks.

---