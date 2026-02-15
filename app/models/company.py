from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from bson import ObjectId
import re


class PyObjectId(ObjectId):
    """Custom type for handling MongoDB ObjectId in Pydantic models"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class CompanyCreate(BaseModel):
    """Schema for creating a new company (registration)"""
    company_name: str = Field(..., min_length=2, max_length=200, description="Company name")
    email: EmailStr = Field(..., description="Company email address")
    mobile: str = Field(..., min_length=10, max_length=15, description="Company mobile number")
    address: str = Field(..., min_length=5, max_length=500, description="Company address")
    password: str = Field(..., min_length=6, description="Company password")
    
    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v):
        """Validate mobile number format"""
        # Remove any spaces, dashes, or parentheses
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        
        # Check if it contains only digits and optional + at start
        if not re.match(r'^\+?\d{10,15}$', cleaned):
            raise ValueError("Mobile number must contain 10-15 digits and can optionally start with +")
        
        return cleaned
    
    @field_validator("company_name")
    @classmethod
    def validate_company_name(cls, v):
        """Validate company name"""
        if not v.strip():
            raise ValueError("Company name cannot be empty or just whitespace")
        return v.strip()
    
    @field_validator("address")
    @classmethod
    def validate_address(cls, v):
        """Validate address"""
        if not v.strip():
            raise ValueError("Address cannot be empty or just whitespace")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "company_name": "Tech Solutions Inc.",
                "email": "contact@techsolutions.com",
                "mobile": "+1234567890",
                "address": "123 Business Street, Tech City, TC 12345",
                "password": "securePassword123"
            }
        }


class CompanyUpdate(BaseModel):
    """Schema for updating company details (all fields optional for partial updates)"""
    company_name: Optional[str] = Field(None, min_length=2, max_length=200, description="Company name")
    email: Optional[EmailStr] = Field(None, description="Company email address")
    mobile: Optional[str] = Field(None, min_length=10, max_length=15, description="Company mobile number")
    address: Optional[str] = Field(None, min_length=5, max_length=500, description="Company address")
    password: Optional[str] = Field(None, min_length=6, description="Company password")
    
    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v):
        """Validate mobile number format"""
        if v is None:
            return v
        
        # Remove any spaces, dashes, or parentheses
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        
        # Check if it contains only digits and optional + at start
        if not re.match(r'^\+?\d{10,15}$', cleaned):
            raise ValueError("Mobile number must contain 10-15 digits and can optionally start with +")
        
        return cleaned
    
    @field_validator("company_name")
    @classmethod
    def validate_company_name(cls, v):
        """Validate company name"""
        if v is not None and not v.strip():
            raise ValueError("Company name cannot be empty or just whitespace")
        return v.strip() if v else v
    
    @field_validator("address")
    @classmethod
    def validate_address(cls, v):
        """Validate address"""
        if v is not None and not v.strip():
            raise ValueError("Address cannot be empty or just whitespace")
        return v.strip() if v else v

    class Config:
        json_schema_extra = {
            "example": {
                "company_name": "Updated Tech Solutions Inc.",
                "email": "newemail@techsolutions.com",
                "mobile": "+9876543210",
                "address": "456 New Business Avenue, Tech City, TC 54321"
            }
        }


class CompanyResponse(BaseModel):
    """Schema for company response (excludes password)"""
    id: str = Field(alias="_id", description="Company ID")
    company_name: str
    email: str
    mobile: str
    address: str
    
    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "company_name": "Tech Solutions Inc.",
                "email": "contact@techsolutions.com",
                "mobile": "+1234567890",
                "address": "123 Business Street, Tech City, TC 12345"
            }
        }
    }


class CompanyInDB(BaseModel):
    """Internal schema for company stored in database (includes hashed password)"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    company_name: str
    email: str
    mobile: str
    address: str
    hashed_password: str
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
