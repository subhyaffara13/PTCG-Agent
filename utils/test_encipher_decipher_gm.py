
def test_encipher_decipher_gm():
    ps = [131, 137, 139, 149, 151, 157, 163, 167,
          173, 179, 181, 191, 193, 197, 199]
    qs = [89, 97, 101, 103, 107, 109, 113, 127,
          131, 137, 139, 149, 151, 157, 47]
    messages = [
        0, 32855, 34303, 14805, 1280, 75859, 38368,
        724, 60356, 51675, 76697, 61854, 18661,
    ]
    for p, q in zip(ps, qs):
        pri = gm_private_key(p, q)
        for msg in messages:
            pub = gm_public_key(p, q)
            enc = encipher_gm(msg, pub)
            dec = decipher_gm(enc, pri)
            assert dec == msg

