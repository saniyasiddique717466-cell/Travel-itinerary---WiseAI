import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import haversine_distances


def calculate_distance_matrix(coordinates):
    """
    Calculate pairwise geographical distances
    using the Haversine formula.

    coordinates:
        List of [latitude, longitude] pairs.

    Returns:
        Distance matrix in kilometers.
    """

    coordinates = np.radians(
        np.array(coordinates)
    )

    distance_matrix = (
        haversine_distances(coordinates)
        * 6371
    )

    return distance_matrix


def estimate_travel_time(
    distance_km,
    avg_speed_kmph=30
):
    """
    Estimate travel time in hours.
    """

    if avg_speed_kmph <= 0:
        raise ValueError(
            "Average speed must be greater than zero."
        )

    return round(
        distance_km / avg_speed_kmph,
        2
    )


def optimize_route(
    route_attractions,
    distance_matrix
):
    """
    Optimize attraction order using a
    nearest-neighbor routing heuristic.

    The highest-scoring attraction is used
    as the starting point.
    """

    if route_attractions.empty:
        return []

    attractions = (
        route_attractions
        .reset_index(drop=True)
    )

    start_index = (
        attractions[
            "attraction_recommendation_score"
        ]
        .idxmax()
    )

    unvisited = set(
        range(len(attractions))
    )

    route = [start_index]

    unvisited.remove(
        start_index
    )

    current = start_index

    while unvisited:

        next_index = min(
            unvisited,
            key=lambda index:
                distance_matrix[
                    current,
                    index
                ]
        )

        route.append(
            next_index
        )

        unvisited.remove(
            next_index
        )

        current = next_index

    return [
        attractions.iloc[index][
            "attraction_id"
        ]
        for index in route
    ]


def build_route_details(
    route_attractions,
    hotel_latitude,
    hotel_longitude
):
    """
    Build an optimized route beginning
    and ending at the selected hotel.
    """

    if route_attractions.empty:
        return {
            "route": [],
            "total_distance_km": 0,
            "estimated_travel_time_hours": 0
        }

    attractions = (
        route_attractions
        .reset_index(drop=True)
    )

    coordinates = [
        [
            hotel_latitude,
            hotel_longitude
        ]
    ]

    coordinates.extend(
        attractions[
            [
                "latitude",
                "longitude"
            ]
        ].values.tolist()
    )

    coordinates.append(
        [
            hotel_latitude,
            hotel_longitude
        ]
    )

    distance_matrix = calculate_distance_matrix(
        coordinates
    )

    attraction_matrix = (
        distance_matrix[
            1:-1,
            1:-1
        ]
    )

    optimized_ids = optimize_route(
        attractions,
        attraction_matrix
    )

    ordered_attractions = (
        attractions
        .set_index("attraction_id")
        .loc[optimized_ids]
        .reset_index()
    )

    route_names = [
        "HOTEL"
    ]

    route_names.extend(
        ordered_attractions[
            "attraction_name"
        ].tolist()
    )

    route_names.append(
        "HOTEL"
    )

    total_distance = 0

    previous_coordinate = coordinates[0]

    for _, attraction in (
        ordered_attractions.iterrows()
    ):

        current_coordinate = [
            attraction["latitude"],
            attraction["longitude"]
        ]

        segment_distance = (
            calculate_distance_matrix(
                [
                    previous_coordinate,
                    current_coordinate
                ]
            )[0, 1]
        )

        total_distance += (
            segment_distance
        )

        previous_coordinate = (
            current_coordinate
        )

    final_distance = (
        calculate_distance_matrix(
            [
                previous_coordinate,
                coordinates[-1]
            ]
        )[0, 1]
    )

    total_distance += final_distance

    return {
        "route": route_names,
        "total_distance_km": round(
            float(total_distance),
            2
        ),
        "estimated_travel_time_hours":
            estimate_travel_time(
                total_distance
            )
    }