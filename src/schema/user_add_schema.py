from pydantic import BaseModel, Field, model_validator, EmailStr
from typing import Annotated, Self


class AddUser(BaseModel):
    name: Annotated[str, Field(..., max_length=255, min_length=5, description="User Name")]
    username: Annotated[str, Field(..., max_length=255, min_length=5, description="Unique username")]
    email: Annotated[EmailStr, Field(..., max_length=255, min_length=5, description="Gmail/Email Address")]
    password: Annotated[str, Field(..., max_length=255, min_length=8, description="A Strong Password Must Include: 0-9 Digits, a-z & A-Z & Special Characters")]

    @model_validator(mode="after")
    def validate_password(self) -> Self:
        if self.password:
            if self.name and self.name in self.password:
                raise ValueError("Password should not include users's name or username.")
            if self.username and self.username in self.password:
                raise ValueError("Password should not include users's name or username.")
        return self