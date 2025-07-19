#!/usr/bin/env python3
"""
Demo script for the AI Adventure Game Master
This script demonstrates the game structure without requiring the Gemini API key.
"""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_state import GameState
from tools import roll_dice, generate_event, calculate_combat_damage, generate_loot

class DemoGame:
    """Demo version of the game that works without API keys."""
    
    def __init__(self):
        self.console = Console()
        self.game_state = GameState()
        self.running = False
        
    def display_welcome(self):
        """Display the game welcome screen."""
        welcome_text = """
🧠 AI Adventure Game Master v1.0.0

Welcome to the DEMO version of the AI-powered text adventure game!

This demo shows the game structure and mechanics without requiring the Gemini API.
In the full version, three AI agents would guide your journey:
• 🎭 Narrator Agent - Tells the story and describes your surroundings
• ⚔️ Monster Agent - Manages combat encounters and battles
• 🎒 Item Agent - Handles your inventory and rewards

Demo Features:
• Character status and inventory management
• Dice rolling and random events
• Combat system with damage calculations
• Loot generation and quest system
• Save/load functionality

Type 'help' at any time to see available commands.
Type 'quit' to exit the demo.

Your demo adventure begins now...
        """.strip()
        
        self.console.print(Panel(welcome_text, title="🎮 Demo - AI Adventure", border_style="blue"))
        self.console.print()
    
    def display_help(self):
        """Display help information."""
        help_text = """
Demo Commands:
• help - Show this help message
• status - Show your character status
• inventory - Show your inventory
• roll - Roll some dice
• event - Generate a random event
• combat - Start a demo combat
• loot - Generate demo loot
• quest - Add a demo quest
• save - Save your demo game
• load - Load your saved demo game
• quit - Exit the demo
        """.strip()
        
        self.console.print(Panel(help_text, title="❓ Demo Help", border_style="green"))
        self.console.print()
    
    def display_status(self):
        """Display player status."""
        status = self.game_state.get_player_status()
        self.console.print(Panel(status, title="📊 Character Status", border_style="yellow"))
        self.console.print()
    
    def display_inventory(self):
        """Display player inventory."""
        if not self.game_state.player.inventory:
            self.console.print(Panel("Your inventory is empty.", title="🎒 Inventory", border_style="cyan"))
        else:
            table = Table(title="🎒 Inventory")
            table.add_column("Item", style="cyan")
            table.add_column("Type", style="magenta")
            table.add_column("Description", style="white")
            
            for item in self.game_state.player.inventory:
                table.add_row(
                    item.get("name", "Unknown"),
                    item.get("type", "Unknown"),
                    item.get("description", "No description")
                )
            
            self.console.print(table)
        self.console.print()
    
    def demo_dice_roll(self):
        """Demonstrate dice rolling."""
        self.console.print("🎲 Rolling some dice...")
        
        # Roll different types of dice
        d20_roll = roll_dice(20, 1)
        d6_roll = roll_dice(6, 3)
        
        self.console.print(f"d20 roll: {d20_roll['description']}")
        self.console.print(f"3d6 roll: {d6_roll['description']}")
        self.console.print()
    
    def demo_event(self):
        """Demonstrate event generation."""
        self.console.print("🎲 Generating a random event...")
        
        event = generate_event("random")
        self.console.print(Panel(f"Event: {event['description']}", title="🎲 Random Event", border_style="red"))
        self.console.print(f"Type: {event['type']}")
        self.console.print(f"Severity: {event['severity']}/10")
        self.console.print(f"Duration: {event['duration']} turns")
        self.console.print()
    
    def demo_combat(self):
        """Demonstrate combat system."""
        self.console.print("⚔️ Starting demo combat...")
        
        # Player attacks
        player_damage = calculate_combat_damage(5, 2)
        self.console.print(f"Player attack: {player_damage['description']}")
        
        # Monster attacks
        monster_damage = calculate_combat_damage(3, 1)
        self.console.print(f"Monster attack: {monster_damage['description']}")
        
        # Show combat details
        table = Table(title="⚔️ Combat Details")
        table.add_column("Attacker", style="cyan")
        table.add_column("Base Damage", style="yellow")
        table.add_column("Level Bonus", style="green")
        table.add_column("Weapon Bonus", style="magenta")
        table.add_column("Total Damage", style="red")
        table.add_column("Critical", style="bold")
        
        table.add_row(
            "Player (Level 5)",
            str(player_damage['base_damage']),
            str(player_damage['level_bonus']),
            str(player_damage['weapon_bonus']),
            str(player_damage['damage']),
            "Yes" if player_damage['is_critical'] else "No"
        )
        
        table.add_row(
            "Monster (Level 3)",
            str(monster_damage['base_damage']),
            str(monster_damage['level_bonus']),
            str(monster_damage['weapon_bonus']),
            str(monster_damage['damage']),
            "Yes" if monster_damage['is_critical'] else "No"
        )
        
        self.console.print(table)
        self.console.print()
    
    def demo_loot(self):
        """Demonstrate loot generation."""
        self.console.print("💰 Generating demo loot...")
        
        loot = generate_loot(5, "rare")
        self.console.print(Panel(f"Loot: {loot['description']}", title="💰 Loot Found", border_style="yellow"))
        self.console.print(f"Rarity: {loot['rarity']}")
        self.console.print(f"Monster Level: {loot['monster_level']}")
        self.console.print(f"Special Item: {'Yes' if loot['has_special_item'] else 'No'}")
        
        # Add some gold to player
        result = self.game_state.add_gold(loot['gold'])
        self.console.print(f"✅ {result}")
        self.console.print()
    
    def demo_quest(self):
        """Demonstrate quest system."""
        self.console.print("📜 Adding a demo quest...")
        
        quest_data = {
            "title": "Demo Quest: Find the Lost Artifact",
            "description": "This is a demo quest to show the quest system functionality",
            "rewards": {"experience": 100, "gold": 50}
        }
        
        result = self.game_state.add_quest(quest_data)
        self.console.print(Panel(result, title="📜 New Quest", border_style="yellow"))
        
        # Show quest details
        table = Table(title="📜 Quest Details")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Title", quest_data["title"])
        table.add_row("Description", quest_data["description"])
        table.add_row("Experience Reward", str(quest_data["rewards"]["experience"]))
        table.add_row("Gold Reward", str(quest_data["rewards"]["gold"]))
        
        self.console.print(table)
        self.console.print()
    
    def process_command(self, command: str) -> bool:
        """Process player commands. Returns True if game should continue."""
        command = command.strip().lower()
        
        if command == "quit":
            self.console.print("Thanks for trying the demo! Goodbye!")
            return False
            
        elif command == "help":
            self.display_help()
            
        elif command == "status":
            self.display_status()
            
        elif command == "inventory":
            self.display_inventory()
            
        elif command == "roll":
            self.demo_dice_roll()
            
        elif command == "event":
            self.demo_event()
            
        elif command == "combat":
            self.demo_combat()
            
        elif command == "loot":
            self.demo_loot()
            
        elif command == "quest":
            self.demo_quest()
            
        elif command == "save":
            result = self.game_state.save_game()
            self.console.print(Panel(result, title="💾 Save Game", border_style="green"))
            
        elif command == "load":
            result = self.game_state.load_game()
            self.console.print(Panel(result, title="📂 Load Game", border_style="green"))
            
        else:
            self.console.print("❌ Unknown command. Type 'help' for available commands.")
        
        return True
    
    def run(self):
        """Main demo loop."""
        self.running = True
        self.display_welcome()
        
        # Add some demo items to inventory
        demo_items = [
            {"name": "Demo Sword", "type": "weapon", "description": "A demonstration sword"},
            {"name": "Demo Potion", "type": "consumable", "description": "A healing potion for demo purposes"}
        ]
        
        for item in demo_items:
            self.game_state.add_item_to_inventory(item)
        
        self.console.print("Demo items added to inventory!")
        self.console.print()
        
        while self.running:
            try:
                command = Prompt.ask("\n[bold cyan]Demo command?[/bold cyan]")
                self.running = self.process_command(command)
                
            except KeyboardInterrupt:
                self.console.print("\n\nDemo interrupted. Thanks for trying!")
                break
            except Exception as e:
                self.console.print(f"❌ Error: {str(e)}")

def main():
    """Main entry point for the demo."""
    print("🎮 AI Adventure Game Master - DEMO")
    print("Starting demo version...")
    print()
    
    try:
        # Create and run the demo
        demo = DemoGame()
        demo.run()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Thanks for trying!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check your setup and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main() 