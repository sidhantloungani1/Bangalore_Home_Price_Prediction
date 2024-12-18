import json
import pickle
import numpy as np

# Global variables
__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())  # Match location
    except ValueError:
        loc_index = -1  # If location not found

    x = np.zeros(len(__data_columns))  # Initialize input array
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1  # Set location-specific index to 1

    try:
        prediction = round(__model.predict([x])[0], 2)
        return prediction
    except Exception as e:
        print(f"Prediction error: {e}")
        return None

def get_location_names():
    """
    Returns the list of available locations.
    """
    global __locations
    return __locations


def load_saved_artifacts():
    global __data_columns
    global __locations
    global __model

    print("Loading JSON File...")
    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        if __data_columns is None:
            print("Error: 'data_columns' key not found in JSON!")
        else:
            print("Loaded Data Columns:", __data_columns[:5])
            __locations = __data_columns[3:]
            print("Loaded Locations:", __locations[:5])

    print("Loading Model...")
    with open("./artifacts/banglore_home_price_prediction.pickle", "rb") as f:
        __model = pickle.load(f)
    print("Artifacts Loaded Successfully")

    print("Loading saved artifacts...done")

# Testing module functionality
if __name__ == "__main__":
    load_saved_artifacts()
    print("Available Locations:", get_location_names())
    price = get_estimated_price('1st Phase JP Nagar', 1000, 3, 3)
    print("Estimated Price:", price)
