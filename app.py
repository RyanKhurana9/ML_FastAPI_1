from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field,field_validator
from typing import Literal, Annotated
from schema.user_input import UserInput 
import pickle
import pandas as pd
from model.predict import predict_output, MODEL_VERSION,model
#field_validator=>it is uded to clean,check and modify the incoming data before it is used in the application
# import the ml model


app = FastAPI()



@app.get('/')
def home():#human readable
    return {'message':"Welcome to the insurance premium prediction API. Please use the /predict endpoint to get your insurance premium category based on your details."}
#machine readable
#/health endpoint tells systems like Amazon Web Services and Kubernetes whether your app is working or not
@app.get('/health')
def health_check():
    return {
        'Status':'OK',
        'Version':MODEL_VERSION,
        'model_loaded':model is True
    }

@app.post('/predict')
def predict_premium(data: UserInput):

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:
        output=predict_output(user_input)
        return JSONResponse(status_code=200,content={"predicted_premium_category":output})
    except Exception as e:
        return JSONResponse(status_code=500,content={"error":str(e)})
    
