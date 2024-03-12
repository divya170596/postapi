from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import jwt
import datetime
import os
import uvicorn
from mangum import Mangum

app = FastAPI()
handler=Mangum(app)

# MongoDB connection
uri = "mongodb+srv://divya:divya170596@track.c7nmyhv.mongodb.net/?retryWrites=true&w=majority&appName=Track"
client = MongoClient(uri)
db = client["Tracking"]
users_collection = db["Driver_details"]

# Secret key for JWT
SECRET_KEY = os.urandom(24)

def generate_token(user_id: str):
    """
    Function to generate a JWT token for authentication.
    """
    token = jwt.encode({'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                       SECRET_KEY)
    return token

@app.post('/login')
def login(data: dict):
    email_or_name = data.get('email_or_name')
    password = data.get('password')

    # Find user by email or name
    user = users_collection.find_one({"$or": [{"email": email_or_name}, {"name": email_or_name}]})

    if user and user.get("password") == password:
        # Generate token
        token = generate_token(str(user["_id"]))
        
        # Return response with user details and token
        response = {
            "message": "Successfully logged in",
            "name": user["name"],
            "email": user["email"],
            "token": token
        }
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


if __name__=="__main__":
  uvicorn.run(app,host="0.0.0.0",port=3300)
