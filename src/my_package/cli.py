"""
Command-line interface using Typer.

This module provides a beautiful, modern CLI using Typer and Rich for
formatting. It demonstrates best practices for CLI design including
proper error handling, progress bars, and user-friendly output.

INSTRUCTIONS FOR CURSOR:
- Add new CLI commands using the @app.command() decorator
- Each command should map to methods in MyPackage or related modules
- Use typer.Option and typer.Argument for parameter handling
- Format output using Rich for better user experience
- Add proper error handling and user feedback
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from my_package.core import MyPackage, ProcessingResult
from my_package.settings import Settings

# Initialize Rich console and Typer app
console = Console()
app = typer.Typer(
    name="vibe",
    help="🚀 Vibe Coding Template - A modern Python CLI template",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """Print version information and exit."""
    if value:
        from my_package import __version__

        console.print(f"vibe version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version", "-v", callback=version_callback, help="Show version and exit"
        ),
    ] = False,
) -> None:
    """🚀 Vibe Coding Template CLI - Modern Python development made easy."""
    pass


@app.command()
def run(
    input_text: Annotated[str, typer.Argument(help="Text to process")],
    transform: Annotated[
        str,
        typer.Option("--transform", "-t", help="Transformation type"),
    ] = "uppercase",
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
    output_file: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Save output to file"),
    ] = None,
) -> None:
    """Process text with the specified transformation."""
    try:
        settings = Settings()
        processor = MyPackage(settings=settings, verbose=verbose)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing...", total=None)
            result = processor.process(input_text, transform)
            progress.update(task, completed=True)

        if result.success:
            # Display result in a nice panel
            console.print(
                Panel(
                    result.output_data,
                    title=f"Result ({transform})",
                    border_style="green",
                )
            )

            # Show metadata if verbose
            if verbose:
                _display_metadata(result.metadata)

            # Save to file if requested
            if output_file:
                output_file.write_text(result.output_data, encoding="utf-8")
                console.print(f"✅ Output saved to {output_file}")

        else:
            console.print(
                f"❌ Processing failed: {result.metadata.get('error', 'Unknown error')}"
            )
            raise typer.Exit(code=1)

    except Exception as e:
        console.print(f"❌ Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def batch(
    input_file: Annotated[Path, typer.Argument(help="Input file with text lines")],
    transform: Annotated[
        str,
        typer.Option("--transform", "-t", help="Transformation type"),
    ] = "uppercase",
    output_file: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Output file for results"),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
) -> None:
    """Process multiple lines from a file in batch mode."""
    try:
        if not input_file.exists():
            console.print(f"❌ Input file not found: {input_file}")
            raise typer.Exit(code=1)

        # Read input lines
        lines = input_file.read_text(encoding="utf-8").strip().split("\n")
        lines = [line.strip() for line in lines if line.strip()]

        if not lines:
            console.print("❌ No valid lines found in input file")
            raise typer.Exit(code=1)

        settings = Settings()
        processor = MyPackage(settings=settings, verbose=verbose)

        with Progress(console=console) as progress:
            task = progress.add_task("Processing batch...", total=len(lines))
            results = processor.batch_process(lines, transform)
            progress.update(task, completed=len(lines))

        # Display results
        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]

        console.print(
            f"✅ Processed {len(successful_results)}/{len(results)} items successfully"
        )

        if failed_results:
            console.print(f"❌ {len(failed_results)} items failed")

        # Save results if requested
        if output_file:
            output_lines = [r.output_data for r in successful_results]
            output_file.write_text("\n".join(output_lines), encoding="utf-8")
            console.print(f"✅ Results saved to {output_file}")

        # Show verbose information
        if verbose:
            _display_batch_summary(results)

    except Exception as e:
        console.print(f"❌ Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def info() -> None:
    """Show package information and statistics."""
    try:
        settings = Settings()
        processor = MyPackage(settings=settings)
        stats = processor.get_stats()

        # Create information table
        table = Table(title="📊 Package Information")
        table.add_column("Setting", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        table.add_row("Version", stats["version"])
        table.add_row("Verbose Mode", str(stats["verbose_mode"]))
        table.add_row("Debug Mode", str(settings.debug))
        table.add_row("Log Level", settings.log_level)
        table.add_row("Data Directory", str(settings.data_dir))
        table.add_row("Output Directory", str(settings.output_dir))
        table.add_row("Default Transform", settings.default_transform)
        table.add_row("Max Batch Size", str(settings.max_batch_size))

        console.print(table)

    except Exception as e:
        console.print(f"❌ Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def transforms() -> None:
    """List available transformation types."""
    transforms_info = [
        ("uppercase", "Convert text to UPPERCASE"),
        ("lowercase", "Convert text to lowercase"),
        ("title", "Convert Text To Title Case"),
        ("capitalize", "Capitalize first letter"),
        ("reverse", "esreveR txet"),
    ]

    table = Table(title="🔄 Available Transformations")
    table.add_column("Transform", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_column("Example", style="yellow")

    for transform, description in transforms_info:
        example = _get_transform_example(transform)
        table.add_row(transform, description, example)

    console.print(table)


def _display_metadata(metadata: dict[str, Any]) -> None:
    """Display processing metadata in a formatted table."""
    if not metadata:
        return

    table = Table(title="📋 Processing Metadata")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")

    for key, value in metadata.items():
        table.add_row(key, str(value))

    console.print(table)


def _display_batch_summary(results: list[ProcessingResult]) -> None:
    """Display batch processing summary."""
    successful = sum(1 for r in results if r.success)
    failed = len(results) - successful

    console.print("\n📊 Batch Summary:")
    console.print(f"  Total items: {len(results)}")
    console.print(f"  Successful: {successful}")
    console.print(f"  Failed: {failed}")

    if results and results[0].success:
        # Show average lengths
        input_lengths = [
            r.metadata.get("input_length", 0) for r in results if r.success
        ]
        output_lengths = [
            r.metadata.get("output_length", 0) for r in results if r.success
        ]

        if input_lengths:
            avg_input = sum(input_lengths) / len(input_lengths)
            avg_output = sum(output_lengths) / len(output_lengths)
            console.print(f"  Average input length: {avg_input:.1f}")
            console.print(f"  Average output length: {avg_output:.1f}")


def _get_transform_example(transform: str) -> str:
    """Get an example output for a transformation."""
    examples = {
        "uppercase": "hello → HELLO",
        "lowercase": "HELLO → hello",
        "title": "hello world → Hello World",
        "capitalize": "hello world → Hello world",
        "reverse": "hello → olleh",
    }
    return examples.get(transform, "hello → ?")


if __name__ == "__main__":
    app()
