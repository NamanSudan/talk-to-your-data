# Talk to Your Data

A conversational interface that allows users to query and visualize data using natural language. Built with Vanna for Text-to-SQL conversion and vLLM for efficient LLM inference.

## Features

- Natural language to SQL conversion using Vanna.
- Interactive chat-like interface
- Data visualization capabilities
- High-performance LLM inference with vLLM. This is not yet implemented.
- Support for multiple database types
- Example queries for quick start

## Need to do:
- Swap out sqlite for clickhouse
- Add vLLM inference

## Prerequisites

- Python 3.11+
- Poetry (recommended) or pip
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/talk-to-your-data.git
cd talk-to-your-data
```

2. Create and activate a virtual environment:

**On macOS/Linux:**
```bash
# Install Python 3.11 if not already installed
# On macOS using brew:
brew install python@3.11

# Create venv
python3.11 -m venv venv

# Activate venv
source venv/bin/activate
```

**On Windows:**
```bash
# Install Python 3.11 from python.org if not already installed

# Create venv
python3.11 -m venv venv

# Activate venv
.\venv\Scripts\activate
```

3. Upgrade pip and install dependencies:
```bash
# Upgrade pip
python3.11 -m pip install --upgrade pip

# Install dependencies using Poetry (recommended)
pip install poetry
poetry install

# OR using pip
pip install -r requirements.txt
```

## Quick Start

1. Initialize the database:
```bash
python3.11 src/database/setup_db.py
```

2. Launch the Streamlit interface:
```bash
python3.11 -m streamlit run src/streamlit_app.py
```

3. Open your browser and navigate to the displayed URL (typically http://localhost:8501)

## Usage

The web interface provides:
- Text input for natural language queries
- Example queries in the sidebar
- Interactive visualization of results
- Query history

Reference to example queries in code:
```python:src/streamlit_app.py
startLine: 32
endLine: 39
```

## Project Structure

For detailed project structure, see:
```markdown:directory_structure.md
startLine: 1
endLine: 62
```

## Technical Details

For complete technical documentation and architecture details, see:
```markdown:design_doc.md
startLine: 42
endLine: 75
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing

Run the test suite:
```bash
poetry run pytest

# OR if using pip
pytest
```

## Troubleshooting

1. **Python version issues:**
   - Verify Python version: `python --version`
   - Ensure you're using Python 3.11: `python3.11 --version`

2. **Virtual environment issues:**
   - Make sure venv is activated (you should see `(venv)` in your terminal)
   - On Windows, if activation fails, try: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

3. **Package installation issues:**
   - Try upgrading pip again: `python -m pip install --upgrade pip`
   - If a package fails to install, try installing it individually

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Vanna.ai](https://vanna.ai/) for Text-to-SQL conversion
- [vLLM](https://vllm.ai/) for efficient LLM inference
- All contributors and maintainers

---
Built by Naman Sudan
```
