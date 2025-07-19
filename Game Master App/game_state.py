from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class Player:
    """Player character data."""
    name: str
    level: int = 1
    health: int = 100
    max_health: int = 100
    experience: int = 0
    gold: int = 50
    inventory: List[Dict[str, Any]] = field(default_factory=list)
    equipment: Dict[str, Optional[str]] = field(default_factory=lambda: {
        "weapon": None,
        "armor": None,
        "accessory": None
    })
    location: str = "Starting Village"
    quests: List[Dict[str, Any]] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)

@dataclass
class GameWorld:
    """Game world and location data."""
    current_location: str = "Starting Village"
    discovered_locations: List[str] = field(default_factory=lambda: ["Starting Village"])
    world_state: Dict[str, Any] = field(default_factory=dict)
    time_of_day: str = "morning"
    weather: str = "clear"
    events: List[Dict[str, Any]] = field(default_factory=list)

class GameState:
    """Main game state manager."""
    
    def __init__(self):
        self.player = Player("Adventurer")
        self.world = GameWorld()
        self.game_mode = "exploration"  # exploration, combat, dialogue, inventory
        self.combat_state = None
        self.dialogue_state = None
        self.save_file = "game_save.json"
    
    def get_state_dict(self) -> Dict[str, Any]:
        """Get current game state as a dictionary."""
        return {
            "player": {
                "name": self.player.name,
                "level": self.player.level,
                "health": self.player.health,
                "max_health": self.player.max_health,
                "experience": self.player.experience,
                "gold": self.player.gold,
                "inventory": self.player.inventory,
                "equipment": self.player.equipment,
                "location": self.player.location,
                "quests": self.player.quests,
                "achievements": self.player.achievements
            },
            "world": {
                "current_location": self.world.current_location,
                "discovered_locations": self.world.discovered_locations,
                "world_state": self.world.world_state,
                "time_of_day": self.world.time_of_day,
                "weather": self.world.weather,
                "events": self.world.events
            },
            "game_mode": self.game_mode,
            "combat_state": self.combat_state,
            "dialogue_state": self.dialogue_state
        }
    
    def update_player_location(self, new_location: str):
        """Update player location and add to discovered locations."""
        self.player.location = new_location
        self.world.current_location = new_location
        
        if new_location not in self.world.discovered_locations:
            self.world.discovered_locations.append(new_location)
    
    def add_experience(self, amount: int):
        """Add experience and handle leveling up."""
        self.player.experience += amount
        
        # Simple leveling system
        required_exp = self.player.level * 100
        if self.player.experience >= required_exp:
            self.player.level += 1
            self.player.experience -= required_exp
            self.player.max_health += 20
            self.player.health = self.player.max_health
            return f"🎉 Level up! You are now level {self.player.level}!"
        
        return f"Gained {amount} experience points."
    
    def add_gold(self, amount: int):
        """Add gold to player inventory."""
        self.player.gold += amount
        return f"Found {amount} gold pieces."
    
    def add_item_to_inventory(self, item: Dict[str, Any]):
        """Add an item to player inventory."""
        self.player.inventory.append(item)
        return f"Added {item.get('name', 'item')} to inventory."
    
    def remove_item_from_inventory(self, item_name: str) -> bool:
        """Remove an item from inventory by name."""
        for i, item in enumerate(self.player.inventory):
            if item.get('name') == item_name:
                del self.player.inventory[i]
                return True
        return False
    
    def heal_player(self, amount: int):
        """Heal the player."""
        old_health = self.player.health
        self.player.health = min(self.player.health + amount, self.player.max_health)
        healed = self.player.health - old_health
        return f"Healed {healed} health points."
    
    def damage_player(self, amount: int):
        """Damage the player."""
        self.player.health = max(0, self.player.health - amount)
        return f"Took {amount} damage."
    
    def start_combat(self, monster_data: Dict[str, Any]):
        """Start a combat encounter."""
        self.game_mode = "combat"
        self.combat_state = {
            "monster": monster_data,
            "monster_health": monster_data.get("health", 50),
            "round": 1,
            "player_actions": [],
            "monster_actions": []
        }
    
    def end_combat(self):
        """End combat and return to exploration mode."""
        self.game_mode = "exploration"
        self.combat_state = None
    
    def start_dialogue(self, npc_data: Dict[str, Any]):
        """Start a dialogue with an NPC."""
        self.game_mode = "dialogue"
        self.dialogue_state = {
            "npc": npc_data,
            "dialogue_history": [],
            "current_topic": "greeting"
        }
    
    def end_dialogue(self):
        """End dialogue and return to exploration mode."""
        self.game_mode = "exploration"
        self.dialogue_state = None
    
    def add_quest(self, quest_data: Dict[str, Any]):
        """Add a new quest to the player's quest log."""
        quest_data["accepted"] = datetime.now().isoformat()
        quest_data["completed"] = False
        self.player.quests.append(quest_data)
        return f"New quest accepted: {quest_data.get('title', 'Unknown Quest')}"
    
    def complete_quest(self, quest_title: str):
        """Mark a quest as completed."""
        for quest in self.player.quests:
            if quest.get("title") == quest_title and not quest.get("completed", False):
                quest["completed"] = True
                quest["completed_at"] = datetime.now().isoformat()
                
                # Give rewards
                rewards = quest.get("rewards", {})
                exp_gained = rewards.get("experience", 0)
                gold_gained = rewards.get("gold", 0)
                
                if exp_gained > 0:
                    self.add_experience(exp_gained)
                if gold_gained > 0:
                    self.add_gold(gold_gained)
                
                return f"Quest completed: {quest_title}!"
        
        return f"Quest '{quest_title}' not found or already completed."
    
    def add_achievement(self, achievement: str):
        """Add an achievement to the player's list."""
        if achievement not in self.player.achievements:
            self.player.achievements.append(achievement)
            return f"Achievement unlocked: {achievement}!"
        return None
    
    def save_game(self):
        """Save the current game state to a file."""
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.get_state_dict(), f, indent=2)
            return "Game saved successfully!"
        except Exception as e:
            return f"Error saving game: {str(e)}"
    
    def load_game(self):
        """Load game state from a file."""
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
            
            # Restore player data
            player_data = data.get("player", {})
            self.player.name = player_data.get("name", "Adventurer")
            self.player.level = player_data.get("level", 1)
            self.player.health = player_data.get("health", 100)
            self.player.max_health = player_data.get("max_health", 100)
            self.player.experience = player_data.get("experience", 0)
            self.player.gold = player_data.get("gold", 50)
            self.player.inventory = player_data.get("inventory", [])
            self.player.equipment = player_data.get("equipment", {})
            self.player.location = player_data.get("location", "Starting Village")
            self.player.quests = player_data.get("quests", [])
            self.player.achievements = player_data.get("achievements", [])
            
            # Restore world data
            world_data = data.get("world", {})
            self.world.current_location = world_data.get("current_location", "Starting Village")
            self.world.discovered_locations = world_data.get("discovered_locations", ["Starting Village"])
            self.world.world_state = world_data.get("world_state", {})
            self.world.time_of_day = world_data.get("time_of_day", "morning")
            self.world.weather = world_data.get("weather", "clear")
            self.world.events = world_data.get("events", [])
            
            # Restore game mode
            self.game_mode = data.get("game_mode", "exploration")
            self.combat_state = data.get("combat_state")
            self.dialogue_state = data.get("dialogue_state")
            
            return "Game loaded successfully!"
        except FileNotFoundError:
            return "No save file found. Starting new game."
        except Exception as e:
            return f"Error loading game: {str(e)}"
    
    def get_player_status(self) -> str:
        """Get a formatted string of player status."""
        return f"""
🧙‍♂️ {self.player.name} - Level {self.player.level}
❤️ Health: {self.player.health}/{self.player.max_health}
⭐ Experience: {self.player.experience}/{self.player.level * 100}
💰 Gold: {self.player.gold}
📍 Location: {self.player.location}
🎒 Inventory: {len(self.player.inventory)} items
📜 Active Quests: {len([q for q in self.player.quests if not q.get('completed', False)])}
🏆 Achievements: {len(self.player.achievements)}
        """.strip() 