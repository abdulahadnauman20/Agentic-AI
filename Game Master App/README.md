# 🧠 AI Adventure Game Master

A text-based adventure game powered by multiple AI agents using the Gemini API. Experience an immersive story where three specialized AI agents work together to create a dynamic gaming experience.

## ✨ Features

### 🤖 Multiple AI Agents
- **🎭 NarratorAgent**: Creates immersive storylines, describes environments, and progresses the narrative
- **⚔️ MonsterAgent**: Manages combat encounters, creates challenging battles, and handles combat mechanics
- **🎒 ItemAgent**: Generates items, manages inventory, and creates rewarding loot systems

### 🎮 Game Features
- **Rich Text Interface**: Beautiful colored output with panels, tables, and formatted text
- **Dynamic Storytelling**: AI-generated narratives that adapt to player choices
- **Combat System**: Turn-based combat with dice rolling mechanics
- **Inventory Management**: Collect and use items throughout your adventure
- **Quest System**: Accept and complete quests for rewards
- **Save/Load System**: Save your progress and continue later
- **Multiple Locations**: Explore different areas with unique encounters

### 🛠️ Tools Integration
- **Dice Rolling**: `roll_dice()` for random game mechanics
- **Event Generation**: `generate_event()` for dynamic encounters
- **Combat Damage**: `calculate_combat_damage()` for battle calculations
- **Loot Generation**: `generate_loot()` for rewards

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Gemini API key from Google AI Studio

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd Game-Master-App
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key**
   
   Create a `.env` file in the project root:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   Or set it as an environment variable:
   ```bash
   export GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the game**
   ```bash
   python main.py
   ```

## 🎯 How to Play

### Basic Commands
- `help` - Show available commands
- `status` - Display character status
- `inventory` - Show your inventory
- `explore` - Explore current location
- `save` - Save your game
- `load` - Load saved game
- `quit` - Exit the game

### Combat Commands
- `attack` - Attack the monster
- `defend` - Defend against attacks
- `flee` - Try to escape combat
- `use <item>` - Use an item during combat

### Navigation
- Use numbered choices (1, 2, 3, etc.) to select options
- Type `move <location>` to travel to specific places
- Explore different areas to discover new content

## 🏗️ Architecture

### Core Components

```
Game Master App/
├── main.py              # Entry point
├── game_runner.py       # Main game orchestrator
├── agents.py            # AI agent implementations
├── game_state.py        # Game state management
├── tools.py             # Game mechanics tools
├── config.py            # Configuration and prompts
├── requirements.txt     # Dependencies
└── README.md           # This file
```

### AI Agent System

1. **NarratorAgent**: Handles story progression and environment descriptions
2. **MonsterAgent**: Manages combat encounters and battle mechanics
3. **ItemAgent**: Creates items and manages inventory systems

### Game Flow

```
Start Game
    ↓
Load/New Game
    ↓
Exploration Mode ←→ Combat Mode
    ↓                    ↓
NarratorAgent      MonsterAgent
    ↓                    ↓
Story Progress     Combat Resolution
    ↓                    ↓
ItemAgent ←→ Inventory Management
    ↓
Save/Load System
```

## 🎲 Game Mechanics

### Experience & Leveling
- Gain experience through combat and quests
- Level up to increase health and combat power
- Experience required: Level × 100

### Combat System
- Turn-based combat with dice rolling
- Player and monster take turns attacking
- Critical hits deal double damage (5% chance)
- Defend to reduce incoming damage

### Inventory System
- Collect items from defeated monsters
- Use items during combat or exploration
- Equipment affects combat performance
- Shop system for purchasing items

### Quest System
- Accept quests from NPCs
- Complete objectives for rewards
- Track quest progress automatically
- Receive experience and gold upon completion

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Gemini API key (required)

### Customization
You can modify the game by editing:
- `config.py`: System prompts and game settings
- `tools.py`: Game mechanics and calculations
- `game_state.py`: Player and world data structures

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   ValueError: Please set GEMINI_API_KEY in your environment variables
   ```
   Solution: Set your Gemini API key in the `.env` file or environment variables.

2. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'google.generativeai'
   ```
   Solution: Install dependencies with `pip install -r requirements.txt`

3. **Permission Errors**
   ```
   PermissionError: [Errno 13] Permission denied
   ```
   Solution: Check file permissions or run with appropriate privileges.

### Getting Help
- Check the console output for error messages
- Verify your API key is correct
- Ensure all dependencies are installed
- Try running with `python -v main.py` for verbose output

## 🎨 Customization

### Adding New Locations
Edit `game_runner.py` and add new scenes to the `scene_descriptions` dictionary.

### Creating New Items
Modify the `ItemAgent` class in `agents.py` to generate different types of items.

### Custom Combat Mechanics
Update the `tools.py` file to modify dice rolling and damage calculations.

## 📝 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 🎮 Enjoy Your Adventure!

Embark on an AI-powered journey where every choice matters and every encounter is unique. The three AI agents work together to create a truly dynamic and engaging gaming experience.

Happy adventuring! 🗡️🛡️✨ 