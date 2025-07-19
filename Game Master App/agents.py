import google.generativeai as genai
from typing import Dict, List, Any, Optional
import json
from config import GEMINI_API_KEY, NARRATOR_SYSTEM_PROMPT, MONSTER_SYSTEM_PROMPT, ITEM_SYSTEM_PROMPT
from tools import roll_dice, generate_event, calculate_combat_damage, generate_loot

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

class BaseAgent:
    """Base class for all AI agents in the game."""
    
    def __init__(self, system_prompt: str, model_name: str = "gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)
        self.system_prompt = system_prompt
        self.conversation_history = []
    
    def _add_to_history(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})
    
    def _get_tools_description(self) -> str:
        """Get description of available tools for the agent."""
        return """
        Available tools:
        - roll_dice(sides: int, count: int): Roll dice for game mechanics
        - generate_event(event_type: str): Generate random events
        - calculate_combat_damage(attacker_level: int, weapon_power: int): Calculate combat damage
        - generate_loot(monster_level: int, rarity: str): Generate loot
        """
    
    def generate_response(self, user_input: str, game_state: Dict[str, Any] = None) -> str:
        """Generate a response using the Gemini model."""
        try:
            # Prepare the full prompt
            full_prompt = f"{self.system_prompt}\n\n{self._get_tools_description()}\n\n"
            
            if game_state:
                full_prompt += f"Current game state: {json.dumps(game_state, indent=2)}\n\n"
            
            full_prompt += f"User input: {user_input}\n\n"
            full_prompt += "Please respond in a natural, engaging way. If you need to use tools, describe what you're doing and the results."
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            # Add to history
            self._add_to_history("user", user_input)
            self._add_to_history("assistant", response.text)
            
            return response.text
            
        except Exception as e:
            return f"Error generating response: {str(e)}"

class NarratorAgent(BaseAgent):
    """AI agent responsible for story narration and progression."""
    
    def __init__(self):
        super().__init__(NARRATOR_SYSTEM_PROMPT)
    
    def narrate_scene(self, scene_description: str, player_choices: List[str] = None) -> str:
        """Narrate a scene and present choices to the player."""
        prompt = f"Narrate this scene: {scene_description}"
        
        if player_choices:
            prompt += f"\n\nPresent these choices to the player:\n"
            for i, choice in enumerate(player_choices, 1):
                prompt += f"{i}. {choice}\n"
        
        return self.generate_response(prompt)
    
    def progress_story(self, player_choice: str, current_location: str) -> str:
        """Progress the story based on player choice."""
        prompt = f"Player chose: {player_choice}\nCurrent location: {current_location}\n\nProgress the story naturally and describe what happens next."
        return self.generate_response(prompt)
    
    def describe_environment(self, location: str, atmosphere: str = "mysterious") -> str:
        """Describe the current environment."""
        prompt = f"Describe the environment at {location} with a {atmosphere} atmosphere. Make it vivid and immersive."
        return self.generate_response(prompt)

class MonsterAgent(BaseAgent):
    """AI agent responsible for combat and monster encounters."""
    
    def __init__(self):
        super().__init__(MONSTER_SYSTEM_PROMPT)
    
    def create_encounter(self, monster_type: str, player_level: int) -> str:
        """Create a monster encounter."""
        # Use tools to generate encounter details
        event = generate_event("combat")
        dice_roll = roll_dice(20, 1)
        
        prompt = f"""
        Create a {monster_type} encounter for a level {player_level} player.
        Event: {event['description']}
        Difficulty roll: {dice_roll['description']}
        
        Describe the monster, its appearance, and the combat situation.
        """
        
        return self.generate_response(prompt)
    
    def manage_combat_round(self, player_action: str, monster_health: int, player_health: int) -> str:
        """Manage a single round of combat."""
        # Calculate damage for both sides
        player_damage = calculate_combat_damage(5, 2)  # Assuming player level 5
        monster_damage = calculate_combat_damage(3, 1)  # Monster level 3
        
        prompt = f"""
        Combat round:
        Player action: {player_action}
        Player damage dealt: {player_damage['description']}
        Monster damage dealt: {monster_damage['description']}
        Monster health: {monster_health}
        Player health: {player_health}
        
        Describe the combat round vividly and determine the outcome.
        """
        
        return self.generate_response(prompt)
    
    def describe_monster_action(self, monster_type: str, action: str) -> str:
        """Describe a monster's action in combat."""
        prompt = f"The {monster_type} performs this action: {action}. Describe it vividly and dramatically."
        return self.generate_response(prompt)

class ItemAgent(BaseAgent):
    """AI agent responsible for inventory and item management."""
    
    def __init__(self):
        super().__init__(ITEM_SYSTEM_PROMPT)
    
    def generate_item(self, item_type: str, rarity: str = "common") -> str:
        """Generate a new item description."""
        # Use tools to generate loot
        loot = generate_loot(5, rarity)  # Assuming level 5 monster
        
        prompt = f"""
        Generate a {rarity} {item_type} item.
        Loot details: {loot['description']}
        
        Create a detailed description of the item, its properties, and potential uses.
        """
        
        return self.generate_response(prompt)
    
    def describe_inventory(self, inventory: List[Dict[str, Any]]) -> str:
        """Describe the player's current inventory."""
        if not inventory:
            return "Your inventory is empty."
        
        prompt = f"Describe the player's inventory containing these items: {json.dumps(inventory, indent=2)}"
        return self.generate_response(prompt)
    
    def suggest_item_use(self, item: Dict[str, Any], situation: str) -> str:
        """Suggest how to use an item in a specific situation."""
        prompt = f"""
        Item: {json.dumps(item, indent=2)}
        Situation: {situation}
        
        Suggest how the player might use this item effectively in this situation.
        """
        
        return self.generate_response(prompt)
    
    def create_shop_inventory(self, shop_type: str, player_level: int) -> str:
        """Create a shop inventory for the player to browse."""
        prompt = f"""
        Create a {shop_type} shop inventory suitable for a level {player_level} player.
        Include various items with different rarities and prices.
        Present them in an engaging way that makes the player want to browse.
        """
        
        return self.generate_response(prompt) 