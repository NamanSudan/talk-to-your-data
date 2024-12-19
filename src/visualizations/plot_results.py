
from typing import Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_visualization(df: pd.DataFrame, query: str) -> Optional[go.Figure]:
    """
    Create appropriate visualization based on data and query context
    Returns a Plotly figure object
    """
    if df.empty or len(df.columns) < 2:
        return None

    query = query.lower()
    try:
        # Aggregation/Summary visualizations
        if any(word in query for word in ['total', 'sum', 'amount', 'spent']):
            if len(df) <= 10:  # For smaller datasets
                return px.bar(df, x=df.columns[0], y=df.columns[-1], title='Total/Sum Analysis')
            return px.pie(df, values=df.columns[-1], names=df.columns[0], title='Distribution Analysis')

        # Time series analysis
        if any(word in query for word in ['time', 'date', 'when', 'period']):
            date_col = df.select_dtypes(include=['datetime64']).columns
            if len(date_col) > 0:
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
                if len(numeric_cols) > 0:
                    return px.line(df, x=date_col[0], y=numeric_cols[0], title='Time Series Analysis')

        # Comparison visualizations
        if any(word in query for word in ['compare', 'difference', 'versus', 'vs']):
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) >= 2:
                return px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title='Comparison Analysis')

        # Default visualization based on data types
        if len(df) <= 10:  # Small dataset
            numeric_col = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_col) > 0:
                return px.bar(df, x=df.index, y=numeric_col[0], title='Summary View')

        # Fallback for larger datasets
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) >= 2:
            return px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title='Data Overview')

    except Exception as e:
        print(f"Error creating visualization: {e}")
        return None

    return None
