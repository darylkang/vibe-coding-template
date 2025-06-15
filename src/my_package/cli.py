"""
Simple CLI interface using Typer.

This module demonstrates basic CLI patterns for modern Python applications.
"""

from __future__ import annotations

from typing import Annotated

import typer

from my_package.core import MyPackage

# Create the Typer app
app = typer.Typer(
    name="vibe",
    help="Modern Python development made easy with TDD enforcement.",
)


def version_callback(value: bool) -> None:
    """Print version information and exit."""
    if value:
        from my_package import __version__

        print(f"vibe version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option("--version", "-v", callback=version_callback, help="Show version"),
    ] = False,
) -> None:
    """Vibe Coding Template - Test-driven Python development made easy."""


@app.command()
def process(
    text: str,
    transform: Annotated[str, typer.Option("--transform", "-t")] = "uppercase",
) -> None:
    """Process text with the specified transformation."""
    try:
        package = MyPackage()
        result = package.process(text, transform)

        if result.success:
            print(result.output_data)
        else:
            print(f"Error: {result.metadata.get('error', 'Unknown error')}")
            raise typer.Exit(code=1)

    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def info() -> None:
    """Show package information."""
    package = MyPackage()
    stats = package.get_stats()

    from my_package import __version__

    print("Package Information:")
    print(f"  Version: {__version__}")
    print(f"  Debug Mode: {stats['settings']['debug']}")
    print(f"  Default Transform: {stats['settings']['default_transform']}")


if __name__ == "__main__":
    app()
