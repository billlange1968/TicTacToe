from __future__ import annotations

import tkinter as tk
from typing import Optional

from .game_state import GameState, GameStatus
from . import ai


class TicTacToeGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tic-Tac-Toe")

        self.game = GameState()
        self.buttons = []  # type: ignore[var-annotated]
        self.default_button_bg: Optional[str] = None

        self.status_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="Human vs Computer")
        self.auto_play_running = False
        self.ai_delay_ms = 400

        self._build_layout()
        self._update_status_label()

    # UI construction -----------------------------------------------------
    def _build_layout(self) -> None:
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Mode:").pack(side=tk.LEFT, padx=(0, 5))
        tk.Radiobutton(
            top_frame,
            text="Human vs Computer",
            variable=self.mode_var,
            value="Human vs Computer",
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            top_frame,
            text="Computer vs Computer",
            variable=self.mode_var,
            value="Computer vs Computer",
        ).pack(side=tk.LEFT, padx=(5, 0))

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        tk.Button(control_frame, text="New Game", command=self.new_game).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(
            control_frame, text="Start Auto-Play", command=self.start_auto_play
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Stop Auto-Play", command=self.stop_auto_play).pack(
            side=tk.LEFT, padx=5
        )

        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=10)

        for r in range(3):
            for c in range(3):
                index = r * 3 + c
                btn = tk.Button(
                    board_frame,
                    text=" ",
                    width=4,
                    height=2,
                    font=("Arial", 24),
                    command=lambda idx=index: self.handle_cell_click(idx),
                )
                btn.grid(row=r, column=c, padx=5, pady=5)
                if self.default_button_bg is None:
                    self.default_button_bg = btn.cget("background")
                self.buttons.append(btn)

        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=(0, 10))

        tk.Label(status_frame, textvariable=self.status_var, font=("Arial", 12)).pack()

    # Game control --------------------------------------------------------
    def new_game(self) -> None:
        self.stop_auto_play()
        self.game.reset()
        self._refresh_board()
        self._update_status_label()

    def start_auto_play(self) -> None:
        """Start continuous computer-vs-computer play."""
        self.mode_var.set("Computer vs Computer")
        if self.game.status is not GameStatus.IN_PROGRESS:
            self.game.reset()
            self._refresh_board()
        self.auto_play_running = True
        self._schedule_next_auto_move()

    def stop_auto_play(self) -> None:
        self.auto_play_running = False

    # Event handlers ------------------------------------------------------
    def handle_cell_click(self, index: int) -> None:
        if self.game.status is not GameStatus.IN_PROGRESS:
            return

        # In Computer vs Computer mode, ignore human clicks
        if self.mode_var.get() == "Computer vs Computer":
            return

        # Human is always X in this simple setup
        if self.game.current_player != "X":
            return

        moved = self.game.make_move(index)
        if not moved:
            return

        self._refresh_board()
        self._update_status_label()

        if self.game.status is GameStatus.IN_PROGRESS:
            # Trigger a single AI response for O
            self.root.after(self.ai_delay_ms, self._ai_single_move)

    def _ai_single_move(self) -> None:
        if self.game.status is not GameStatus.IN_PROGRESS:
            return
        if self.game.current_player != "O":
            return

        move = ai.choose_move(self.game)
        if move is None:
            return
        self.game.make_move(move)
        self._refresh_board()
        self._update_status_label()

    def _schedule_next_auto_move(self) -> None:
        if not self.auto_play_running:
            return
        if self.game.status is not GameStatus.IN_PROGRESS:
            return
        self.root.after(self.ai_delay_ms, self._auto_move_step)

    def _auto_move_step(self) -> None:
        if not self.auto_play_running:
            return
        if self.game.status is not GameStatus.IN_PROGRESS:
            return

        move = ai.choose_move(self.game)
        if move is None:
            self.auto_play_running = False
            return

        self.game.make_move(move)
        self._refresh_board()
        self._update_status_label()

        if self.auto_play_running and self.game.status is GameStatus.IN_PROGRESS:
            self._schedule_next_auto_move()
        else:
            self.auto_play_running = False

    # UI updates ----------------------------------------------------------
    def _refresh_board(self) -> None:
        # Reset all buttons first
        for i, btn in enumerate(self.buttons):
            val = self.game.board[i]
            btn.config(text=(val if val is not None else " "))
            if self.default_button_bg is not None:
                btn.config(background=self.default_button_bg)
            btn.config(state=tk.NORMAL)

        # Highlight winning line if any
        if self.game.winning_line is not None:
            for i in self.game.winning_line:
                self.buttons[i].config(background="#a8e6a1")

        # Disable board if game ended
        if self.game.status is not GameStatus.IN_PROGRESS:
            for btn in self.buttons:
                btn.config(state=tk.DISABLED)

    def _update_status_label(self) -> None:
        if self.game.status is GameStatus.IN_PROGRESS:
            self.status_var.set(f"{self.game.current_player}'s turn")
        elif self.game.status is GameStatus.X_WON:
            self.status_var.set("X wins!")
        elif self.game.status is GameStatus.O_WON:
            self.status_var.set("O wins!")
        else:
            self.status_var.set("It's a draw.")


def run() -> None:
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
