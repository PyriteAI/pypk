import subprocess  # nosec
from pathlib import Path

from . import _contents


def create(
    package: Path,
    author: str,
    author_email: str,
    python_version: str,
    init_git: bool = True,
) -> None:
    srcdir = package.name.replace("-", "_")

    package.mkdir(parents=True, exist_ok=True)
    package.joinpath("src", srcdir).mkdir(parents=True, exist_ok=True)
    package.joinpath("requirements").mkdir(exist_ok=True)
    with package.joinpath(".flake8").open("w") as f:
        f.write(_contents.FLAKE8)
    with package.joinpath(".gitignore").open("w") as f:
        f.write(_contents.GITIGNORE)
    with package.joinpath(".pre-commit-config.yaml").open("w") as f:
        f.write(_contents.PRECOMMIT.format(package_name=package.name))
    with package.joinpath("pyproject.toml").open("w") as f:
        target_version = f"py{''.join(python_version.split('.')[:2])}"
        f.write(_contents.PYPROJECT.format(package_name=package.name, target_version=target_version))
    with package.joinpath("README.md").open("w") as f:
        f.write(_contents.README.format(package_name=package.name))
    with package.joinpath("setup.py").open("w") as f:
        f.write(
            _contents.SETUP.format(
                package_name=package.name, author=author, author_email=author_email, python_version=python_version
            )
        )
    package.joinpath("requirements", "requirements.in").touch(exist_ok=True)
    with package.joinpath("requirements", "dev-requirements.in").open("w") as f:
        f.write(_contents.DEVREQUIREMENTS)
    package.joinpath("src", srcdir, "__init__.py").touch(exist_ok=True)
    if init_git:
        subprocess.run(["git", "init"], cwd=package)  # nosec


__all__ = ["create"]
