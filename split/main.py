from .split import *
import click

@click.command()
@click.argument('filename', type=str, required=True)
def split_pdf(filename: str) -> None:
    input_file = filename
    split_pdf_into_chapters(input_file)

    