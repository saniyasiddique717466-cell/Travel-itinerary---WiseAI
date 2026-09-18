import pandas as pd


def recommend_attractions(
    attractions,
    destination_id,
    user_profile,
    top_n=10
):
    attractions_subset = attractions[
        attractions["destination_id"] == destination_id
    ].copy()

    if attractions_subset.empty:
        raise ValueError(
            f"No attractions found for destination {destination_id}"
        )

    preferred_interest = str(
        user_profile.get("interests", "")
    ).lower()

    attractions_subset["interest_match"] = (
        attractions_subset["category"]
        .astype(str)
        .str.lower()
        .apply(
            lambda x: 1 if preferred_interest in x else 0
        )
    )

    attractions_subset["rating_score"] = (
        attractions_subset["rating"] / 5
    )

    attractions_subset["popularity_score_norm"] = (
        attractions_subset["popularity_score"] / 100
    )

    activity_level = str(
        user_profile.get("activity_level", "")
    ).lower()

    activity_map = {
        "low": 1,
        "moderate": 2,
        "high": 3
    }

    user_activity_score = activity_map.get(
        activity_level,
        2
    )

    attractions_subset["activity_match"] = (
        1
        - (
            attractions_subset["adventure_level"]
            - user_activity_score
        ).abs() / 2
    ).clip(0, 1)

    max_cost = attractions_subset[
        "estimated_spend"
    ].max()

    min_cost = attractions_subset[
        "estimated_spend"
    ].min()

    if max_cost > min_cost:
        attractions_subset["cost_score"] = (
            1
            - (
                attractions_subset["estimated_spend"]
                - min_cost
            )
            / (max_cost - min_cost)
        )
    else:
        attractions_subset["cost_score"] = 1

    attractions_subset[
        "attraction_recommendation_score"
    ] = (
        attractions_subset["interest_match"] * 0.35
        + attractions_subset["rating_score"] * 0.20
        + attractions_subset["popularity_score_norm"] * 0.15
        + attractions_subset["activity_match"] * 0.15
        + attractions_subset["cost_score"] * 0.15
    )

    return (
        attractions_subset
        .sort_values(
            "attraction_recommendation_score",
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )