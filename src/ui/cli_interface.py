from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.table import Table
from conversational_layer.conversation import ConversationManager
import pandas as pd

class CLIInterface:
    def __init__(self):
        self.console = Console()
        self.conversation = ConversationManager()

    def display_welcome(self):
        welcome_message = """
        🤖 Welcome to the Conversational Data Assistant!
        
        You can ask questions about your data in natural language.
        Type 'exit' to quit or 'clear' to start a new conversation.
        """
        self.console.print(Panel(welcome_message, title="Welcome", border_style="blue"))

    def display_results(self, results: pd.DataFrame):
        if results is None or results.empty:
            self.console.print("[yellow]No results found[/yellow]")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        for col in results.columns:
            table.add_column(str(col))
        
        for _, row in results.iterrows():
            table.add_row(*[str(x) for x in row])
        
        self.console.print(table)

    def display_sql(self, sql: str):
        syntax = Syntax(sql, "sql", theme="monokai", line_numbers=True)
        self.console.print(Panel(syntax, title="Generated SQL", border_style="green"))

    def start(self):
        self.display_welcome()
        
        while True:
            try:
                user_input = self.console.input("[bold blue]You:[/bold blue] ")
                
                if user_input.lower() == 'exit':
                    self.console.print("[yellow]Goodbye![/yellow]")
                    break
                
                if user_input.lower() == 'clear':
                    self.conversation.clear_history()
                    self.console.clear()
                    self.display_welcome()
                    continue
                
                self.console.print("\n[bold green]Processing...[/bold green]")
                
                response, results, viz = self.conversation.process_query(user_input)
                
                self.console.print("\n[bold purple]Assistant:[/bold purple]", response)
                
                if results is not None:
                    self.display_results(results)
                
                if viz:
                    self.console.print("\n[bold blue]Visualization available![/bold blue]")
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Session terminated by user[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")
