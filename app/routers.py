# routers.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from middleware import make_cookie_from_dict
from schemas import *
import requests
import os

URL_ACCOUNT_SERVICE = os.getenv("URL_ACCOUNT_SERVICE")
if not URL_ACCOUNT_SERVICE:
    raise RuntimeError("Environment variable URL_ACCOUNT_SERVICE is not set.")

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

###################################
##### Routers Functions Below #####
###################################

#Default function, change as needed
@router.get("")
async def root_func():
    return {"message": "Root function ran!"}

@router.post("/login", response_model=UserReadDTO, status_code=200)
async def auth_login(payload: UserLoginDTO):
    try:
        user = requests.post(URL_ACCOUNT_SERVICE + "/account/login", json=payload.dict())
        if user.status_code != 200:
            raise HTTPException(status_code=user.status_code, detail=user.json().get("detail"))
        cookie = make_cookie_from_dict(user.json())
        
        response = JSONResponse(
            content=user.json()
        )
        response.set_cookie(
            key="session_token",
            value=cookie,
            httponly=True,
            samesite="lax"
        )
        return response

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))