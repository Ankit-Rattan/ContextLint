import typer
from typing import List, Optional
from core.compiler import PromptCompiler
from llm.gateway import LLMGateway

# Initialize the Typer app
app = typer.Typer(help="Prompt Compiler: Turn messy context into structured LLM prompts.")

# This forces Typer to keep command groups even if there is only one command
@app.callback()
def callback():
    pass

@app.command()
def optimize(
    prompt: str = typer.Option(..., "-p", "--prompt", help="Your vague, initial prompt or goal."),
    files: Optional[List[str]] = typer.Option(None, "-f", "--file", help="Path to a context file (can be used multiple times)."),
    output: str = typer.Option("optimized_prompt.md", "-o", "--output", help="Name of the output Markdown file.")
):
    """
    Takes a vague prompt and raw files, compiles them, and uses an LLM to generate a structured markdown prompt.
    """
    typer.secho("\n🚀 Starting Prompt Compilation...", fg=typer.colors.CYAN)
    
    # 1. Initialize our modules
    compiler = PromptCompiler()
    try:
        gateway = LLMGateway(provider="gemini")
    except ValueError as e:
        typer.secho(f"\n❌ Configuration Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    file_paths = files if files else []
    
    # 2. Compile the payload (Parse files, count tokens, wrap in Meta-Prompt)
    typer.secho(f"📁 Parsing {len(file_paths)} file(s) and calculating tokens...", fg=typer.colors.YELLOW)
    try:
        compiled_payload = compiler.compile(vague_prompt=prompt, file_paths=file_paths)
    except Exception as e:
        typer.secho(f"\n❌ Error during compilation: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    metrics = compiled_payload["metrics"]
    typer.secho(f"📊 Raw Input Tokens: {metrics['raw_input_tokens']}", fg=typer.colors.BLUE)
    
    # 3. Call the LLM Gateway
    typer.secho("🤖 Sending compiled payload to Gemini...", fg=typer.colors.YELLOW)
    try:
        final_markdown = gateway.generate_optimized_prompt(compiled_payload)
    except Exception as e:
        typer.secho(f"\n❌ Error from LLM Gateway: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    # 4. Save the output
    try:
        with open(output, "w", encoding="utf-8") as f:
            f.write(final_markdown)
    except IOError as e:
        typer.secho(f"\n❌ Failed to write to {output}: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    # 5. Final Report
    typer.secho(f"\n✅ Success! Optimized prompt saved to -> {output}", fg=typer.colors.GREEN, bold=True)
    typer.secho(f"📈 Total Compiled Tokens Sent to Gemini: {metrics['compiled_payload_tokens']}\n", fg=typer.colors.BLUE)

if __name__ == "__main__":
    app()