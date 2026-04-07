# Tic-Tac-Toe Game

A Python desktop GUI implementation of the classic Tic-Tac-Toe game with AI capabilities.

## Features

- **Human vs Computer**: Play against an intelligent computer opponent
- **Computer vs Computer**: Watch the AI play against itself in demo mode
- **Smart AI**: Computer player with strategic decision-making
- **Graphical Interface**: Built with tkinter for cross-platform compatibility
- **Clean Game Flow**: Reset board between games, display turn indicators, and highlight winning lines
- **Draw Detection**: Automatically detects wins, losses, and draws

## Tech Stack

- **Language**: Python 3.x
- **GUI Framework**: tkinter (included in Python standard library)

## Game Modes

1. **Human vs Computer** - You play as X, the computer plays as O
2. **Computer vs Computer** - Watch both AI players compete

## Getting Started

Run the game with:
```bash
python main.py
```

## Project Structure

- `main.py` - Application entry point
- `tictactoe/` - Core game modules
  - `game_state.py` - Game logic and board state management
  - `ai.py` - Computer player AI implementation
  - `gui.py` - Tkinter-based graphical user interface
- `docs/` - Documentation
  - [tic_tac_toe_design.md](docs/tic_tac_toe_design.md) - Detailed design document

## Design Details

For a comprehensive overview of the game architecture, requirements, and design decisions, see the [Design Document](docs/tic_tac_toe_design.md).
