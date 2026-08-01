
def _device_code_login() -> None:
    """Run the Device Code OAuth flow: request a code, prompt the user to authorize it in a browser,
    poll for the token and save it."""
    device_info = request_device_code()

    # The complete URI has the code pre-filled when the server supports it.
    print(f"\n    Open this URL in your browser:\n        {device_info['verification_uri_complete']}\n")
    print(f"    And enter the code: {device_info['user_code']}\n")

    print("    Waiting for authorization", end="", flush=True)
    try:
        response = poll_device_token(device_info, on_pending=lambda: print(".", end="", flush=True))
    finally:
        print()  # newline after the progress dots, also on failure

    _save_oauth_token(response)

