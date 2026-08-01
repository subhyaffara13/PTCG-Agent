
def execute_command(user_input: str, ctx: click.Context):
    """Parse and execute a command."""
    # Parse command and arguments
    parts = user_input.split()
    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []

    # Import cli here to avoid circular import
    from . import main

    cli = main.cli

    # Check if command exists
    if command not in cli.commands:
        click.echo(f"Unknown command: {command}")
        click.echo("Type 'help' to see available commands.")
        return

    # Execute the command
    try:
        # Create a new argument list for click to parse
        sys.argv = ["lite"] + [command] + args

        # Get the command object and invoke it
        cmd = cli.commands[command]

        # Create a new context for the subcommand
        with ctx.scope():
            cmd.main(args, parent=ctx, standalone_mode=False)

    except click.ClickException as e:
        e.show()
    except click.Abort:
        click.echo("Command aborted.")
    except SystemExit:
        # Prevent the interactive shell from exiting on command errors
        pass
    except Exception as e:
        click.echo(f"Error executing command: {e}")

