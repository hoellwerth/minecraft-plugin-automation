#!/usr/bin/python3
import os as os
import json
import typer
from typing_extensions import Annotated
from typing import Optional
import subprocess

app = typer.Typer()

configurationFile = open('config.json')
config = json.load(configurationFile)
configurationFile.close()

working_path = config['path']

def checkConfig(config):
    # Check current forconfiguration
    if not os.path.isfile(config['path'] + 'pom.xml'):
        print('\033[91m' + '\033[1m' + 'Path is not valid!' + '\033[0m')

        return False

    if config['server']['local']:
        if not os.path.isdir(config['server']['serverPath'] + 'plugins'):
            print('\033[91m' + '\033[1m' + 'Local server path is not valid!' + '\033[0m')
            
            return False
        
    return True

@app.command()
def configure(
    path: Annotated[Optional[str], typer.Option()] = working_path,
    local: Annotated[Optional[bool], typer.Option()] = config['server']['local'],
    serverPath: Annotated[Optional[str], typer.Option()] = config['server']['serverPath'],
    adress: Annotated[Optional[str], typer.Option()] = config['server']['adress'],
    port: Annotated[Optional[int], typer.Option()] = config['server']['port'],
    username: Annotated[Optional[str], typer.Option()] = config['server']['username'],
    password: Annotated[Optional[str], typer.Option()] = config['server']['password']):

    file = open('config.json')
    if checkConfig(json.load(file)):
        writeFile = open('config.json', 'w')
        writeFile.write(json.dumps({
        "path": path,
        "server": {
            "local": local,
            "serverPath": serverPath,
            "adress": adress,
            "port": port,
            "username": username,
            "password": password
        }}))
        writeFile.close()

        print('\033[92m' + '\033[1m' + 'Saved configuration' + '\033[0m')
    
    file.close()

@app.command()
def start():
    subprocess.run(["systemctl", "start", 'minecraft-auto'])

    typer.echo('\033[92m' + 'Runner has started' + '\033[0m')

@app.command()
def stop():
    subprocess.run(["systemctl", "stop", 'minecraft-auto'])

    typer.echo('\033[93m' + 'Runner has stopped' + '\033[0m')

if __name__ == '__main__':
    app()