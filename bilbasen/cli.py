from datetime import datetime
import typer
from bilbasen.scrape import driver

app = typer.Typer()
@app.command()
def scrape(brand: str, model: str):
    print(brand, model)
    timestamp = datetime.now().strftime("%Y-%b-%d-%H-%M-%S")
    driver(brand, model, timestamp)
    #typer.echo(f"Hello {name}")


if __name__ == "__main__":
    app()
