
def _get_email_logger_class():
    """
    Determine which email logger class to use based on environment variables.
    Priority: SendGrid > Resend > SMTP > BaseEmailLogger (fallback)

    Returns:
        The email logger class to use, or None if BaseEmailLogger is not available
    """
    if BaseEmailLogger is None:
        return None

    # Check for SendGrid API key
    if SendGridEmailLogger is not None and os.getenv("SENDGRID_API_KEY"):
        return SendGridEmailLogger

    # Check for Resend API key
    if ResendEmailLogger is not None and os.getenv("RESEND_API_KEY"):
        return ResendEmailLogger

    # Check for SMTP configuration
    if SMTPEmailLogger is not None and os.getenv("SMTP_HOST"):
        return SMTPEmailLogger

    # Fallback to BaseEmailLogger (though it won't actually send emails)
    return BaseEmailLogger

