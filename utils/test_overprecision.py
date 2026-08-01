
def test_overprecision():
    # We used to output too many digits in FontMatrix entries and
    # ItalicAngle, which could make Type-1 parsers unhappy.
    filename = os.path.join(os.path.dirname(__file__), 'data', 'cmr10.pfb')
    font = t1f.Type1Font(filename)
    slanted = font.transform({'slant': .167})
    lines = slanted.parts[0].decode('ascii').splitlines()
    matrix, = (line[line.index('[')+1:line.index(']')]
               for line in lines if '/FontMatrix' in line)
    angle, = (word
              for line in lines if '/ItalicAngle' in line
              for word in line.split() if word[0] in '-0123456789')
    # the following used to include 0.00016700000000000002
    assert matrix == '0.001 0 0.000167 0.001 0 0'
    # and here we had -9.48090361795083
    assert angle == '-9.4809'

