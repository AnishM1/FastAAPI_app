from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, model, utils, database

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.APIResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if db.query(model.User).filter(model.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(model.User).filter(model.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = utils.hash_password(user.password)
    db_user = model.User(
        username=user.username,
        email=user.email,
        password=hashed_pw,
        is_superuser=user.is_superuser
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully", "data": utils.serialize_model(db_user, schemas.UserResponse)}

@router.post("/login", response_model=schemas.APIResponse)
def login(user: schemas.Login, db: Session = Depends(database.get_db)):
    db_user = db.query(model.User).filter(
        (model.User.username == user.username_or_email) |
        (model.User.email == user.username_or_email)
    ).first()
    if not db_user or not utils.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = utils.create_access_token(db_user.id)
    return {"message": "Login successful", "data": {"token": token}}

@router.post("/logout", response_model=schemas.APIResponse)
def logout():
    return {"message": "User logged out successfully", "data": None}
