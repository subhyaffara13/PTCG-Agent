
def load_launcher_manifest(name):
    res = resources.files(__name__).joinpath('launcher manifest.xml')
    return res.read_text(encoding='utf-8') % vars()

