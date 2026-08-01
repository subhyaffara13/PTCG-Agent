
def find_reached(board, c):
    color = board[c]
    chain = {c}
    reached = set()
    frontier = [c]
    while frontier:
        current = frontier.pop()
        chain.add(current)
        for n in NEIGHBORS[current]:
            if board[n] == color and n not in chain:
                frontier.append(n)
            elif board[n] != color:
                reached.add(n)
    return chain, reached

