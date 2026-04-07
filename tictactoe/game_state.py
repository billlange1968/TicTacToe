from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Sequence, Tuple


class GameStatus(Enum):
    IN_PROGRESS = auto()
    X_WON = auto()
    O_WON = auto()
    DRAW = auto()


# All winning line index triples for a 3x3 board (flattened indices 0-8)
WIN_LINES: Tuple[Tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def _compute_winner(board: Sequence[Optional[str]]) -> Optional[Tuple[str, Tuple[int, int, int]]]:
    """Return (winner_symbol, winning_line) or None if no winner yet."""
    for line in WIN_LINES:
        a, b, c = line
        symbol = board[a]
        if symbol is not None and symbol == board[b] == board[c]:
            return symbol, line
    return None


@dataclass
class GameState:
    board: List[Optional[str]] = field(default_factory=lambda: [None] * 9)
    current_player: str = "X"
    status: GameStatus = GameStatus.IN_PROGRESS
    winner: Optional[str] = None
    winning_line: Optional[Tuple[int, int, int]] = None

    def reset(self) -> None:
        self.board = [None] * 9
        self.current_player = "X"
        self.status = GameStatus.IN_PROGRESS
        self.winner = None
        self.winning_line = None

    def legal_moves(self) -> List[int]:
        if self.status is not GameStatus.IN_PROGRESS:
            return []
        return [i for i, cell in enumerate(self.board) if cell is None]

    def make_move(self, position: int) -> bool:
        """Place current player's mark at position if valid.

        Returns True if the move was applied, False otherwise.
        """
        if self.status is not GameStatus.IN_PROGRESS:
            return False
        if position < 0 or position >= 9:
            return False
        if self.board[position] is not None:
            return False

        self.board[position] = self.current_player
        self._update_status()
        if self.status is GameStatus.IN_PROGRESS:
            self._switch_player()
        return True

    def _switch_player(self) -> None:
        self.current_player = "O" if self.current_player == "X" else "X"

    def _update_status(self) -> None:
        result = _compute_winner(self.board)
        if result is not None:
            symbol, line = result
            self.winner = symbol
            self.winning_line = line
            self.status = GameStatus.X_WON if symbol == "X" else GameStatus.O_WON
            return

        if not any(cell is None for cell in self.board):
            self.status = GameStatus.DRAW
            self.winner = None
            self.winning_line = None
        else:
            self.status = GameStatus.IN_PROGRESS
            self.winner = None
            self.winning_line = None

    def clone(self) -> "GameState":
        """Return a shallow copy suitable for AI simulation."""
        return GameState(
            board=list(self.board),
            current_player=self.current_player,
            status=self.status,
            winner=self.winner,
            winning_line=self.winning_line,
        )

    def __str__(self) -> str:  # pragma: no cover - convenience only
        rows = []
        for r in range(3):
            row = []
            for c in range(3):
                val = self.board[r * 3 + c]
                row.append(val if val is not None else ".")
            rows.append(" ".join(row))
        return "\n".join(rows)
