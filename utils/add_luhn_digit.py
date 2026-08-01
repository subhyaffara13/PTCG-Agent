
def add_luhn_digit(card_number: str) -> str:
    # See https://en.wikipedia.org/wiki/Luhn_algorithm
    for digit in '0123456789':
        with contextlib.suppress(Exception):
            pydantic.PaymentCardNumber.validate_luhn_check_digit(card_number + digit)
            return card_number + digit
    raise AssertionError('Unreachable')  # pragma: no cover

