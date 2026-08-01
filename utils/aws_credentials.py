
def aws_credentials(monkeysession):
    """Mocked AWS Credentials for moto."""
    monkeysession.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeysession.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeysession.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeysession.setenv("AWS_SESSION_AWS_SESSION_TOKEN", "testing")
    monkeysession.setenv("AWS_DEFAULT_REGION", "us-east-1")

