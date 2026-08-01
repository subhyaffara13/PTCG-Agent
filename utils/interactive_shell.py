
def interactive_shell(ctx: click.Context):
    """Run the interactive shell."""
    setup_shell(ctx)

    while True:
        try:
            # Add some space before the input box to ensure it's positioned well
            click.echo("\n")  # Extra spacing

            # Show styled prompt
            user_input = styled_prompt()

            if not user_input:
                continue

            # Handle special commands
            if handle_special_commands(user_input):
                if user_input.lower() in ["exit", "quit"]:
                    break
                continue

            # Execute regular commands
            execute_command(user_input, ctx)

        except (KeyboardInterrupt, EOFError):
            click.echo("\nGoodbye!")
            break
        except Exception as e:
            click.echo(f"Error: {e}")

