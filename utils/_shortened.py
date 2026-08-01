
def _shortened(word):
    dpos = word.find('$')
    return '|'.join(word[:dpos] + word[dpos+1:i] + r'\b'
                    for i in range(len(word), dpos, -1))

