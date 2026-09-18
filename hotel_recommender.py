import pandas as pd


def recommend_hotels(
    hotels,
    destination_id,
    user_profile,
    top_n=5
):
    """
    Rank hotels based on:
    - Preferred hotel type
    - Rating
    - Price
    - Distance from center
    - Breakfast availability
    """

    hotels_subset = hotels[
        hotels["destination_id"] == destination_id
    ].copy()

    if hotels_subset.empty:
        raise ValueError(
            f"No hotels found for destination {destination_id}"
        )

    preferred_hotel = str(
        user_profile.get("hotel_preference", "")
    ).lower()

    # -----------------------------
    # Hotel preference match
    # -----------------------------
    hotels_subset["hotel_preference_match"] = (
        hotels_subset["hotel_type"]
        .astype(str)
        .str.lower()
        .apply(
            lambda x: 1
            if preferred_hotel in x
            else 0
        )
    )

    # -----------------------------
    # Rating score
    # -----------------------------
    hotels_subset["rating_score"] = (
        hotels_subset["rating"] / 5
    )

    # -----------------------------
    # Price score
    # Lower price = higher score
    # -----------------------------
    max_price = hotels_subset[
        "price_per_night"
    ].max()

    min_price = hotels_subset[
        "price_per_night"
    ].min()

    if max_price > min_price:
        hotels_subset["price_score"] = (
            1 -
            (
                hotels_subset["price_per_night"]
                - min_price
            )
            /
            (max_price - min_price)
        )
    else:
        hotels_subset["price_score"] = 1

    # -----------------------------
    # Distance score
    # -----------------------------
    max_distance = hotels_subset[
        "distance_from_center_km"
    ].max()

    if max_distance > 0:
        hotels_subset["distance_score"] = (
            1 -
            hotels_subset[
                "distance_from_center_km"
            ] / max_distance
        )
    else:
        hotels_subset["distance_score"] = 1

    # -----------------------------
    # Breakfast score
    # -----------------------------
    hotels_subset["breakfast_score"] = (
        hotels_subset["breakfast_included"]
        .astype(int)
    )

    # -----------------------------
    # Final score
    # -----------------------------
    hotels_subset["hotel_recommendation_score"] = (
        hotels_subset["hotel_preference_match"] * 0.35 +
        hotels_subset["rating_score"] * 0.25 +
        hotels_subset["price_score"] * 0.15 +
        hotels_subset["distance_score"] * 0.15 +
        hotels_subset["breakfast_score"] * 0.10
    )

    return (
        hotels_subset
        .sort_values(
            "hotel_recommendation_score",
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )