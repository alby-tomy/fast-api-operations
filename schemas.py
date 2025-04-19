from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

# Custom validator to strictly enforce integer values for age
def validate_age(age: Optional[int]):
    if age is None:
        return None  # Ensure None is properly returned
    if isinstance(age, float):
        raise ValueError("Age must be an integer, float values are not allowed.")
    if isinstance(age, str):
        raise ValueError("Age must be an integer, string values are not allowed.")
    return age

class UserProfileBase(BaseModel):
    name: str
    age: Optional[int] = Field(None, gt=18, le=120, description="Age must be between 18 and 120")
    email: EmailStr
    profession: Optional[str] = None
    # is_partial: Optional[bool]= Field(default=False)
    
    @field_validator("age")
    def check_age(cls, v):
        return validate_age(v)
    


class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
    profession: Optional[str] = None

    @field_validator("age")
    def check_age_update(cls, v):
        return validate_age(v)

class UserProfile(UserProfileBase):
    id: int

    class Config:
        orm_mode = True


class UserProfileResponse(BaseModel):
    message: str
    user_details: UserProfile

    class Config:
        orm_mode = True
        
        
class UserListProfileResponse(BaseModel):
    message: str
    user_details: list[UserProfile]

    class Config:
        orm_mode = True


# product scheme
class ProductBase(BaseModel):
    product_id: str
    country_code: str
    product_quantity_number: int

class ProductCreate(ProductBase):
    pass

class ProductStockResponse(BaseModel):
    product_id: str
    country_code: str
    available_quantity: int
    status: str
    message: str


class ProductAvailabilityRequest(BaseModel):
    product_id: str
    country_code: str
    required_quantity: int