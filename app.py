import streamlit as st
import pandas as pd
import numpy as np
import pickle
import base64

st.title("Heart Disease Predictor")
tab1,tab2 = st.tabs(['Predict','Model Information'])

with tab1:
    age = st.number_input("Age (years)", min_value=0, max_value=150)
    sex = st.selectbox("Sex", ["Male", "Female"])
    chest_pain = st.selectbox("Chest Pain Type", ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Anginal Pain"])
    resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", min_value=0, max_value=300)
    cholesterol = st.number_input("Serum Cholesterol (mm/dl)", min_value=0)
    fasting_bs = st.selectbox("Fasting Blood Sugar", ["<= 120 mg/dl", "> 120 mg/dl"])
    resting_ecg = st.selectbox("Resting ECG Results", ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"])
    max_hr = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=202)
    exercise_angina = st.selectbox("Exercise-Induced Angina", ["Yes", "No"])
    oldpeak = st.number_input("Oldpeak (ST Depression)", min_value=0.0, max_value=10.0)
    st_slope = st.selectbox("Slope of Peak Exercise ST Segment", ["Unsloping", "Flat", "Downsloping"])

    # convert categorical inputs to numeric
    sex = 0 if sex == "Male" else 1
    chest_pain = ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Anginal Pain"].index(chest_pain)
    fasting_bs = 1 if fasting_bs == "> 120 mg/dl" else 0
    resting_ecg = ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"].index(resting_ecg)
    exercise_angina = 1 if exercise_angina == "Yes" else 0
    st_slope = ["Unsloping", "Flat", "Downsloping"].index(st_slope)

    # create a dataframe with the user inputs
    input_data = pd.DataFrame({
        'age': [age],
        'sex': [sex],
        'chest_pain': [chest_pain],
        'resting_bp': [resting_bp],
        'cholesterol': [cholesterol],
        'fasting_bs': [fasting_bs],
        'resting_ecg': [resting_ecg],
        'max_hr': [max_hr],
        'exercise_angina': [exercise_angina],
        'oldpeak': [oldpeak],
        'st_slope': [st_slope]
    })

    algonames = ['Decision Trees', 'Logistic Regression', 'Random Forest', 'Support Vector Machine', 'Grid Random Forest']
    modelnames = ['DesicionTree.pkl','LogisticR.pkl','RandomForest.pkl','SVM.pkl','GridRF.pkl']

    predictions = []
    def predict_heart_disease(data):
        for modelname in modelnames:
            model = pickle.load(open(modelname, 'rb'))
            prediction = model.predict(data)
            predictions.append(prediction)
        return predictions

    # create a submit button to make predictions
    if st.button("Submit"):
        st.subheader('Results....')
        st.markdown('---------------------------')

        result = predict_heart_disease(input_data) 

        for i in range(len(predictions)):
            st.subheader(algonames[i])
            if result[i][0] == 0:
                st.write("No heart disease detected.")
            else:
                st.write("Heart disease detected.")
            st.markdown('------------------------')          

