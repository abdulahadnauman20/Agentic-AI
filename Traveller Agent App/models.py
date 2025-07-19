from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum
import uuid

class TravelMood(Enum):
    ADVENTURE = "adventure"
    RELAXATION = "relaxation"
    CULTURE = "culture"
    FOOD = "food"
    NATURE = "nature"
    URBAN = "urban"
    BEACH = "beach"
    MOUNTAINS = "mountains"

class BudgetLevel(Enum):
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"

@dataclass
class TravelRequest:
    """Represents a travel request from a user"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_name: str = ""
    destination_preferences: List[str] = field(default_factory=list)
    mood: TravelMood = TravelMood.ADVENTURE
    budget: BudgetLevel = BudgetLevel.MODERATE
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    num_travelers: int = 1
    special_requirements: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Destination:
    """Represents a travel destination"""
    name: str
    country: str
    description: str
    best_time_to_visit: str
    average_temperature: str
    activities: List[str] = field(default_factory=list)
    mood_suitability: List[TravelMood] = field(default_factory=list)
    budget_range: BudgetLevel = BudgetLevel.MODERATE
    image_url: Optional[str] = None

@dataclass
class Flight:
    """Represents a flight option"""
    airline: str
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    duration: str
    stops: int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    cabin_class: str = "Economy"
    available_seats: int = 100

@dataclass
class Hotel:
    """Represents a hotel option"""
    name: str
    location: str
    rating: float
    price_per_night: float
    description: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    amenities: List[str] = field(default_factory=list)
    room_types: List[str] = field(default_factory=list)
    image_url: Optional[str] = None
    distance_from_center: str = "5 km"

@dataclass
class Attraction:
    """Represents a tourist attraction"""
    name: str
    category: str  # museum, restaurant, park, etc.
    description: str
    location: str
    rating: float
    price_range: str
    opening_hours: str
    best_time_to_visit: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tips: List[str] = field(default_factory=list)

@dataclass
class Restaurant:
    """Represents a restaurant"""
    name: str
    cuisine: str
    rating: float
    price_range: str
    location: str
    description: str
    opening_hours: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    specialties: List[str] = field(default_factory=list)
    reservation_required: bool = False

@dataclass
class TravelPlan:
    """Complete travel plan with all components"""
    request: TravelRequest
    destination: Destination
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    flights: List[Flight] = field(default_factory=list)
    hotel: Optional[Hotel] = None
    attractions: List[Attraction] = field(default_factory=list)
    restaurants: List[Restaurant] = field(default_factory=list)
    total_cost: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "draft"

@dataclass
class AgentResponse:
    """Standard response format for all agents"""
    success: bool
    message: str
    data: Optional[Any] = None
    agent_name: str = ""
    timestamp: datetime = field(default_factory=datetime.now) 