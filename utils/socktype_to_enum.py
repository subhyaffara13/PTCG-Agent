
def socktype_to_enum(num):
    """Convert a numeric socket type value to an IntEnum member.
    If it's not a known member, return the numeric value itself.
    """
    try:
        return socket.SocketKind(num)
    except ValueError:
        return num

