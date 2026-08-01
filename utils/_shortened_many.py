
def _shortened_many(*words):
    return '|'.join(map(_shortened, words))

