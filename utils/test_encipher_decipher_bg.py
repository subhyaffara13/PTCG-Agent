
def test_encipher_decipher_bg():
    ps = [67, 7, 71, 103, 11, 43, 107, 47,
          79, 19, 83, 23, 59, 127, 31]
    qs = qs = [7, 71, 103, 11, 43, 107, 47,
               79, 19, 83, 23, 59, 127, 31, 67]
    messages = [
        0, 328, 343, 148, 1280, 758, 383,
        724, 603, 516, 766, 618, 186,
    ]

    for p, q in zip(ps, qs):
        pri = bg_private_key(p, q)
        for msg in messages:
            pub = bg_public_key(p, q)
            enc = encipher_bg(msg, pub)
            dec = decipher_bg(enc, pri)
            assert dec == msg

