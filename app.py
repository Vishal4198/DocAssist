from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

sex_map = {'M': 0, 'F': 1}

# Load the trained model
model = joblib.load('models/model.joblib')

# Define a function to preprocess input data
def preprocess_data(data):
    data = pd.DataFrame([data])
    data['SEX'] = data['SEX'].map({'M': 0, 'F': 1})
    print(data)
    return data

@app.route('/', methods=['GET', 'POST'])

def index():
    #print("Form submitted!")  # Debugging statement
    treatment_recommendation = None
    treatment_recommendation_text = None
    if request.method == 'POST':
        # Process the form data here
        patient_data = {
            'HAEMATOCRIT': float(request.form['HAEMATOCRIT']),
            'HAEMOGLOBINS': float(request.form['HAEMOGLOBINS']),
            'ERYTHROCYTE': float(request.form['ERYTHROCYTE']),
            'LEUCOCYTE': float(request.form['LEUCOCYTE']),
            'THROMBOCYTE': float(request.form['THROMBOCYTE']),
            'MCH': float(request.form['MCH']),
            'MCHC': float(request.form['MCHC']),
            'MCV': float(request.form['MCV']),
            'AGE': int(request.form['AGE']),
            'SEX': request.form['SEX']
        }
        #print(patient_data) # Debugging statement

        # Preprocess the data
        processed_data = preprocess_data(patient_data)

        # Make predictions using the model
        treatment_recommendation = model.predict(processed_data)

        if treatment_recommendation is not None:
            if treatment_recommendation == 1:
                treatment_recommendation_text = "Treatment required. Please consult the doctor"
            elif treatment_recommendation == 0:
                treatment_recommendation_text = "No treatment required. Be happy"

    return render_template('index.html', treatment_recommendation=treatment_recommendation_text)

if __name__ == '__main__':
    app.run(debug=True)