import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def train_cost_models(
    trip_history,
    user_preferences,
    destinations
):
    """
    Train and compare trip-cost prediction models.

    Returns:
        best_model
        comparison_results
    """

    # Merge trip history with user preferences
    model_data = trip_history.merge(
        user_preferences,
        on="user_id",
        how="left"
    )

    # Add destination information
    model_data = model_data.merge(
        destinations[
            [
                "destination_id",
                "avg_daily_budget"
            ]
        ],
        on="destination_id",
        how="left"
    )

    # Features
    features = [
        "travelers",
        "budget",
        "duration_days",
        "avg_daily_budget"
    ]

    X = model_data[features]
    y = model_data["trip_cost"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    # Linear Regression
    linear_model = LinearRegression()

    linear_model.fit(
        X_train,
        y_train
    )

    linear_predictions = linear_model.predict(
        X_test
    )

    # Random Forest
    random_forest_model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    random_forest_model.fit(
        X_train,
        y_train
    )

    random_forest_predictions = (
        random_forest_model.predict(X_test)
    )

    # Model evaluation
    results = []

    for model_name, predictions in [
        ("Linear Regression", linear_predictions),
        ("Random Forest", random_forest_predictions)
    ]:

        results.append({
            "Model": model_name,
            "MAE": mean_absolute_error(
                y_test,
                predictions
            ),
            "RMSE": np.sqrt(
                mean_squared_error(
                    y_test,
                    predictions
                )
            ),
            "R2": r2_score(
                y_test,
                predictions
            )
        })

    comparison_results = pd.DataFrame(
        results
    )

    # Select model with lowest MAE
    best_model_name = (
        comparison_results
        .sort_values("MAE")
        .iloc[0]["Model"]
    )

    if best_model_name == "Linear Regression":
        best_model = linear_model
    else:
        best_model = random_forest_model

    return (
        best_model,
        comparison_results
    )


def predict_trip_cost(
    model,
    travelers,
    budget,
    duration_days,
    avg_daily_budget
):
    """
    Predict estimated trip cost for a new trip.
    """

    input_data = pd.DataFrame({
        "travelers": [travelers],
        "budget": [budget],
        "duration_days": [duration_days],
        "avg_daily_budget": [avg_daily_budget]
    })

    prediction = model.predict(
        input_data
    )[0]

    return round(
        float(prediction),
        2
    )
