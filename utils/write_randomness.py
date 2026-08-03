import random

def write_randomness(number=200):
    f = open(fname, "w")
    for i in range(number):
        f.write(random.choice(rand_chars))
    f.close()
    f = open(fname, "r")
    contents = f.read()
    f.close()
    return contents

