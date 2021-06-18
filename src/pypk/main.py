import sys
from pathlib import Path
from typing import NoReturn

import typer

from . import core
from .config import load_custom_config, try_load_default_config
from .version import version as pypk_version

_CURRENT_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}.0"

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
    python_version: str = typer.Option(  # noqa: B008
        _CURRENT_VERSION, "--py-version", "-p", help="Minimum Python version supported"
    ),
    init_git: bool = typer.Option(True, "--init-git/--skip-git-init", help="Toggle Git initialization"),  # noqa: B008
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
    python_version = python_version if python_version else cfg.get("py_version")

    if author is None:
        exit_with_status("[Error] 'author' must be specified in either the config or via command line")
    if email is None:
        exit_with_status("[Error] 'email' must be specified in either the config or via command line")
    if version is None:
        exit_with_status("[Error] 'version' must be specified in either the config or via command line")

    core.create(package, author, email, python_version, init_git=init_git)


@app.command()
def version():
    typer.echo(pypk_version)


__all__ = ["app"]
