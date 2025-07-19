import time
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich.align import Align

from agents import NarratorAgent, MonsterAgent, ItemAgent
from game_state import GameState
from tools import roll_dice, generate_event, generate_loot
from config import GAME_TITLE, GAME_VERSION

class GameRunner:
    """Main game runner that orchestrates all AI agents and game flow."""
    
    def __init__(self):
        self.console = Console()
        self.game_state = GameState()
        self.narrator_agent = NarratorAgent()
        self.monster_agent = MonsterAgent()
        self.item_agent = ItemAgent()
        self.running = False
        
        # Game flow control
        self.current_scene = "village_square"
        self.scene_history = []
        
    def display_welcome(self):
        """Display the game welcome screen."""
        welcome_text = f"""
{GAME_TITLE} v{GAME_VERSION}

Welcome to an AI-powered text adventure game!

You are an adventurer in a mysterious world filled with magic, monsters, and treasures.
Three AI agents will guide your journey:
• 🎭 Narrator Agent - Tells the story and describes your surroundings
• ⚔️ Monster Agent - Manages combat encounters and battles
• 🎒 Item Agent - Handles your inventory and rewards

Type 'help' at any time to see available commands.
Type 'quit' to exit the game.

Your adventure begins now...
        """.strip()
        
        self.console.print(Panel(welcome_text, title="🎮 Welcome to AI Adventure", border_style="blue"))
        self.console.print()
    
    def display_help(self):
        """Display help information."""
        help_text = """
Available Commands:
• help - Show this help message
• status - Show your character status
• inventory - Show your inventory
• explore - Explore the current location
• move <location> - Move to a different location
• attack - Attack in combat
• defend - Defend in combat
• use <item> - Use an item from inventory
• save - Save your game
• load - Load your saved game
• quit - Exit the game

Combat Commands (during combat):
• attack - Attack the monster
• defend - Defend against attacks
• use <item> - Use an item during combat
• flee - Try to escape from combat
        """.strip()
        
        self.console.print(Panel(help_text, title="❓ Help", border_style="green"))
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
    
    def narrate_current_scene(self):
        """Use the narrator agent to describe the current scene."""
        scene_descriptions = {
            "village_square": "You stand in the bustling village square. Merchants call out their wares, children play in the streets, and the smell of fresh bread wafts from the bakery. The village elder's house stands prominently to the north, while a mysterious forest path leads east.",
            "elder_house": "You enter the elder's house, a cozy building filled with ancient books and mysterious artifacts. The village elder sits by the fireplace, looking wise and welcoming.",
            "forest_path": "You walk along a winding forest path. Tall trees create a canopy overhead, and you can hear the sounds of wildlife in the distance. The path seems to lead deeper into the forest.",
            "dark_cave": "You enter a dark, mysterious cave. The air is cool and damp, and you can hear water dripping somewhere in the distance. Strange markings cover the walls.",
            "ancient_ruins": "You discover ancient ruins, remnants of a long-forgotten civilization. Crumbling stone structures stand testament to the passage of time."
        }
        
        scene_desc = scene_descriptions.get(self.current_scene, "You find yourself in an unknown location.")
        
        # Get AI-generated narration
        narration = self.narrator_agent.describe_environment(
            self.game_state.player.location,
            "mysterious"
        )
        
        self.console.print(Panel(narration, title="📍 Current Location", border_style="blue"))
        self.console.print()
        
        # Present choices based on location
        self.present_location_choices()
    
    def present_location_choices(self):
        """Present available choices based on current location."""
        choices = {
            "village_square": [
                "Visit the village elder",
                "Explore the forest path",
                "Check the local shop",
                "Talk to villagers"
            ],
            "elder_house": [
                "Ask for a quest",
                "Learn about the village history",
                "Return to village square"
            ],
            "forest_path": [
                "Continue deeper into the forest",
                "Search for resources",
                "Return to village square"
            ],
            "dark_cave": [
                "Explore deeper into the cave",
                "Search for treasures",
                "Return to the forest path"
            ],
            "ancient_ruins": [
                "Investigate the ruins",
                "Search for artifacts",
                "Return to the forest path"
            ]
        }
        
        available_choices = choices.get(self.current_scene, ["Return to previous location"])
        
        self.console.print("What would you like to do?")
        for i, choice in enumerate(available_choices, 1):
            self.console.print(f"{i}. {choice}")
        self.console.print()
    
    def handle_exploration_choice(self, choice: str):
        """Handle player choice during exploration."""
        if "elder" in choice.lower():
            self.current_scene = "elder_house"
            self.game_state.update_player_location("Elder's House")
            response = self.narrator_agent.progress_story(choice, "Elder's House")
            self.console.print(Panel(response, title="📖 Story Progress", border_style="green"))
            
        elif "forest" in choice.lower():
            self.current_scene = "forest_path"
            self.game_state.update_player_location("Forest Path")
            response = self.narrator_agent.progress_story(choice, "Forest Path")
            self.console.print(Panel(response, title="📖 Story Progress", border_style="green"))
            
        elif "cave" in choice.lower():
            self.current_scene = "dark_cave"
            self.game_state.update_player_location("Dark Cave")
            response = self.narrator_agent.progress_story(choice, "Dark Cave")
            self.console.print(Panel(response, title="📖 Story Progress", border_style="green"))
            
        elif "ruins" in choice.lower():
            self.current_scene = "ancient_ruins"
            self.game_state.update_player_location("Ancient Ruins")
            response = self.narrator_agent.progress_story(choice, "Ancient Ruins")
            self.console.print(Panel(response, title="📖 Story Progress", border_style="green"))
            
        elif "return" in choice.lower():
            if self.current_scene == "elder_house":
                self.current_scene = "village_square"
                self.game_state.update_player_location("Starting Village")
            elif self.current_scene in ["forest_path", "dark_cave", "ancient_ruins"]:
                self.current_scene = "forest_path"
                self.game_state.update_player_location("Forest Path")
            response = self.narrator_agent.progress_story(choice, self.game_state.player.location)
            self.console.print(Panel(response, title="📖 Story Progress", border_style="green"))
            
        elif "shop" in choice.lower():
            self.handle_shop_interaction()
            
        elif "quest" in choice.lower():
            self.handle_quest_interaction()
            
        else:
            # Random event chance
            if roll_dice(20, 1)["total"] > 15:
                event = generate_event("random")
                self.console.print(Panel(f"Random event: {event['description']}", title="🎲 Random Event", border_style="red"))
                
                # Chance for combat
                if roll_dice(20, 1)["total"] > 18:
                    self.start_random_combat()
    
    def handle_shop_interaction(self):
        """Handle shop interactions using the item agent."""
        shop_inventory = self.item_agent.create_shop_inventory("general", self.game_state.player.level)
        self.console.print(Panel(shop_inventory, title="🏪 Shop", border_style="cyan"))
        
        # Simple shop interaction
        self.console.print("Would you like to buy something? (yes/no)")
        if Confirm.ask("Buy items?"):
            # Generate a random item
            item_desc = self.item_agent.generate_item("sword", "common")
            self.console.print(Panel(item_desc, title="🛒 Purchase", border_style="green"))
            
            # Add item to inventory
            new_item = {
                "name": "Rusty Sword",
                "type": "weapon",
                "description": "A basic sword that could use some sharpening",
                "power": 5
            }
            result = self.game_state.add_item_to_inventory(new_item)
            self.console.print(f"✅ {result}")
    
    def handle_quest_interaction(self):
        """Handle quest interactions."""
        quest_data = {
            "title": "The Lost Artifact",
            "description": "Find the ancient artifact hidden in the ruins",
            "rewards": {"experience": 100, "gold": 50}
        }
        
        result = self.game_state.add_quest(quest_data)
        self.console.print(Panel(result, title="📜 New Quest", border_style="yellow"))
    
    def start_random_combat(self):
        """Start a random combat encounter."""
        monster_types = ["goblin", "wolf", "bandit", "undead warrior", "mysterious creature"]
        monster_type = roll_dice(len(monster_types), 1)["rolls"][0] - 1
        
        encounter_desc = self.monster_agent.create_encounter(
            monster_types[monster_type], 
            self.game_state.player.level
        )
        
        self.console.print(Panel(encounter_desc, title="⚔️ Combat Encounter", border_style="red"))
        
        # Start combat
        monster_data = {
            "name": monster_types[monster_type],
            "health": 30,
            "level": 3,
            "type": "enemy"
        }
        self.game_state.start_combat(monster_data)
        
        self.console.print("Combat has begun! Use 'attack', 'defend', or 'flee' commands.")
    
    def handle_combat_round(self, player_action: str):
        """Handle a single round of combat."""
        if not self.game_state.combat_state:
            return "Not in combat."
        
        combat_state = self.game_state.combat_state
        monster = combat_state["monster"]
        
        if player_action.lower() == "attack":
            # Player attacks
            combat_desc = self.monster_agent.manage_combat_round(
                "attack", 
                combat_state["monster_health"], 
                self.game_state.player.health
            )
            
            # Calculate damage
            damage = roll_dice(10, 1)["total"] + self.game_state.player.level * 2
            combat_state["monster_health"] -= damage
            
            self.console.print(Panel(combat_desc, title="⚔️ Combat", border_style="red"))
            self.console.print(f"💥 You deal {damage} damage to the {monster['name']}!")
            
            # Check if monster is defeated
            if combat_state["monster_health"] <= 0:
                self.end_combat_victory()
                return
            
            # Monster counter-attack
            monster_damage = roll_dice(8, 1)["total"]
            self.game_state.damage_player(monster_damage)
            self.console.print(f"💥 The {monster['name']} deals {monster_damage} damage to you!")
            
        elif player_action.lower() == "defend":
            # Player defends
            self.console.print("🛡️ You take a defensive stance!")
            monster_damage = max(1, roll_dice(8, 1)["total"] - 3)  # Reduced damage
            self.game_state.damage_player(monster_damage)
            self.console.print(f"💥 The {monster['name']} deals {monster_damage} damage to you!")
            
        elif player_action.lower() == "flee":
            # Try to flee
            flee_roll = roll_dice(20, 1)["total"]
            if flee_roll > 10:
                self.console.print("🏃 You successfully flee from combat!")
                self.game_state.end_combat()
            else:
                self.console.print("❌ You fail to escape!")
                monster_damage = roll_dice(8, 1)["total"]
                self.game_state.damage_player(monster_damage)
                self.console.print(f"💥 The {monster['name']} deals {monster_damage} damage to you!")
        
        # Check if player is defeated
        if self.game_state.player.health <= 0:
            self.console.print("💀 You have been defeated! Game over.")
            self.running = False
    
    def end_combat_victory(self):
        """Handle combat victory."""
        combat_state = self.game_state.combat_state
        monster = combat_state["monster"]
        
        self.console.print(f"🎉 You defeated the {monster['name']}!")
        
        # Generate loot
        loot = generate_loot(monster.get("level", 3), "common")
        self.console.print(f"💰 {loot['description']}")
        
        # Add rewards
        exp_gained = monster.get("level", 3) * 10
        gold_gained = loot["gold"]
        
        exp_result = self.game_state.add_experience(exp_gained)
        gold_result = self.game_state.add_gold(gold_gained)
        
        self.console.print(f"⭐ {exp_result}")
        self.console.print(f"💰 {gold_result}")
        
        # Generate item description
        if loot["has_special_item"]:
            item_desc = self.item_agent.generate_item("treasure", "uncommon")
            self.console.print(Panel(item_desc, title="🎁 Special Item Found", border_style="yellow"))
            
            # Add item to inventory
            new_item = {
                "name": "Mysterious Artifact",
                "type": "treasure",
                "description": "A strange artifact with unknown powers",
                "rarity": "uncommon"
            }
            result = self.game_state.add_item_to_inventory(new_item)
            self.console.print(f"✅ {result}")
        
        self.game_state.end_combat()
    
    def process_command(self, command: str) -> bool:
        """Process player commands. Returns True if game should continue."""
        command = command.strip().lower()
        
        if command == "quit":
            self.console.print("Thanks for playing! Goodbye!")
            return False
            
        elif command == "help":
            self.display_help()
            
        elif command == "status":
            self.display_status()
            
        elif command == "inventory":
            self.display_inventory()
            
        elif command == "explore":
            self.narrate_current_scene()
            
        elif command == "save":
            result = self.game_state.save_game()
            self.console.print(Panel(result, title="💾 Save Game", border_style="green"))
            
        elif command == "load":
            result = self.game_state.load_game()
            self.console.print(Panel(result, title="📂 Load Game", border_style="green"))
            
        elif command.startswith("move "):
            location = command[5:].strip()
            self.game_state.update_player_location(location)
            self.console.print(f"📍 Moved to {location}")
            
        elif command.startswith("use "):
            item_name = command[4:].strip()
            # Find item in inventory
            for item in self.game_state.player.inventory:
                if item.get("name", "").lower() == item_name.lower():
                    suggestion = self.item_agent.suggest_item_use(item, "general")
                    self.console.print(Panel(suggestion, title="🔧 Use Item", border_style="cyan"))
                    break
            else:
                self.console.print(f"❌ Item '{item_name}' not found in inventory.")
                
        elif command in ["attack", "defend", "flee"]:
            if self.game_state.game_mode == "combat":
                self.handle_combat_round(command)
            else:
                self.console.print("❌ You're not in combat!")
                
        elif command.isdigit():
            # Handle numbered choices
            choice_num = int(command)
            if self.game_state.game_mode == "exploration":
                choices = {
                    "village_square": [
                        "Visit the village elder",
                        "Explore the forest path", 
                        "Check the local shop",
                        "Talk to villagers"
                    ],
                    "elder_house": [
                        "Ask for a quest",
                        "Learn about the village history",
                        "Return to village square"
                    ],
                    "forest_path": [
                        "Continue deeper into the forest",
                        "Search for resources",
                        "Return to village square"
                    ],
                    "dark_cave": [
                        "Explore deeper into the cave",
                        "Search for treasures",
                        "Return to the forest path"
                    ],
                    "ancient_ruins": [
                        "Investigate the ruins",
                        "Search for artifacts",
                        "Return to the forest path"
                    ]
                }
                
                available_choices = choices.get(self.current_scene, ["Return to previous location"])
                if 1 <= choice_num <= len(available_choices):
                    self.handle_exploration_choice(available_choices[choice_num - 1])
                else:
                    self.console.print("❌ Invalid choice number.")
            else:
                self.console.print("❌ Invalid command.")
                
        else:
            self.console.print("❌ Unknown command. Type 'help' for available commands.")
        
        return True
    
    def run(self):
        """Main game loop."""
        self.running = True
        self.display_welcome()
        
        # Load existing game or start new
        load_result = self.game_state.load_game()
        if "successfully" in load_result:
            self.console.print(Panel(load_result, title="📂 Load Game", border_style="green"))
        
        # Initial scene
        self.narrate_current_scene()
        
        while self.running:
            try:
                command = Prompt.ask("\n[bold cyan]What would you like to do?[/bold cyan]")
                self.running = self.process_command(command)
                
                # Add some delay for better readability
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                self.console.print("\n\nThanks for playing! Goodbye!")
                break
            except Exception as e:
                self.console.print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    game = GameRunner()
    game.run() 