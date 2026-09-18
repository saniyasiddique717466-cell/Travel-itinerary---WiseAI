import pandas as pd


def recommend_restaurants(
    restaurants,
    destination_id,
    user_profile,
    top_n=5
):
    """
    Rank restaurants based on:
    - Food preference
    - Rating
    - Price level
    - Distance
    - Family suitability
    """

    restaurants_subset = restaurants[
        restaurants["destination_id"] == destination_id
    ].copy()

    if restaurants_subset.empty:
        raise ValueError(
            f"No restaurants found for destination {destination_id}"
        )

    # -----------------------------
    # Food preference match
    # -----------------------------
    preferred_food = str(
        user_profile.get("preferred_food", "")
    ).lower()

    restaurants_subset["food_preference_match"] = (
        restaurants_subset["food_type"]
        .astype(str)
        .str.lower()
        .apply(
            lambda x: 1
            if preferred_food in x
            else 0
        )
    )

    # -----------------------------
    # Rating score
    # -----------------------------
    restaurants_subset["rating_score"] = (
        restaurants_subset["rating"] / 5
    )

    # -----------------------------
    # Price score
    # -----------------------------
    price_map = {
        "$": 1.0,
        "$$": 0.75,
        "$$$": 0.50
    }

    restaurants_subset["price_score"] = (
        restaurants_subset["price_level"]
        .map(price_map)
        .fillna(0.5)
    )

    # -----------------------------
    # Distance score
    # -----------------------------
    max_distance = restaurants_subset[
        "distance_from_center_km"
    ].max()

    if max_distance > 0:
        restaurants_subset["distance_score"] = (
            1 -
            restaurants_subset[
                "distance_from_center_km"
            ] / max_distance
        )
    else:
        restaurants_subset["distance_score"] = 1

    # -----------------------------
    # Family suitability
    # -----------------------------
    restaurants_subset["family_score"] = (
        restaurants_subset["family_friendly"]
        .astype(int)
    )

    # -----------------------------
    # Final recommendation score
    # -----------------------------
    restaurants_subset[
        "restaurant_recommendation_score"
    ] = (
        restaurants_subset["food_preference_match"] * 0.35 +
        restaurants_subset["rating_score"] * 0.25 +
        restaurants_subset["price_score"] * 0.15 +
        restaurants_subset["distance_score"] * 0.15 +
        restaurants_subset["family_score"] * 0.10
    )

    return (
        restaurants_subset
        .sort_values(
            "restaurant_recommendation_score",
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )