import sys
from pathlib import Path
from typing import NoReturn

import typer

from . import core
from .config import load_custom_config, try_load_default_config

app = typer.Typer()


def exit_with_status(msg: str, code: int = 1) -> NoReturn:
    typer.echo(msg, err=True)
    sys.exit(code)


@app.command()
def create(
    package: Path = typer.Argument(..., help="Path to root package directory"),  # noqa: B008
    config: Path = typer.Option(None, "--config", "-c", help="Path to config file"),  # noqa: B008
    author: str = typer.Option(None, "--author", "-a", help="Author's name"),  # noqa: B008
    email: str = typer.Option(None, "--email", "-e", help="Author's email"),  # noqa: B008
    version: str = typer.Option("3.6.0", "--version", "-v", help="Minimum Python version supported"),  # noqa: B008
) -> None:
    try:
        if config is not None:
            cfg = load_custom_config(config)
        else:
            cfg = try_load_default_config()
    except Exception as e:
        exit_with_status(f"[Error] failed to load config: '{e}'")

    author = author if author else cfg.get("author")
    email = email if email else cfg.get("email")
    version = version if version else cfg.get("version")

    if author is None:
        exit_with_status("[Error] 'author' must be specified in either the config or via command line")
    if email is None:
        exit_with_status("[Error] 'email' must be specified in either the config or via command line")
    if version is None:
        exit_with_status("[Error] 'version' must be specified in either the config or via command line")

    core.create(package, author, email, version)


__all__ = ["app"]