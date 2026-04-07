from __future__ import annotations

from typing import Optional

from .game_state import GameState, WIN_LINES


def choose_move(state: GameState) -> Optional[int]:
    """Choose the next move for the current player.

    Strategy (simple but decent):
    1. If there is a winning move, take it.
    2. Else if the opponent has a winning reply, block it.
    3. Else take center if available.
    4. Else take a corner if available.
    5. Else take any remaining move.
    """

    if state.status.name != "IN_PROGRESS":
        return None

    player = state.current_player
    opponent = "O" if player == "X" else "X"
    legal = state.legal_moves()
    if not legal:
        return None

    # 1. Winning move for current player
    for move in legal:
        if _is_winning_move(state, move, player):
            return move

    # 2. Block opponent's winning move
    for move in legal:
        if _is_winning_move(state, move, opponent):
            return move

    # 3. Take center
    if 4 in legal:
        return 4

    # 4. Take a corner
    for corner in (0, 2, 6, 8):
        if corner in legal:
            return corner

    # 5. Fallback: any legal move
    return legal[0]


def _is_winning_move(state: GameState, move: int, player: str) -> bool:
    board = list(state.board)
    board[move] = player
    for a, b, c in WIN_LINES:
        if board[a] == board[b] == board[c] == player:
            return True
    return False
