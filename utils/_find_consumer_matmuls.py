
def _find_consumer_matmuls(node: torch.fx.Node) -> list[_Matmul]:
    """
    Find the matmuls that use `node` as the lhs argument.
    """
    matmuls = []
    for user in node.users:
        # ND matmuls
        if user.target is aten.reshape.default:
            matmuls.extend(_find_reshape_mm_reshape(user))
        # 2D matmuls
        elif user.target is aten.mm.default:
            matmul = _Matmul.from_match(match=[user])
            matmuls.append(matmul)
        elif user.target is aten._scaled_mm.default:
            matmul = _ScaledMatmul.from_match([user])
            matmuls.append(matmul)
    return matmuls

