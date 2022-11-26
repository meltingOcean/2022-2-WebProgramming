from fastapi import Depends, FastAPI, Request, Response, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse, RedirectResponse

from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.templating import Jinja2Templates


from models import Base, User
from crud import db_register_user
from database import SessionLocal, engine
from typing import List, Union

from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class NotAuthenticatedException(Exception):
    pass
db = {}

SECRET = "super-secret-key"
manager = LoginManager(SECRET, '/login', use_cookie=True,
                            custom_exception=NotAuthenticatedException)




Base.metadata.create_all(bind=engine)



@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse(url='login')

@manager.user_loader
def get_user(username: str, db: Session = None):
    if not db:
        with SessionLocal() as db:
            return db.query(User).filter(User.name == username).first()
    return db.query(User).filter(User.name == username).first()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# ==== Login / Logout / Register ==== #

@app.get("/")
def get_root(user=Depends(manager)):
    return FileResponse("index1.html")

@app.get("/login")
def get_login(req: Request):
    return templates.TemplateResponse("common/login.html", {"request" : req})

@app.get("/logout")
def logout(response : Response):
    response = RedirectResponse("/login", status_code= 302)
    response.delete_cookie(key = "access-token")
    return response

@app.post('/token')
def login(response: Response, data: OAuth2PasswordRequestForm = Depends()):

    username = data.username
    password = data.password

    user = get_user(username)

    if not user:
        raise InvalidCredentialsException
    if user.password != password:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data = { 'sub': username }
    )
    manager.set_cookie(response, access_token)
    return {'access_token' : access_token}

@app.post('/register')
def register_user(response: Response,
    data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):

    username = data.username
    password = data.password

    user = db_register_user(db, username, password)
    if user:
        access_token = manager.create_access_token(
            data={"sub": username}

        )
        manager.set_cookie(response, access_token)
        return "User created"
    else:
        return "Failed"
# ==== Login / Logout / Register ==== #


# ============= Seller ============== #

@app.get('/seller/{user_id}')
def get_seller_main(response : Response):
    return 1




# ============= Seller ============== #


# ============= Buyer  ============== #

@app.get('/buyer/{user_id}')
def get_buyer_main(response : Response):
    return 1

# ============= Buyer  ============== #