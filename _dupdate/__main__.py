import click
import requests
from pathlib import Path
from github.releases import getRelease

@click.group()
def cli():
    pass

@cli.command(short_help='Installs the latest version of apktool')
def apktool():
    """Installs the latest version of apktool in the bin/apktool folder"""
    click.echo('Requesting latest release...')
    release = getRelease('ibotpeaches', 'apktool', 'latest')
    click.echo(f'Found \'{release.name}\', starting download')
    jar = requests.get(release.assets[0].browser_download_url)
    click.echo('Successfully downloaded, writing to file')
    with open("bin/apktool.jar","wb") as jarFile:
        jarFile.write(jar.content)
    click.echo('Succesfully installed to bin/apktool/apktool.jar, you can now simply use the alias dapktool to access apktool everywhere')

if __name__ == '__main__':
    cli()