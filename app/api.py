from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, model, database, utils

router = APIRouter(prefix="/users", tags=["Users"])

# --- Admin only routes ---
@router.get("/", response_model=schemas.APIResponse)
def get_all_users(
    db: Session = Depends(database.get_db),
    current_user: model.User = Depends(utils.admin_required)
):
    users = db.query(model.User).all()
    return {"message": "All users fetched", "data": utils.serialize_model(users, schemas.UserResponse)}

@router.get("/{user_id}", response_model=schemas.APIResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: model.User = Depends(utils.admin_required)
):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User fetched", "data": utils.serialize_model(user, schemas.UserResponse)}

@router.put("/{user_id}", response_model=schemas.APIResponse)
def update_user(
    user_id: int,
    update: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: model.User = Depends(utils.admin_required)
):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if update.username:
        user.username = update.username
    if update.email:
        user.email = update.email
    if update.password:
        user.password = utils.hash_password(update.password)
    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "data": utils.serialize_model(user, schemas.UserResponse)}

@router.delete("/{user_id}", response_model=schemas.APIResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: model.User = Depends(utils.admin_required)
):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully", "data": None}

# --- Normal user routes ---
@router.delete("/soft/{user_id}", response_model=schemas.APIResponse)
def soft_delete_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: model.User = Depends(utils.get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot delete other users")
    user = db.query(model.User).filter(model.User.id == user_id).first()
    user.is_active = False
    db.commit()
    return {"message": "User soft deleted", "data": {"id": user.id, "is_active": user.is_active}}

@router.get("/profile/me", response_model=schemas.APIResponse)
def get_profile(
    db: Session = Depends(database.get_db),
    current_user: model.User = Depends(utils.get_current_user)
):
    profile = db.query(model.Profile).filter(model.Profile.user_id == current_user.id).first()
    return {"message": "Profile fetched", "data": utils.serialize_model(profile, schemas.ProfileResponse)}

@router.get("/notifications/me", response_model=schemas.APIResponse)
def get_notifications(
    db: Session = Depends(database.get_db),
    current_user: model.User = Depends(utils.get_current_user)
):
    notifications = db.query(model.Notification).filter(model.Notification.user_id == current_user.id).all()
    return {"message": "Notifications fetched", "data": utils.serialize_model(notifications, schemas.NotificationResponse)}
