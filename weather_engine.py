import pandas as pd


def recommend_weather(
    weather,
    destination_id,
    travel_month,
    top_n=1
):
    """
    Recommend weather conditions for a destination
    and travel month.
    """

    month_map = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }

    if isinstance(travel_month, int):
        travel_month = month_map.get(travel_month)

    if travel_month is None:
        raise ValueError(
            "travel_month must be between 1 and 12."
        )

    weather_subset = weather[
        (weather["destination_id"] == destination_id) &
        (
            weather["month"]
            .astype(str)
            .str.lower()
            == str(travel_month).lower()
        )
    ].copy()

    if weather_subset.empty:
        raise ValueError(
            f"No weather data found for "
            f"{destination_id} and {travel_month}"
        )

    # Normalize weather-related scores
    weather_subset["weather_score_normalized"] = (
        weather_subset["weather_score"] / 100
    )

    weather_subset["outdoor_activity_score_normalized"] = (
        weather_subset["outdoor_activity_score"] / 100
    )

    # Combined recommendation score
    weather_subset["weather_recommendation_score"] = (
        weather_subset["weather_score_normalized"] * 0.60 +
        weather_subset[
            "outdoor_activity_score_normalized"
        ] * 0.40
    )

    return (
        weather_subset
        .sort_values(
            "weather_recommendation_score",
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )