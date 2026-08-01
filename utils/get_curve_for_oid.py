
def get_curve_for_oid(oid: ObjectIdentifier) -> type[EllipticCurve]:
    try:
        return _OID_TO_CURVE[oid]
    except KeyError:
        raise LookupError(
            "The provided object identifier has no matching elliptic "
            "curve class"
        )

