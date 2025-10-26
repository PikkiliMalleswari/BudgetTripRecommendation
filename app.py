from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load dataset
data = pd.read_csv("data.csv")

# Ensure Average_Cost is numeric
data['Average_Cost'] = pd.to_numeric(data['Average_Cost'], errors='coerce')

# Clean Type column: lowercase and strip spaces
data['Type'] = data['Type'].str.strip().str.lower()

# Optional: clean Destination and State columns
data['Destination'] = data['Destination'].str.strip()
data['State'] = data['State'].str.strip()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Get input from form
        budget = float(request.form['budget'])
        trip_type = request.form['trip_type'].strip().lower()  # lowercase to match CSV

        # Debug prints to check values
        print("Form input - Budget:", budget, "Trip Type:", trip_type)
        print("CSV Types:", data['Type'].unique())

        # Filter trips
        recommendations = data[
            (data['Average_Cost'] <= budget) &
            (data['Type'].str.lower() == trip_type)
        ]

        print("Filtered trips:\n", recommendations)

        trips = recommendations.to_dict(orient='records')

        return render_template("result.html", recommendations=trips)
    
    except Exception as e:
        print("Error:", e)
        return render_template("result.html", recommendations=[])

if __name__ == "__main__":
    app.run(debug=True)
