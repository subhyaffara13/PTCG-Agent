
def sha256_of_string(string):
    """ Computes the SHA256 hash of a string. """
    sh = sha256()
    sh.update(string)
    return sh

