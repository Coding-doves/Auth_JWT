import time
import jwt
from decouple import config


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


# Returns jwt generate token
def token_resp(token:str):
    return {"bearer": token}

# Encode/create token
def token_encode(userID:str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 500
        }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_resp(token)
   
def token_decode(token:str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return decode_token if decode_token['exipires'] >= time.time() else None
    except Exception as e:
        return {"Error": e}
