from fastapi import HTTPException

from src.core.logger_setup import LOGGER
from src.model.user import User
from src.model.user_cred import UserCred
from src.schema.user_add_schema import AddUser
from src.schema.user_update_schema import UpdateUser
from src.service.session import session
from src.service.utils import get_hash_password


class UserService:
    @classmethod
    def add_user(cls, user: AddUser) -> dict:
        try:
            # Check for duplicates
            if session.query(User).filter(User.email == user.email).first():
                raise HTTPException(
                    status_code=409, detail="Email already exists")
            if session.query(User).filter(User.username == user.username).first():
                raise HTTPException(
                    status_code=409, detail="Username already exists")

            # Create User
            new_user = User(
                name=user.name,
                username=user.username,
                email=user.email
            )

            # Create UserCred
            new_user_pass = UserCred(hash_password=get_hash_password(user.password), user=new_user)

            # Save
            session.add(new_user)
            session.add(new_user_pass)
            session.commit()
            session.refresh(new_user)

            return {
                "id": new_user.id,
                "name": new_user.name,
                "username": new_user.username,
                "email": new_user.email
            }

        except HTTPException:
            raise
        except Exception as e:
            session.rollback()
            LOGGER.error(repr(e))
            raise HTTPException(status_code=400, detail=str(e))

    @classmethod
    def get_all_users(cls) -> list:
        try:
            data = session.query(User).all()
            return [
                {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "email": user.email
                }
                for user in data
            ]
        except Exception as e:
            LOGGER.error(repr(e))
            raise HTTPException(status_code=500, detail=str(e))

    @classmethod
    def get_user_by_id(cls, id: int) -> dict:
        user = session.get(User, id)
        if not user:
            raise HTTPException(status_code=404, detail="User Not Found")
        return {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email
        }

    @classmethod
    def get_user_password_by_username(cls, username: str) -> str:
        user = session.query(User).filter(User.username == username).first()
        if not user or not user.credential:
            raise HTTPException(status_code=404, detail="User Not Found")
        return user.credential.hash_password

    @classmethod
    def update_user(cls, update_user: UpdateUser, user_id: int) -> dict:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User Not Found")

        try:
            user_data = update_user.model_dump(exclude_unset=True)

            for key, value in user_data.items():
                match key:
                    case "name":
                        user.name = value
                    case "email":
                        user.email = value
                    case "username":
                        user.username = value
                    case "password":
                        hashed_pw = get_hash_password(value)

                        if user.password:
                            user.credential.hash_password = hashed_pw
                        else:
                            new_cred = UserCred(user=user, hash_password=hashed_pw)
                            session.add(new_cred)

            session.commit()
            session.refresh(user)

            return {
                "id": user.id,
                "name": user.name,
                "username": user.username,
                "email": user.email
            }

        except Exception as e:
            session.rollback()
            LOGGER.error(repr(e))
            raise HTTPException(status_code=400, detail=str(e))
