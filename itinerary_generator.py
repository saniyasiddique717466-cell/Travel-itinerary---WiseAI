import pandas as pd


def allocate_attractions_across_trip(
    attractions,
    trip_days,
    max_sightseeing_hours=6
):
    """
    Distribute recommended attractions across
    the trip while keeping daily sightseeing
    time reasonable.
    """

    if attractions.empty:
        return {
            day: []
            for day in range(1, trip_days + 1)
        }

    attractions = (
        attractions
        .sort_values(
            "attraction_recommendation_score",
            ascending=False
        )
        .reset_index(drop=True)
    )

    daily_plans = {
        day: []
        for day in range(1, trip_days + 1)
    }

    daily_hours = {
        day: 0
        for day in range(1, trip_days + 1)
    }

    for _, attraction in attractions.iterrows():

        suitable_days = [
            day
            for day in range(1, trip_days + 1)
            if (
                daily_hours[day]
                + attraction["avg_visit_hours"]
                <= max_sightseeing_hours
            )
        ]

        if suitable_days:

            selected_day = min(
                suitable_days,
                key=lambda day:
                    daily_hours[day]
            )

        else:

            selected_day = min(
                daily_hours,
                key=daily_hours.get
            )

        daily_plans[selected_day].append(
            attraction["attraction_id"]
        )

        daily_hours[selected_day] += (
            attraction["avg_visit_hours"]
        )

    return daily_plans


def generate_trip_itinerary(
    attractions,
    hotel,
    trip_days=6,
    max_sightseeing_hours=6
):
    """
    Generate a day-by-day itinerary.

    Each day contains:
    - Hotel starting point
    - Recommended attractions
    - Visit duration
    - Estimated sightseeing hours
    """

    if trip_days <= 0:
        raise ValueError(
            "trip_days must be greater than zero."
        )

    if attractions.empty:
        return []

    selected_attractions = (
        attractions
        .copy()
        .sort_values(
            "attraction_recommendation_score",
            ascending=False
        )
    )

    daily_plans = allocate_attractions_across_trip(
        selected_attractions,
        trip_days,
        max_sightseeing_hours
    )

    attraction_lookup = (
        selected_attractions
        .set_index("attraction_id")
    )

    itinerary = []

    for day in range(1, trip_days + 1):

        day_attractions = []

        for attraction_id in daily_plans[day]:

            attraction = (
                attraction_lookup
                .loc[attraction_id]
            )

            day_attractions.append({
                "attraction_id":
                    attraction_id,

                "attraction_name":
                    attraction["attraction_name"],

                "category":
                    attraction["category"],

                "rating":
                    attraction["rating"],

                "visit_hours":
                    attraction["avg_visit_hours"],

                "entry_fee":
                    attraction["entry_fee"],

                "latitude":
                    attraction["latitude"],

                "longitude":
                    attraction["longitude"]
            })

        total_hours = sum(
            attraction["visit_hours"]
            for attraction in day_attractions
        )

        itinerary.append({
            "day": day,
            "hotel": hotel,
            "attractions": day_attractions,
            "total_sightseeing_hours":
                round(total_hours, 2)
        })

    return itinerary