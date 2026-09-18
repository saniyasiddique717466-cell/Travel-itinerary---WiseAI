
# ✈️ TripWise AI
### Personalized Travel Intelligence & Recommendation System

TripWise AI is an intelligent travel planning platform that helps users create personalized travel experiences based on their destination, budget, duration, interests, and travel preferences.

The system uses Data Science, Machine Learning, and recommendation techniques to suggest destinations, hotels, attractions, restaurants, transportation, and suitable travel seasons.

---

## 🌍 Project Overview

Planning a trip often requires searching across multiple platforms for hotels, attractions, restaurants, transportation, weather, and costs.

TripWise AI brings these travel planning requirements together into one intelligent platform.

Users can enter their travel preferences and receive personalized recommendations and an organized itinerary.

---

## 🎯 Key Features

- 🌍 Personalized destination recommendations
- 🏨 Hotel recommendation system
- 📍 Attraction recommendation system
- 🍽️ Restaurant recommendation system
- 🌦️ Weather and season analysis
- 🚆 Transportation recommendations
- 💰 Trip cost estimation
- 🗓️ Day-by-day itinerary generation
- 🗺️ Interactive travel maps
- 🤖 AI-powered itinerary assistance (planned enhancement)
- 🎨 Interactive Streamlit web interface

---

## 🧠 Data Science & Machine Learning

The project uses recommendation scoring and machine learning techniques to support travel planning.

### Recommendation Engines

- Destination recommendation
- Hotel recommendation
- Attraction recommendation
- Restaurant recommendation
- Weather suitability analysis
- Transportation recommendation

### Cost Prediction

Machine learning models explored:

- Linear Regression
- Random Forest Regressor

Evaluation metrics:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

> Note: The current prototype uses synthetic data for development and testing. Results should not be interpreted as real-world travel cost predictions.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Pandas | Data processing |
| NumPy | Numerical computation |
| Scikit-learn | Machine learning |
| Streamlit | Web application |
| Plotly | Data visualization |
| Folium | Interactive maps |
| OpenPyXL | Excel data handling |

---

## 📂 Project Structure

```text
TripWise-AI/
│
├── data/
│   └── TripWise_AI_Dataset.xlsx
│
├── notebooks/
│   └── 01_EDA.ipynb
│
├── src/
│   ├── data_preprocessing.py
│   ├── recommendation_engine.py
│   ├── hotel_recommender.py
│   ├── attraction_recommender.py
│   ├── restaurant_recommender.py
│   ├── weather_engine.py
│   ├── cost_prediction.py
│   ├── route_optimizer.py
│   └── itinerary_generator.py
│
├── models/
│
├── app/
│   └── streamlit_app.py
│
├── api/
│
├── test_modules.py
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

The current prototype uses a synthetic, relational travel dataset containing information about:

- Destinations
- Attractions
- Hotels
- Restaurants
- Transportation
- Weather and seasons
- User preferences
- Trip history
- Activity costs

The dataset is intended for development, testing, and demonstrating the project architecture.

---

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project

```bash
cd TripWise-AI
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Streamlit application

```bash
streamlit run app/streamlit_app.py
```

---

## 🔬 Project Workflow

```text
User Travel Preferences
          ↓
Destination Recommendation
          ↓
Hotel, Attraction & Restaurant Recommendations
          ↓
Weather & Transportation Analysis
          ↓
Trip Cost Estimation
          ↓
Itinerary Generation
          ↓
Interactive Travel Experience
```

---

## 🔮 Future Enhancements

- Integration with real-world travel APIs
- Global destination coverage
- Live weather information
- Google Places and Maps integration
- Advanced route optimization
- AI chatbot for itinerary modifications
- Real-time hotel and restaurant information
- Cloud deployment
- User authentication and saved trips

---

## ⚠️ Disclaimer

This project is a prototype developed for educational and portfolio purposes.

The current dataset contains synthetic information. Recommendations, prices, and estimated costs should not be treated as verified live travel information.

---

## 👩‍💻 Author

**Saniya Begum**

Aspiring Data Analyst & Data Scientist

---

⭐ If you find this project interesting, feel free to explore and contribute!