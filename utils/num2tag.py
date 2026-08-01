
def num2tag(n):
    if n < 0x200000:
        return str(n)
    else:
        return (
            struct.unpack("4s", struct.pack(">L", n))[0].replace(b"\000", b"").decode()
        )

