
def import_email_validator() -> None:
    global email_validator
    try:
        import email_validator
    except ImportError as e:
        raise ImportError("email-validator is not installed, run `pip install 'pydantic[email]'`") from e
    if not version('email-validator').partition('.')[0] == '2':
        raise ImportError('email-validator version >= 2.0 required, run pip install -U email-validator')


def import_email_validator() -> None:
    global email_validator
    try:
        import email_validator
    except ImportError as e:
        raise ImportError('email-validator is not installed, run `pip install pydantic[email]`') from e

