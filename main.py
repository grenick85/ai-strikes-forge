from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_winner
from enum import Enum

app = FastAPI(title="The Architect's Sports Oracle", version="2.0")

# 1. This creates the Dropdown Menu for sports
class Sport(str, Enum):
    NFL = "NFL"
    NBA = "NBA"
    NCAAB = "NCAAB"
    MLB = "MLB"
    NHL = "NHL"

# 2. This tells the API what data we need from the user
class MatchRequest(BaseModel):
    sport: Sport
    home_team: str
    away_team: str

@app.get("/")
def read_root():
    return {"message": "Oracle 2.0 Online. Ready for Multi-Sport Analysis."}

@app.post("/predict")
def get_prediction(match: MatchRequest):
    # This sends the data to your new brain in model.py
    result = predict_winner(match.home_team, match.away_team, match.sport)
    return result