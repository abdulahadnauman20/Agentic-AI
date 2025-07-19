import random
import json
from typing import Dict, List, Any

def roll_dice(sides: int = 20, count: int = 1) -> Dict[str, Any]:
    """
    Roll dice for game mechanics.
    
    Args:
        sides: Number of sides on the dice (default: 20)
        count: Number of dice to roll (default: 1)
    
    Returns:
        Dictionary with roll results and details
    """
    if sides < 2:
        raise ValueError("Dice must have at least 2 sides")
    if count < 1:
        raise ValueError("Must roll at least 1 die")
    
    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls)
    
    return {
        "total": total,
        "rolls": rolls,
        "sides": sides,
        "count": count,
        "description": f"Rolled {count}d{sides} = {rolls} (Total: {total})"
    }

def generate_event(event_type: str = "random") -> Dict[str, Any]:
    """
    Generate random events for the game.
    
    Args:
        event_type: Type of event to generate (combat, exploration, social, random)
    
    Returns:
        Dictionary with event details
    """
    events = {
        "combat": [
            "A band of goblins emerges from the shadows!",
            "A fierce dragon blocks your path!",
            "Undead warriors rise from the ground!",
            "A pack of wolves surrounds you!",
            "A mysterious knight challenges you to combat!"
        ],
        "exploration": [
            "You discover a hidden cave entrance!",
            "Ancient ruins lie ahead!",
            "A magical portal appears before you!",
            "You find a mysterious artifact!",
            "A secret passage reveals itself!"
        ],
        "social": [
            "A friendly merchant offers you goods!",
            "A wise old sage shares ancient knowledge!",
            "A mysterious stranger approaches you!",
            "Villagers ask for your help!",
            "A royal messenger delivers important news!"
        ],
        "random": [
            "A sudden storm approaches!",
            "You hear distant music!",
            "A shooting star streaks across the sky!",
            "The ground begins to tremble!",
            "A magical aura surrounds you!"
        ]
    }
    
    if event_type not in events:
        event_type = "random"
    
    chosen_event = random.choice(events[event_type])
    
    return {
        "type": event_type,
        "description": chosen_event,
        "severity": random.randint(1, 10),
        "duration": random.randint(1, 5)
    }

def calculate_combat_damage(attacker_level: int, weapon_power: int = 1) -> Dict[str, Any]:
    """
    Calculate combat damage for battles.
    
    Args:
        attacker_level: Level of the attacker
        weapon_power: Power multiplier of the weapon
    
    Returns:
        Dictionary with damage calculation
    """
    base_damage = random.randint(1, 10)
    level_bonus = attacker_level * 2
    weapon_bonus = weapon_power * random.randint(1, 5)
    
    total_damage = base_damage + level_bonus + weapon_bonus
    
    # Critical hit chance (5%)
    is_critical = random.random() < 0.05
    if is_critical:
        total_damage *= 2
    
    return {
        "damage": total_damage,
        "is_critical": is_critical,
        "base_damage": base_damage,
        "level_bonus": level_bonus,
        "weapon_bonus": weapon_bonus,
        "description": f"{'CRITICAL HIT! ' if is_critical else ''}Dealt {total_damage} damage"
    }

def generate_loot(monster_level: int, rarity: str = "common") -> Dict[str, Any]:
    """
    Generate loot based on monster level and rarity.
    
    Args:
        monster_level: Level of the defeated monster
        rarity: Rarity of the loot (common, uncommon, rare, epic, legendary)
    
    Returns:
        Dictionary with loot details
    """
    rarity_multipliers = {
        "common": 1,
        "uncommon": 2,
        "rare": 3,
        "epic": 5,
        "legendary": 10
    }
    
    base_gold = random.randint(1, 10) * monster_level
    rarity_bonus = rarity_multipliers.get(rarity, 1)
    total_gold = base_gold * rarity_bonus
    
    # Chance for special items based on rarity
    item_chance = {
        "common": 0.1,
        "uncommon": 0.3,
        "rare": 0.5,
        "epic": 0.7,
        "legendary": 0.9
    }
    
    has_special_item = random.random() < item_chance.get(rarity, 0.1)
    
    return {
        "gold": total_gold,
        "rarity": rarity,
        "has_special_item": has_special_item,
        "monster_level": monster_level,
        "description": f"Found {total_gold} gold pieces"
    } 