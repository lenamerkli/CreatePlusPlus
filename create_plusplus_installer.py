#!/usr/bin/env python3

from random import randint
from os import getpid, getlogin
from os.path import dirname
from platform import system as platform_system
from rich.console import Console
from sys import exit
from json import load as json_load, dump as json_dump, JSONDecodeError
from pathlib import Path


VERSION = '1.0.0'
CONSOLE = Console()
HEADING = """ $$$$$$\\                                 $$\\                                   
$$  __$$\\                                $$ |                 $$\\       $$\\    
$$ /  \\__| $$$$$$\\   $$$$$$\\   $$$$$$\\ $$$$$$\\    $$$$$$\\     $$ |      $$ |   
$$ |      $$  __$$\\ $$  __$$\\  \\____$$\\\\_$$  _|  $$  __$$\\ $$$$$$$$\\ $$$$$$$$\\ 
$$ |      $$ |  \\__|$$$$$$$$ | $$$$$$$ | $$ |    $$$$$$$$ |\\__$$  __|\\__$$  __|
$$ |  $$\\ $$ |      $$   ____|$$  __$$ | $$ |$$\\ $$   ____|   $$ |      $$ |   
\\$$$$$$  |$$ |      \\$$$$$$$\\ \\$$$$$$$ | \\$$$$  |\\$$$$$$$\\    \\__|      \\__|   
 \\______/ \\__|       \\_______| \\_______|  \\____/  \\_______|                    """
DEFAULT_CONFIG = {

}


def raise_error(message: str) -> None:
    CONSOLE.print(f"[red bold]Beim Ausführen des Create++ Installers ist ein Fehler aufgetreten.[/]")
    CONSOLE.print(f"[red bold]{message}[/]")
    exit(1)
    return None


def get_os() -> str:
    """
    Get the operating system
    :return: Either `Linux`, `macOS` or `Windows`
    """
    system = platform_system()
    if system not in ['Linux', 'Darwin', 'Windows']:
        raise_error(f"Nicht unterstütztes Betriebssystem: `{system}`")
    return system.replace('Darwin', 'macOS')


def get_config(os: str) -> str:
    """
    Get the path to the permanent user configuration file
    :param os: The name of the operating system
    :return: the absolute file path
    """
    if os == 'Linux':
        return f"/home/{getlogin()}/.config/create_plusplus/installer.json"
    elif os == 'macOS':
        return f"/Users/{getlogin()}/Library/Application Support/create_plusplus/installer.json"
    elif os == 'Windows':
        return f"C:\\Users\\{getlogin()}\\AppData\\Local\\create_plusplus\\installer.json"
    raise_error(f"Nicht unterstütztes Betriebssystem: `{os}`")
    return ''


def read_config(os: str) -> dict:
    try:
        with open(get_config(os), 'r') as file:
            contents = json_load(file)
    except (FileNotFoundError, JSONDecodeError):
        contents = DEFAULT_CONFIG
    return contents


def write_config(os: str, config: dict) -> None:
    config_file = get_config(os)
    Path(dirname(config_file)).mkdir(parents=True, exist_ok=True)
    with open(get_config(os), 'w') as file:
        json_dump(config, file)  # type: ignore[arg-type]
    return None



def get_temp(os: str) -> str:
    if os == 'Linux' or os == 'Darwin':
        return f"/tmp/create_installer/{getpid()}_{randint(10 ** 6, 10 ** 7)}/"
    elif os == 'Windows':
        return f"C:\\Users\\{getlogin()}\\AppData\\Local\\Temp\\create_installer\\{getpid()}_{randint(10 ** 6, 10 ** 7)}\\"
    CONSOLE.print(f"[red bold]Nicht unterstütztes Betriebssystem: `{os}`[/]")
    exit(1)
    return ''


def select(options: list[str]) -> int:
    CONSOLE.print(f"[purple]{'-' * 8}[/] [purple bold]Wählen Sie eine Option:[/] [purple]{'-' * 8}[/]")
    for i, option in enumerate(options):
        CONSOLE.print(f"[purple bold]{i + 1}[/]: {option}")
    CONSOLE.print(f"Oder [purple bold]c[/] um abzubrechen.")
    loop = True
    choice = -1
    while loop:
        try:
            choice = input("Wählen Sie eine Option: ")
            if choice == 'c':
                CONSOLE.print("[red bold]Der Create++ Installer wird beendet.[/]")
                exit(0)
                choice = -1
            choice = int(choice)
            if choice < 0 or choice >= len(options):
                CONSOLE.print("[red bold]Ungültige Auswahl. Bitte versuchen Sie es erneut.[/]")
                continue
            loop = False
        except ValueError:
            CONSOLE.print("[red bold]Ungültige Eingabe. Bitte versuchen Sie es erneut.[/]")
    return choice



def print_table(table: list[list[str]]) -> None:
    """
    Print the table in the following format, cells are left aligned:
    +-------+-------+-------+
    | cell1 | cell2 | cell3 |
    | cell4 | cell5 | cell6 |
    +-------+-------+-------+
    If the first element of a row is `----`, the row will be replaced with a horizontal line which include the plus signs.
    The minimum width of a cell is 4, including the padding.
    :param table: A 2D list of strings
    :return: None
    """
    widths = [2] * max(len(row) for row in table)  # without the padding (4 - 2 = 2)
    for row in table:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    def format_row(row_: list[str], widths_: list[int]) -> str:
        return '[blue bold]|[/] ' + ' [blue bold]|[/] '.join(cell_.ljust(widths_[i_]) for i_, cell_ in enumerate(row_)) + ' [blue bold]|[/]'

    def print_separator(widths_: list[int]) -> str:
        return '[blue bold]+-[/]' + '[blue bold]-+-[/]'.join(f"[blue bold]{'-' * width_}[/]" for width_ in widths_) + '[blue bold]-+[/]'

    CONSOLE.print(print_separator(widths))
    for row in table:
        if row[0] == "----":
            CONSOLE.print(print_separator(widths))
        else:
            CONSOLE.print(format_row(row, widths))
    CONSOLE.print(print_separator(widths))
    return None


def detect_specific_user(config: dict) -> str:
    # NOT IMPLEMENTED
    if 'username' in config and len(config['username']) > 0:
        return config['username']
    return 'anonym'


def main() -> None:
    os = get_os()
    config = read_config(os)
    config_path = get_config(os)
    temp = get_temp(os)
    user = detect_specific_user(config)
    CONSOLE.print(f"[green bold]{HEADING}[/]\n")
    print_table([
        ['Installer Version', VERSION],
        ['Betriebssystem', os],
        ['Benutzer', user],
        ['Temporäres Verzeichnis', temp],
        ['Einstellungsdatei', config_path],
    ])
    choice_1 = select([
        'Create++ mit Unterstützung installieren',
        'Create++ mit Unterstützung aktualisieren',
        'Benutzer setzen',
        'Dateien extrahieren',
        'Create++ Installer deinstallieren',
    ])



if __name__ == '__main__':
    main()
