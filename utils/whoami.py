import time

def whoami():
    """Show current authentication status"""
    token_data = load_token()

    if not token_data:
        click.echo("❌ Not authenticated. Run 'lite login' to authenticate.")
        return

    click.echo("✅ Authenticated")
    click.echo(f"User Email: {token_data.get('user_email', 'Unknown')}")
    click.echo(f"User ID: {token_data.get('user_id', 'Unknown')}")
    click.echo(f"User Role: {token_data.get('user_role', 'Unknown')}")

    # Check if token is still valid (basic timestamp check)
    timestamp = token_data.get("timestamp", 0)
    age_hours = (time.time() - timestamp) / 3600
    click.echo(f"Token age: {age_hours:.1f} hours")

    if age_hours > CLI_JWT_EXPIRATION_HOURS:
        click.echo(
            f"⚠️ Warning: Token is more than {CLI_JWT_EXPIRATION_HOURS} hours old and may have expired."
        )

