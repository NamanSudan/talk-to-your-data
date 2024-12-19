from ui.cli_interface import CLIInterface
from database.setup_db import initialize_database
from rich.console import Console
from rich.traceback import install

def main():
    # Install rich traceback handler
    install(show_locals=True)
    console = Console()

    try:
        # Initialize database
        initialize_database()
        
        # Start CLI interface
        cli = CLIInterface()
        cli.start()
    except Exception as e:
        console.print_exception()
        console.print("[red]Application terminated due to error[/red]")

if __name__ == "__main__":
    main()
