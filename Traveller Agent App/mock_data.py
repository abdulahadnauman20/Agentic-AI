import random
from datetime import datetime, timedelta, date
from typing import List, Dict, Any
from models import (
    Flight, Hotel, Attraction, Restaurant, Destination, 
    TravelMood, BudgetLevel
)

class MockDataGenerator:
    """Generates realistic mock data for the travel system"""
    
    # Mock data sources
    AIRLINES = [
        "Emirates", "Qatar Airways", "Singapore Airlines", "ANA", "Lufthansa",
        "British Airways", "Air France", "KLM", "Turkish Airlines", "Etihad"
    ]
    
    AIRPORTS = {
        "New York": "JFK",
        "London": "LHR", 
        "Paris": "CDG",
        "Tokyo": "NRT",
        "Dubai": "DXB",
        "Singapore": "SIN",
        "Bangkok": "BKK",
        "Sydney": "SYD",
        "Rome": "FCO",
        "Barcelona": "BCN"
    }
    
    HOTEL_CHAINS = [
        "Marriott", "Hilton", "Hyatt", "InterContinental", "Four Seasons",
        "Ritz-Carlton", "W Hotels", "Sheraton", "Westin", "Renaissance"
    ]
    
    CUISINES = [
        "Italian", "French", "Japanese", "Thai", "Indian", "Chinese",
        "Mexican", "Mediterranean", "American", "Spanish", "Greek"
    ]
    
    ATTRACTION_CATEGORIES = [
        "Museum", "Historical Site", "Park", "Beach", "Mountain",
        "Shopping District", "Temple", "Castle", "Garden", "Market"
    ]

    @staticmethod
    def generate_flights(origin: str, destination: str, date: date, num_options: int = 5) -> List[Flight]:
        """Generate mock flight options"""
        flights = []
        
        for i in range(num_options):
            # Random departure time between 6 AM and 10 PM
            departure_hour = random.randint(6, 22)
            departure_minute = random.choice([0, 15, 30, 45])
            departure_time = datetime.combine(date, datetime.min.time().replace(hour=departure_hour, minute=departure_minute))
            
            # Flight duration between 2-12 hours
            duration_hours = random.randint(2, 12)
            arrival_time = departure_time + timedelta(hours=duration_hours)
            
            # Price based on duration and airline
            base_price = 200 + (duration_hours * 50)
            price_variation = random.uniform(0.8, 1.5)
            price = round(base_price * price_variation, 2)
            
            flight = Flight(
                airline=random.choice(MockDataGenerator.AIRLINES),
                flight_number=f"{random.choice(['EK', 'QR', 'SQ', 'NH', 'LH'])}{random.randint(100, 999)}",
                departure_airport=MockDataGenerator.AIRPORTS.get(origin, "JFK"),
                arrival_airport=MockDataGenerator.AIRPORTS.get(destination, "LHR"),
                departure_time=departure_time,
                arrival_time=arrival_time,
                price=price,
                duration=f"{duration_hours}h {random.randint(0, 59)}m",
                stops=random.choice([0, 1, 2]),
                cabin_class=random.choice(["Economy", "Premium Economy", "Business", "First"]),
                available_seats=random.randint(5, 50)
            )
            flights.append(flight)
        
        return sorted(flights, key=lambda x: x.price)

    @staticmethod
    def generate_hotels(destination: str, budget: BudgetLevel, num_options: int = 5) -> List[Hotel]:
        """Generate mock hotel options"""
        hotels = []
        
        price_ranges = {
            BudgetLevel.BUDGET: (50, 150),
            BudgetLevel.MODERATE: (150, 400),
            BudgetLevel.LUXURY: (400, 1000)
        }
        
        min_price, max_price = price_ranges[budget]
        
        for i in range(num_options):
            price = round(random.uniform(min_price, max_price), 2)
            rating = round(random.uniform(3.0, 5.0), 1)
            
            # Amenities based on budget
            base_amenities = ["WiFi", "Air Conditioning"]
            if budget == BudgetLevel.MODERATE:
                base_amenities.extend(["Pool", "Restaurant", "Gym"])
            elif budget == BudgetLevel.LUXURY:
                base_amenities.extend(["Spa", "Concierge", "Room Service", "Pool", "Restaurant", "Gym", "Business Center"])
            
            hotel = Hotel(
                name=f"{random.choice(MockDataGenerator.HOTEL_CHAINS)} {destination}",
                location=f"Downtown {destination}",
                rating=rating,
                price_per_night=price,
                amenities=base_amenities + random.sample(["Parking", "Shuttle", "Bar", "Laundry"], random.randint(0, 2)),
                room_types=random.sample(["Standard", "Deluxe", "Suite", "Executive"], random.randint(2, 4)),
                description=f"Comfortable accommodation in the heart of {destination} with excellent amenities and service.",
                distance_from_center=f"{random.randint(1, 10)} km"
            )
            hotels.append(hotel)
        
        return sorted(hotels, key=lambda x: x.price_per_night)

    @staticmethod
    def generate_attractions(destination: str, mood: TravelMood, num_options: int = 8) -> List[Attraction]:
        """Generate mock attractions based on destination and mood"""
        attractions = []
        
        # Attraction types based on mood
        mood_attractions = {
            TravelMood.ADVENTURE: ["Mountain", "Park", "Beach", "Historical Site"],
            TravelMood.RELAXATION: ["Beach", "Garden", "Park", "Spa"],
            TravelMood.CULTURE: ["Museum", "Historical Site", "Temple", "Castle"],
            TravelMood.FOOD: ["Market", "Restaurant District", "Food Tour"],
            TravelMood.NATURE: ["Park", "Garden", "Mountain", "Beach"],
            TravelMood.URBAN: ["Shopping District", "Museum", "Market", "Historical Site"],
            TravelMood.BEACH: ["Beach", "Water Sports", "Marina"],
            TravelMood.MOUNTAINS: ["Mountain", "Park", "Hiking Trail"]
        }
        
        categories = mood_attractions.get(mood, MockDataGenerator.ATTRACTION_CATEGORIES)
        
        attraction_names = {
            "Museum": [f"{destination} National Museum", f"Modern Art Gallery", f"History Museum"],
            "Historical Site": [f"Ancient Ruins", f"Historic District", f"Old Town"],
            "Park": [f"Central Park", f"Botanical Gardens", f"City Park"],
            "Beach": [f"Golden Beach", f"Crystal Bay", f"Sunset Beach"],
            "Mountain": [f"Peak View", f"Mountain Trail", f"Summit Point"],
            "Shopping District": [f"Shopping Mall", f"Market Street", f"Boutique District"],
            "Temple": [f"Ancient Temple", f"Peace Pagoda", f"Meditation Center"],
            "Castle": [f"Royal Castle", f"Fortress", f"Palace"],
            "Garden": [f"Botanical Gardens", f"Zen Garden", f"Flower Park"],
            "Market": [f"Local Market", f"Artisan Market", f"Food Market"]
        }
        
        for i in range(num_options):
            category = random.choice(categories)
            name = random.choice(attraction_names.get(category, [f"{category} in {destination}"]))
            
            attraction = Attraction(
                name=name,
                category=category,
                description=f"Experience the best of {destination} at this amazing {category.lower()}.",
                location=f"{destination} City Center",
                rating=round(random.uniform(3.5, 5.0), 1),
                price_range=random.choice(["Free", "$", "$$", "$$$"]),
                opening_hours=f"{random.randint(8, 10)}:00 AM - {random.randint(6, 10)}:00 PM",
                best_time_to_visit=random.choice(["Morning", "Afternoon", "Evening", "All day"]),
                tips=random.sample([
                    "Visit early to avoid crowds",
                    "Bring comfortable shoes",
                    "Don't forget your camera",
                    "Check the weather forecast",
                    "Book tickets in advance"
                ], random.randint(2, 4))
            )
            attractions.append(attraction)
        
        return attractions

    @staticmethod
    def generate_restaurants(destination: str, num_options: int = 6) -> List[Restaurant]:
        """Generate mock restaurant options"""
        restaurants = []
        
        restaurant_names = [
            f"La {destination} Bistro", f"{destination} Grill", f"Spice Garden",
            f"Ocean View", f"Golden Dragon", f"Pasta Palace", f"Fresh Market",
            f"Royal Kitchen", f"Sunset Cafe", f"Urban Eats"
        ]
        
        for i in range(num_options):
            cuisine = random.choice(MockDataGenerator.CUISINES)
            name = random.choice(restaurant_names)
            
            restaurant = Restaurant(
                name=name,
                cuisine=cuisine,
                rating=round(random.uniform(3.5, 5.0), 1),
                price_range=random.choice(["$", "$$", "$$$", "$$$$"]),
                location=f"{destination} Downtown",
                description=f"Authentic {cuisine.lower()} cuisine in a beautiful setting.",
                specialties=random.sample([
                    "Signature Pasta", "Fresh Seafood", "Local Specialties",
                    "Chef's Special", "Seasonal Menu", "Traditional Dishes"
                ], random.randint(2, 4)),
                opening_hours=f"{random.randint(7, 11)}:00 AM - {random.randint(9, 11)}:00 PM",
                reservation_required=random.choice([True, False])
            )
            restaurants.append(restaurant)
        
        return restaurants

    @staticmethod
    def generate_destinations() -> List[Destination]:
        """Generate mock destination data"""
        destinations_data = [
            {
                "name": "Bali",
                "country": "Indonesia",
                "description": "Tropical paradise with beautiful beaches, temples, and culture",
                "best_time_to_visit": "April to October",
                "average_temperature": "26°C (79°F)",
                "activities": ["Beach relaxation", "Temple visits", "Rice terrace tours", "Water sports"],
                "mood_suitability": [TravelMood.RELAXATION, TravelMood.CULTURE, TravelMood.BEACH],
                "budget_range": BudgetLevel.MODERATE
            },
            {
                "name": "Tokyo",
                "country": "Japan",
                "description": "Modern metropolis blending technology with traditional culture",
                "best_time_to_visit": "March to May and September to November",
                "average_temperature": "15°C (59°F)",
                "activities": ["Sightseeing", "Shopping", "Food tours", "Temple visits"],
                "mood_suitability": [TravelMood.URBAN, TravelMood.CULTURE, TravelMood.FOOD],
                "budget_range": BudgetLevel.MODERATE
            },
            {
                "name": "Paris",
                "country": "France",
                "description": "City of love with iconic landmarks and world-class cuisine",
                "best_time_to_visit": "April to June and September to October",
                "average_temperature": "12°C (54°F)",
                "activities": ["Museum visits", "Eiffel Tower", "Seine River cruise", "Shopping"],
                "mood_suitability": [TravelMood.CULTURE, TravelMood.FOOD, TravelMood.URBAN],
                "budget_range": BudgetLevel.MODERATE
            },
            {
                "name": "New York",
                "country": "USA",
                "description": "The city that never sleeps with endless entertainment options",
                "best_time_to_visit": "April to June and September to November",
                "average_temperature": "13°C (55°F)",
                "activities": ["Broadway shows", "Museum visits", "Central Park", "Shopping"],
                "mood_suitability": [TravelMood.URBAN, TravelMood.CULTURE, TravelMood.FOOD],
                "budget_range": BudgetLevel.MODERATE
            },
            {
                "name": "Swiss Alps",
                "country": "Switzerland",
                "description": "Breathtaking mountain scenery perfect for adventure and relaxation",
                "best_time_to_visit": "December to March (skiing) or June to September (hiking)",
                "average_temperature": "5°C (41°F)",
                "activities": ["Skiing", "Hiking", "Mountain biking", "Scenic train rides"],
                "mood_suitability": [TravelMood.ADVENTURE, TravelMood.MOUNTAINS, TravelMood.NATURE],
                "budget_range": BudgetLevel.LUXURY
            }
        ]
        
        destinations = []
        for data in destinations_data:
            destination = Destination(**data)
            destinations.append(destination)
        
        return destinations 