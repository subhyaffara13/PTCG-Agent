
def auth_whoami() -> None:
    """Find out which huggingface.co account you are logged in as."""

    token = get_token()
    if token is None:
        out.error("Not logged in")
        raise typer.Exit(code=1)

    info = whoami(token)
    orgs = ",".join(org["name"] for org in info["orgs"]) or None
    endpoint = ENDPOINT if ENDPOINT != "https://huggingface.co" else None
    out.result("Logged in", user=info["name"], orgs=orgs, endpoint=endpoint)

