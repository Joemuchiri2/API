# Bring the light weight  dependencies
from fastapi import FastAPI
import uvicorn
import joblib
from typing import List, Literal
from pydantic import BaseModel
import pandas as pd
import pickle, os

app = FastAPI()

class Sepsis(BaseModel):
    id: str
    prg: int
    pl: int
    pr: int
    sk: int
    ts: int
    m11: float
    bd2: float
    age: int
    insurance: int
    sepssis: str

# Load the models
random_forest_pipeline = joblib.load('./models/random_forest_pipeline.pkl')



# Load the label encoder
encoder = joblib.load('./label_encoder.pkl')


@app.get('/')
async def root():
    return {"Status":"Ok"}

@app.post('/predict_sepsis/')
async def predict_sepsis(data: Sepsis):

    # Convert data to DataFrame
    df = pd.DataFrame([data.dict()])

    # Encode categorical features
    df_encoded = encoder.transform(df[['sepssis']])

    # Drop the original categorical column 
    df = df.drop(columns=['sepssis'])
    df['sepssis'] = df_encoded

    # Make prediction using the random forest model
    prediction = random_forest_pipeline.predict(df)

    # Convert prediction to an int
    prediction = int(prediction[0])

    # Decode the prediction using the encoder
    prediction = encoder.inverse_transform([prediction])[0]

    # Get the probability of each class
    probability = random_forest_pipeline.predict_proba(df)

    return {"Prediction": prediction, "Probability": probability[0].tolist()}




   