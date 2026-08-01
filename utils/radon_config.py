
def radon_config():
    r = RadonConfig()
    yield r
    del r

