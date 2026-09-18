
import streamlit as st
from pathlib import Path
import sys

# Allow imports from the project root
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.data_preprocessing import load_tripwise_data, validate_tripwise_data

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TripWise AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #F8F3ED;
        color: #40362F;
    }

    [data-testid="stSidebar"] {
        background-color: #EDE2D5;
    }

    h1, h2, h3 {
        color: #49382D;
        font-family: Georgia, serif;
    }

    .hero {
        background: linear-gradient(
            135deg,
            #DCC7B2,
            #F4E8DA
        );
        padding: 42px;
        border-radius: 25px;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 46px;
        margin-bottom: 8px;
    }

    .hero p {
        font-size: 18px;
        color: #6D5A4B;
    }

    .info-card {
        background-color: #FFFDF9;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #E5D7C8;
        margin-bottom: 15px;
    }

    .stButton > button {
        background-color: #8B6F55;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 22px;
    }

    .stButton > button:hover {
        background-color: #6F5540;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

@st.cache_data
def get_data():
    data = load_tripwise_data()
    validate_tripwise_data(data)
    return data

data = get_data()

destinations = data["destinations"]

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("## ✈️ TripWise AI")
    st.caption("Your intelligent travel companion")

    st.divider()

    st.markdown("### Plan your journey")

    destination = st.selectbox(
        "Where do you want to go?",
        sorted(destinations["destination_name"].unique())
    )

    duration = st.slider(
        "Trip duration (days)",
        min_value=1,
        max_value=30,
        value=6
    )

    travelers = st.number_input(
        "Number of travelers",
        min_value=1,
        max_value=20,
        value=2
    )

    budget = st.number_input(
        "Total budget",
        min_value=1000,
        max_value=10000000,
        value=70000,
        step=1000
    )

    travel_month = st.selectbox(
        "Travel month",
        list(range(1, 13)),
        index=5,
        format_func=lambda x: [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ][x - 1]
    )

    hotel_preference = st.selectbox(
        "Hotel preference",
        ["Budget", "3-Star", "4-Star", "5-Star"]
    )

    interests = st.selectbox(
        "Main interest",
        ["Nature", "Beach", "Food", "Adventure", "Nightlife"]
    )

    preferred_food = st.selectbox(
        "Food preference",
        ["Vegetarian", "Non-Vegetarian"]
    )

    activity_level = st.selectbox(
        "Activity level",
        ["Low", "Moderate", "High"]
    )

    generate_plan = st.button(
        "✨ Generate Travel Plan",
        use_container_width=True
    )

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>Travel beautifully. Explore intelligently.</h1>
    <p>
        Discover personalized destinations, hotels, attractions,
        food experiences, and intelligent travel itineraries.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("## Where will your next adventure take you?")

st.write(
    "Create a personalized travel experience based on your "
    "preferences, budget, and travel style."
)

# --------------------------------------------------
# DESTINATION INFORMATION
# --------------------------------------------------

selected_destination = destinations[
    destinations["destination_name"] == destination
].iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="info-card">
            <h3>📍 Destination</h3>
            <h2>{destination}</h2>
            <p>{selected_destination["country"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="info-card">
            <h3>📅 Duration</h3>
            <h2>{duration} Days</h2>
            <p>{travelers} Traveler(s)</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="info-card">
            <h3>💰 Budget</h3>
            <h2>₹{budget:,.0f}</h2>
            <p>Personalized travel planning</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# PLAN GENERATION
# --------------------------------------------------

if generate_plan:
    destination_id = selected_destination["destination_id"]

    user_profile = {
        "destination_type": selected_destination["destination_type"],
        "budget": budget,
        "duration_days": duration,
        "travelers": travelers,
        "hotel_preference": hotel_preference,
        "interests": interests,
        "preferred_food": preferred_food,
        "activity_level": activity_level
    }

    st.session_state["destination_id"] = destination_id
    st.session_state["user_profile"] = user_profile
    st.session_state["travel_month"] = travel_month

    st.success("Your travel preferences have been saved!")

    st.markdown("## 🌍 Your TripWise AI workspace")

    tab1, tab2, tab3 = st.tabs([
        "🏨 Hotels",
        "📍 Attractions",
        "🍽️ Restaurants"
    ])

    from src.hotel_recommender import recommend_hotels
    from src.attraction_recommender import recommend_attractions
    from src.restaurant_recommender import recommend_restaurants

    with tab1:
        hotels = recommend_hotels(
            data["hotels"],
            destination_id,
            user_profile,
            top_n=5
        )

        st.dataframe(
            hotels[
                [
                    "hotel_name",
                    "hotel_type",
                    "rating",
                    "price_per_night",
                    "hotel_recommendation_score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    with tab2:
        attractions = recommend_attractions(
            data["attractions"],
            destination_id,
            user_profile,
            top_n=10
        )

        st.dataframe(
            attractions[
                [
                    "attraction_name",
                    "category",
                    "rating",
                    "avg_visit_hours",
                    "attraction_recommendation_score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    with tab3:
        restaurants = recommend_restaurants(
            data["restaurants"],
            destination_id,
            user_profile,
            top_n=5
        )

        st.dataframe(
            restaurants[
                [
                    "restaurant_name",
                    "cuisine",
                    "food_type",
                    "rating",
                    "restaurant_recommendation_score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )
else:
    st.markdown("""
    <div class="info-card">
        <h3>✨ Your personalized journey starts here</h3>
        <p>
            Select your travel preferences from the sidebar,
            then click <b>Generate Travel Plan</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)