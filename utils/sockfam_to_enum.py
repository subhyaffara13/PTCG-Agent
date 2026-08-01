
def sockfam_to_enum(num):
    """Convert a numeric socket family value to an IntEnum member.
    If it's not a known member, return the numeric value itself.
    """
    try:
        return socket.AddressFamily(num)
    except ValueError:
        return num

