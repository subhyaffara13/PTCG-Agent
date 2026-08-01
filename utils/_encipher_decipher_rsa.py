
def _encipher_decipher_rsa(i, key, factors=None):
    n, d = key
    if not factors:
        return pow(i, d, n)

    def _is_coprime_set(l):
        is_coprime_set = True
        for i in range(len(l)):
            for j in range(i+1, len(l)):
                if gcd(l[i], l[j]) != 1:
                    is_coprime_set = False
                    break
        return is_coprime_set

    prod = reduce(lambda i, j: i*j, factors)
    if prod == n and _is_coprime_set(factors):
        return _decipher_rsa_crt(i, d, factors)
    return _encipher_decipher_rsa(i, key, factors=None)

