import click

__version__ = '0.0.1'

@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
def one():
    click.echo('One')


@cli.command(help='Command Two')
def two():
    click.echo('Two')
