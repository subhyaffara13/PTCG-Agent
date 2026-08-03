import os

def _macos_vers():
    version = platform.mac_ver()[0]
    # fallback for MacPorts
    if version == '':
        plist = '/System/Library/CoreServices/SystemVersion.plist'
        if os.path.exists(plist):
            with open(plist, 'rb') as fh:
                plist_content = plistlib.load(fh)
            if 'ProductVersion' in plist_content:
                version = plist_content['ProductVersion']
    return version.split('.')

