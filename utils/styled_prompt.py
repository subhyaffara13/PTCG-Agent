import os

def styled_prompt():
    """Create a styled blue box prompt for user input."""

    # Get terminal height to ensure we have enough space
    try:
        terminal_height = os.get_terminal_size().lines
        # Ensure we have at least 5 lines of space (for the box + some buffer)
        if terminal_height < 10:
            # If terminal is too small, just add some newlines to push content up
            click.echo("\n" * 3)
    except Exception as e:
        # Fallback if we can't get terminal size
        verbose_logger.debug(f"Error getting terminal size: {e}")
        click.echo("\n" * 3)

    # Unicode box drawing characters
    top_left = "┌"
    top_right = "┐"
    bottom_left = "└"
    bottom_right = "┘"
    horizontal = "─"
    vertical = "│"

    # Create the box with increased width
    width = 80
    top_line = top_left + horizontal * (width - 2) + top_right
    bottom_line = bottom_left + horizontal * (width - 2) + bottom_right

    # Create styled elements
    left_border = click.style(vertical, fg="blue", bold=True)
    right_border = click.style(vertical, fg="blue", bold=True)
    prompt_text = click.style("> ", fg="cyan", bold=True)

    # Display the complete box structure first to reserve space
    click.echo(click.style(top_line, fg="blue", bold=True))

    # Create empty space in the box for input
    empty_space = " " * (width - 4)
    click.echo(f"{left_border} {empty_space} {right_border}")

    # Display bottom border to complete the box
    click.echo(click.style(bottom_line, fg="blue", bold=True))

    # Now move cursor up to the input line and get input
    click.echo("\033[2A", nl=False)  # Move cursor up 2 lines
    click.echo(
        f"\r{left_border} {prompt_text}", nl=False
    )  # Position at start of input line

    try:
        # Get user input
        user_input = input().strip()

        # Move cursor down to after the box
        click.echo("\033[1B")  # Move cursor down 1 line
        click.echo("")  # Add some space after

    except (KeyboardInterrupt, EOFError):
        # Move cursor down and add space
        click.echo("\033[1B")
        click.echo("")
        raise

    return user_input

