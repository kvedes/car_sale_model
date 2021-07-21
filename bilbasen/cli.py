from datetime import datetime
import os
import typer
from bilbasen.scrape import driver

app = typer.Typer()
@app.command()
def scrape(brand: str, model: str, output_dir: str="~/data"):
    
    typer.echo(f"Scraping cars of brand {brand} and model {model}")
    typer.echo(f"Using output path: {output_dir}")
    output_dir = os.path.expanduser(output_dir)

    timestamp = datetime.now().strftime("%Y-%b-%d-%H-%M-%S")
    driver(brand, model, timestamp, output_dir)

if __name__ == "__main__":
    app()
