# Tic-Tac-Toe GUI – Design Document

## 1. Overview
- **Goal**: Implement a Python desktop GUI Tic-Tac-Toe game where:
  - A human can play against the computer.
  - The computer can play against itself (auto-play / demo mode).
- **Tech stack (planned)**:
  - Language: Python 3.x
  - GUI: `tkinter` (standard library, no extra install)

## 2. Core Requirements
- 3x3 Tic-Tac-Toe board.
- Support these modes:
  - Human vs Computer
  - Computer vs Computer (with visible moves on the board)
- Game flow:
  - Select mode via a start screen or control panel.
  - Board resets cleanly between games.
  - Display turn indicator ("X's turn" / "O's turn").
  - Detect win, loss, draw:
    - Highlight winning line.
    - Show result message.
  - Provide "New Game" / "Reset" button.
- Computer behavior:
  - Basic AI that plays valid moves and attempts to win / block, or a minimax-based AI for perfect play.
  - In computer vs computer mode, both sides use the AI logic.
  - Optionally add a small delay between computer moves so the user can watch the game.

## 3. High-Level Architecture
- **Main modules (planned)**:
  1. `game_state` (pure logic)
     - Represents board, players, and rules.
     - No GUI dependencies.
  2. `ai` (computer player)
     - Given a game state, chooses the next move.
  3. `gui` (Tkinter UI)
     - Renders board and controls.
     - Connects user actions and AI decisions to the game state.

### 3.1 Game State Responsibilities
- Represent board as a 3x3 structure (e.g., list of 9 cells or 3x3 list).
- Track:
  - Current player (`"X"` or `"O"`).
  - Game status: `IN_PROGRESS`, `X_WON`, `O_WON`, `DRAW`.
- Operations:
  - `reset()` – clear board and set starting player.
  - `make_move(position)` – place current player's mark if the move is valid; update game status; switch current player.
  - `legal_moves()` – return list of empty positions.
  - `check_winner()` – compute and return winner or draw.

### 3.2 AI Responsibilities
- Input: a snapshot of `game_state` (or a lightweight view of it).
- Output: the chosen move (board index or row/col).
- Initial strategy options:
  - **Simple AI (Phase 1)**:
    - If there is a winning move, take it.
    - Else if the opponent has a winning move next, block it.
    - Else choose center, then corners, then sides.
  - **Minimax AI (Phase 2, optional)**:
    - Evaluate all possible outcomes for perfect play.
    - Always choose optimal move (never loses).

### 3.3 GUI Responsibilities
- Build main window with:
  - Title, e.g., "Tic-Tac-Toe".
  - 3x3 grid of buttons for board cells.
  - Status label for messages and turn indicator.
  - Mode selection:
    - Radio buttons or dropdown: `Human vs Computer`, `Computer vs Computer`.
  - Control buttons:
    - `New Game`
    - Optional: `Start Auto-Play` / `Stop Auto-Play`.
- Event handling:
  - Cell button click (human move):
    - Call `make_move` on `game_state`.
    - Refresh UI.
    - If game still in progress and mode includes computer, trigger computer move.
  - Computer move:
    - Use AI to select move.
    - Apply it to `game_state`.
    - Refresh UI.
  - Auto-play loop (Computer vs Computer):
    - Use `after()` method in Tkinter for timed callbacks (e.g., 300–800 ms between moves).

## 4. Data Structures
- Board representation (candidate):
  - `board = [None] * 9` where indices 0–8 map to a 3x3 grid.
  - Helper to convert (row, col) ↔ index: `index = row * 3 + col`.
- Winning lines:
  - Predefined list of index triples, e.g. `[(0,1,2), (3,4,5), ..., (0,4,8), (2,4,6)]`.
- Game status enum (could be simple constants or `Enum`).

## 5. Game Flow Scenarios

### 5.1 Human vs Computer
1. User selects `Human vs Computer` and clicks `New Game`.
2. Game state resets; board is cleared.
3. Human clicks on a cell:
   - If move is valid, `game_state` updates.
   - GUI updates button text and disables that cell.
4. Check game status:
   - If win/draw, show result, disable input.
   - Otherwise, trigger computer move.
5. Computer move:
   - AI selects move based on current board.
   - Apply move, update GUI, check for end state.
6. Repeat until game ends.

### 5.2 Computer vs Computer (Self-Play)
1. User selects `Computer vs Computer` and clicks `Start Auto-Play` (or `New Game`).
2. Game state resets.
3. Use a recurring Tkinter `after()` callback:
   - If game is in progress:
     - Current player is treated as AI.
     - AI picks move and applies it.
     - GUI updates.
     - Schedule the next callback after a short delay.
   - If game ended:
     - Show result.
     - Optionally auto-restart after a delay if desired.

## 6. Error Handling & Edge Cases
- Ignore clicks on already-occupied cells.
- Prevent additional moves after game ends.
- Safely handle no-legal-move situations (should imply draw).
- Ensure that the auto-play loop stops when window is closed.

## 7. Incremental Implementation Plan
1. **Game logic only**
   - Implement `game_state` with unit-testable functions.
2. **Minimal AI**
   - Implement simple AI with win/block/center/corners/sides.
3. **Basic GUI – Human vs Human**
   - Draw the board and wire buttons to `game_state`.
4. **Integrate AI – Human vs Computer**
   - After human move, call AI and update board.
5. **Add Computer vs Computer mode**
   - Implement a timed loop using Tkinter `after()`.
6. **Polish**
   - Highlight winning line, better status messages, small delays for visibility.

## 8. Future Enhancements (Optional)
- Difficulty levels (random vs smart vs perfect AI).
- Scoreboard across multiple games.
- Option to choose who starts (X or O, human or computer).
- Themes / colors / simple animations.
