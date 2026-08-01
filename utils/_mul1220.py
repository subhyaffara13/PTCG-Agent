
def _mul1220(num1, num2):
    """Multiply two numbers in 12.20 fixed point format."""
    # Separated into a function because >> has surprising precedence
    return (num1*num2) >> 20

