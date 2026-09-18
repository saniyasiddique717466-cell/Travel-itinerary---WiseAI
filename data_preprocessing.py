import pandas as pd
from pathlib import Path


def load_tripwise_data(data_path=None):
    """
    Load all TripWise AI datasets from the Excel workbook.

    Returns:
        Dictionary containing all project dataframes.
    """

    if data_path is None:
        data_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "TripWise_AI_Dataset.xlsx"
        )

    data_path = Path(data_path)

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {data_path}"
        )

    sheets = pd.read_excel(
        data_path,
        sheet_name=None
    )

    required_sheets = [
        "destinations",
        "attractions",
        "hotels",
        "restaurants",
        "transportation",
        "weather_season",
        "user_preferences",
        "trip_history",
        "activity_costs"
    ]

    missing_sheets = [
        sheet
        for sheet in required_sheets
        if sheet not in sheets
    ]

    if missing_sheets:
        raise ValueError(
            "Missing required sheets: "
            + ", ".join(missing_sheets)
        )

    data = {
        sheet: sheets[sheet].copy()
        for sheet in required_sheets
    }

    # Basic cleanup
    for name, df in data.items():

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # Remove completely empty rows
        data[name] = (
            df.dropna(how="all")
            .reset_index(drop=True)
        )

    return data


def validate_tripwise_data(data):
    """
    Perform basic structural validation
    on loaded TripWise datasets.
    """

    required_columns = {
        "destinations": [
            "destination_id",
            "destination_name",
            "country"
        ],
        "attractions": [
            "attraction_id",
            "destination_id",
            "attraction_name"
        ],
        "hotels": [
            "hotel_id",
            "destination_id",
            "hotel_name"
        ],
        "restaurants": [
            "restaurant_id",
            "destination_id",
            "restaurant_name"
        ],
        "transportation": [
            "transport_id",
            "source",
            "destination"
        ],
        "weather_season": [
            "destination_id",
            "month"
        ],
        "user_preferences": [
            "user_id",
            "budget",
            "duration_days"
        ],
        "trip_history": [
            "trip_id",
            "user_id",
            "destination_id"
        ],
        "activity_costs": [
            "activity_id",
            "attraction_id"
        ]
    }

    for sheet, columns in required_columns.items():

        if sheet not in data:
            raise ValueError(
                f"Dataset '{sheet}' is missing."
            )

        missing_columns = [
            column
            for column in columns
            if column not in data[sheet].columns
        ]

        if missing_columns:
            raise ValueError(
                f"{sheet} is missing columns: "
                + ", ".join(missing_columns)
            )

    return True