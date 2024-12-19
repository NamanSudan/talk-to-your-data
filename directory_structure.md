project-root/
├─ docs/
│  ├─ design-doc.md                # The design document described above
│  ├─ architecture-diagrams/       # Additional diagrams (if any)
│  └─ readme.md                    # High-level project description
│
├─ src/
│  ├─ conversational_layer/        # Integration layer orchestrating UI, Vanna, and vLLM
│  │  ├─ __init__.py
│  │  ├─ conversation.py           # Code handling user queries and responses
│  │  └─ prompt_templates.py       # Prompt templates and few-shot examples
│  │
│  ├─ vanna_integration/           # Code interacting directly with Vanna
│  │  ├─ __init__.py
│  │  ├─ vanna_wrapper.py          # Wrapper to communicate with Vanna’s to_sql and run_sql methods
│  │  └─ schema_definition.py      # Schema details or utilities for schema handling
│  │
│  ├─ vllm_integration/            # Code responsible for talking to the vLLM server
│  │  ├─ __init__.py
│  │  ├─ vllm_client.py            # A client class to send prompts and receive completions from vLLM
│  │  └─ config.py                 # Configuration for vLLM endpoint, tokens, etc.
│  │
│  ├─ database/
│  │  ├─ __init__.py
│  │  ├─ setup_db.py               # Script to initialize/populate the SQLite database
│  │  └─ db_uri.txt                # Stores the database URI or config details
│  │
│  ├─ ui/
│  │  ├─ __init__.py
│  │  ├─ cli_interface.py          # Simple CLI-based user interface
│  │  └─ web_ui.py                 # Placeholder for a future Streamlit or Gradio UI
│  │
│  ├─ visualizations/
│  │  ├─ __init__.py
│  │  ├─ plot_results.py           # Functions for turning query results into charts (plotly, matplotlib)
│  │  └─ helpers.py                # Helper functions for formatting data for visualization
│  │
│  └─ main.py                      # The main entry point that ties everything together
│
├─ models/
│  ├─ README.md                    # Info on which models are placed here
│  └─ (model directories and weights)
│
├─ tests/
│  ├─ unit/
│  │  ├─ test_vanna_integration.py
│  │  ├─ test_vllm_integration.py
│  │  └─ test_conversational_layer.py
│  │
│  ├─ integration/
│  │  ├─ test_end_to_end.py        # Tests user query → LLM → SQL → DB → results
│  │  └─ test_prompt_templates.py
│  │
│  └─ fixtures/                    # Test fixtures, sample data, mock responses
│
├─ scripts/
│  ├─ run_vllm_server.sh           # Script to launch the vLLM server with chosen model
│  └─ run_vanna.sh                 # Script to start Vanna-related services (if needed)
│
├─ requirements.txt                # Python dependencies
└─ README.md                       # High-level overview, how to run POC
