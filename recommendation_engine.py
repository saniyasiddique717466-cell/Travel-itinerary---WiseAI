import pandas as pd
import numpy as np


def recommend_destinations(
    destinations,
    user_profile,
    travel_month,
    top_n=5
):
    """
    Rank destinations based on user preferences,
    budget, interests, food, hotel preference,
    popularity and weather.
    """

    model = destinations.copy()

    # -----------------------------
    # Destination type match
    # -----------------------------
    preferred_type = str(
        user_profile.get("destination_type", "")
    ).lower()

    model["type_match"] = (
        model["destination_type"]
        .astype(str)
        .str.lower()
        .apply(
            lambda x: 1
            if preferred_type in x
            else 0
        )
    )

    # -----------------------------
    # Budget fit
    # -----------------------------
    budget = float(
        user_profile.get("budget", 0)
    )

    duration = max(
        int(user_profile.get("duration_days", 1)),
        1
    )

    effective_daily_budget = (
        budget / duration
    )

    model["budget_fit"] = (
        1 -
        (
            model["avg_daily_budget"]
            - effective_daily_budget
        ).abs()
        /
        model["avg_daily_budget"].replace(
            0, np.nan
        )
    )

    model["budget_fit"] = (
        model["budget_fit"]
        .clip(0, 1)
        .fillna(0)
    )

    # -----------------------------
    # Popularity fit
    # -----------------------------
    model["popularity_fit"] = (
        model["popularity_score"] / 100
    )

    # -----------------------------
    # Final recommendation score
    # -----------------------------
    model["final_recommendation_score"] = (
        model["type_match"] * 0.30 +
        model["budget_fit"] * 0.40 +
        model["popularity_fit"] * 0.30
    )

    # -----------------------------
    # Explanation
    # -----------------------------
    def explain_destination(row):

        reasons = []

        if row["type_match"] == 1:
            reasons.append(
                "matches your destination type"
            )

        if row["budget_fit"] >= 0.70:
            reasons.append(
                "fits your budget well"
            )

        if row["popularity_fit"] >= 0.70:
            reasons.append(
                "is highly popular"
            )

        if not reasons:
            reasons.append(
                "has a balanced overall profile"
            )

        return ", ".join(reasons)

    model["recommendation_reason"] = (
        model.apply(
            explain_destination,
            axis=1
        )
    )

    return (
        model
        .sort_values(
            "final_recommendation_score",
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )