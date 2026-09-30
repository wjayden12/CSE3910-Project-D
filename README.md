# Conquistador

**Conquistador** is a local four-player strategy board game built in Python with Pygame. Inspired by resource-management and settlement-building games, players collect resources, expand their road networks, build settlements and cities, use development cards, and compete to reach 10 victory points.

This project was developed for Alberta High School Advanced Computing Science **CSE3910 Project D**.

## Features

- Four-player local gameplay
- Randomized 19-tile hex-style board
- Randomized number-token placement with adjacent 6s and 8s avoided
- Snake-order starting placement (`1 → 2 → 3 → 4 → 4 → 3 → 2 → 1`)
- Dice rolling and automatic resource distribution
- Roads, settlements, and city upgrades
- Placement validation for roads and settlements
- Robber movement when a 7 is rolled
- Stealing a random resource from an adjacent player
- 3:1 resource trading with the bank
- Development cards, including knights and victory-point cards
- Largest Army bonus
- Longest Road calculation and bonus
- Automatic victory-point tracking
- Win screen at 10 victory points
- Menu system, graphical UI, and background music

## Tech Stack

- **Python 3**
- **Pygame**

## Project Structure

```text
CSE3910-Project_D/
├── main.py                 # Application entry point and main menu/game loop
├── src/
│   ├── game/
│   │   ├── board.py        # Board state, placement rules, resources, longest road
│   │   ├── constants.py    # Board coordinates, road graph, colours, tile mappings
│   │   ├── game.py         # Turn flow, phases, trading, robber, scoring, win logic
│   │   ├── player.py       # Player, bank, dice, resources, costs, player actions
│   │   ├── structures.py   # Road, Settlement, and City data classes
│   │   └── tiles.py        # Random board and number-token generation
│   ├── ui/
│   │   ├── menu.py         # Main menu rendering/input
│   │   └── ui.py           # Board and in-game UI rendering
│   └── audio/
│       └── song.mp3        # Background music
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd CSE3910-Project_D
```

### 2. Install Pygame

```bash
pip install pygame
```

Using a virtual environment is recommended:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Then install Pygame:

```bash
pip install pygame
```

## Running the Game

Run the project from the repository root so that the `src` imports and audio path resolve correctly:

```bash
python main.py
```

The game opens in a borderless window at the current display resolution and starts at the main menu.

## How to Play

### Initial placement

Each player places one settlement followed by one connected road. Placement follows snake order:

```text
Player 1 → Player 2 → Player 3 → Player 4
Player 4 → Player 3 → Player 2 → Player 1
```

When a player places their second starting settlement, they receive one resource from each adjacent non-desert tile.

### Turns

During a normal turn, a player can:

1. **Roll the dice.**
2. Collect resources from tiles matching the roll.
3. Build roads, settlements, or cities if they can afford them.
4. Buy or use development cards.
5. Trade resources with the bank at a 3:1 ratio.
6. End their turn.

A player must roll before ending their turn or performing several turn actions.

### Building costs

| Item | Cost |
| --- | --- |
| Road | 1 Wood + 1 Brick |
| Settlement | 1 Wood + 1 Brick + 1 Sheep + 1 Wheat |
| City | 3 Ore + 2 Wheat |
| Development Card | 1 Sheep + 1 Wheat + 1 Ore |

Settlements must connect to one of the player's roads and cannot be placed directly beside another settlement or city. Cities are upgrades to settlements already owned by the player.

### Resource production

When a number is rolled, players receive resources from adjacent tiles with that number:

- **Settlement:** 1 resource
- **City:** 2 resources

The robber blocks production on the tile it occupies.

### Robber

When a **7** is rolled, the current player moves the robber to another tile. If another player's structure is adjacent to that tile, the current player can steal one random resource from an eligible player.

Playing a knight development card also activates the robber.

### Longest Road and Largest Army

The game tracks two bonus awards:

- **Longest Road:** +2 victory points
- **Largest Army:** +2 victory points after using at least 3 knight cards and having the largest army

Road calculations account for connected road segments and opposing structures that interrupt a route.

### Winning

Victory points come from:

- Settlements: **1 VP**
- Cities: **2 VP**
- Victory-point development cards: **1 VP**
- Longest Road: **2 VP**
- Largest Army: **2 VP**

The first player to reach **10 victory points** wins.

## Board Generation

Each new game creates a randomized board containing:

| Resource | Tiles |
| --- | ---: |
| Lumber | 4 |
| Grain | 4 |
| Wool | 4 |
| Brick | 3 |
| Ore | 3 |
| Desert | 1 |

Number tokens are also shuffled. The generator attempts to prevent high-probability **6** and **8** tiles from being directly adjacent to each other.

## Code Overview

### `main.py`
Initializes Pygame, creates the borderless display, starts background music, and switches between the menu and active game states.

### `game.py`
Contains the main gameplay controller. It manages setup order, turns, input handling, building modes, dice rolls, trading, robber phases, development cards, bonuses, victory points, and the win state.

### `board.py`
Represents the game board and its graph of vertices and edges. It validates structure placement, distributes resources, tracks the robber, calculates victory points, and uses a depth-first search to determine road length.

### `player.py`
Defines player inventory, building costs, dice rolling, development cards, and click actions. It also contains the bank and its resource inventory.

### `tiles.py`
Randomizes terrain tiles and number tokens for each new board while checking the placement of 6 and 8 tokens.

### `constants.py`
Stores drawing coordinates and the mappings between tiles, settlement vertices, and valid road connections.

### `structures.py`
Defines the game's `Road`, `Settlement`, and `City` objects.

## Current Development Notes

The core playable systems are implemented, but the project can still be expanded and polished. Possible next steps include:

- Improve the interface and visual feedback
- Add player-to-player trading
- Expand the development-card system
- Add ports and specialized trade ratios
- Improve bank/resource accounting throughout all game actions
- Add automated tests for placement and scoring rules
- Add configurable player names or player counts
- Add save/load support


