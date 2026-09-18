from src.data_preprocessing import load_tripwise_data
from src.recommendation_engine import recommend_destinations
from src.hotel_recommender import recommend_hotels
from src.attraction_recommender import recommend_attractions
from src.restaurant_recommender import recommend_restaurants
from src.weather_engine import recommend_weather
from src.cost_prediction import train_cost_models, predict_trip_cost
from src.route_optimizer import (
    calculate_distance_matrix,
    estimate_travel_time,
    optimize_route,
    build_route_details
)
from src.itinerary_generator import (
    allocate_attractions_across_trip,
    generate_trip_itinerary
)

print("===================================")
print("   TripWise AI Module Test")
print("===================================")
print("ALL MODULES IMPORTED SUCCESSFULLY! ❤️")