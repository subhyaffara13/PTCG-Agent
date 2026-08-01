
def word_sequences(tokens):
    return "(" + '|'.join(token.replace(' ', r'\s+') for token in tokens) + r')\b'

