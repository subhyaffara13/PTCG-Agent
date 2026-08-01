
def getworkerinfoline(node):
    try:
        return node._workerinfocache
    except AttributeError:
        d = node.workerinfo
        ver = "{}.{}.{}".format(*d["version_info"][:3])
        node._workerinfocache = s = "[{}] {} -- Python {} {}".format(
            d["id"], d["sysplatform"], ver, d["executable"]
        )
        return s

