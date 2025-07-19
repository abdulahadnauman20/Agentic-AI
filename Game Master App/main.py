#!/usr/bin/env python3
"""
🧠 AI Adventure Game Master
A text-based adventure game powered by multiple AI agents using Gemini API.

Features:
- NarratorAgent: Story progression and environment description
- MonsterAgent: Combat encounters and battle management  
- ItemAgent: Inventory and reward management
- Rich text interface with colored output
- Save/load game functionality
- Multiple locations and quests
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from game_runner import GameRunner
    from config import GAME_TITLE, GAME_VERSION
except ImportError as e:
    print(f"Error importing game modules: {e}")
    print("Please make sure all required files are present and dependencies are installed.")
    sys.exit(1)

def main():
    """Main entry point for the game."""
    print(f"🎮 {GAME_TITLE} v{GAME_VERSION}")
    print("Starting AI Adventure Game...")
    print()
    
    try:
        # Create and run the game
        game = GameRunner()
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check your configuration and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main() 