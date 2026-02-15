from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from typing import List
from app.models.company import CompanyCreate, CompanyResponse
from app.database import get_companies_collection
from app.utils.security import hash_password

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(company: CompanyCreate):
    companies_collection = get_companies_collection()
    
    hashed_password = hash_password(company.password)
    
    company_data = {
        "company_name": company.company_name,
        "email": company.email,
        "mobile": company.mobile,
        "address": company.address,
        "hashed_password": hashed_password
    }
    
    try:
        result = companies_collection.insert_one(company_data)
    except DuplicateKeyError as e:
        if "email" in str(e):
            raise HTTPException(status_code=400, detail="Email already exists")
        elif "mobile" in str(e):
            raise HTTPException(status_code=400, detail="Mobile number already exists")
        raise HTTPException(status_code=400, detail="Duplicate entry")
    
    created_company = companies_collection.find_one({"_id": result.inserted_id})
    created_company["_id"] = str(created_company["_id"])
    created_company.pop("hashed_password", None)
    
    return CompanyResponse.model_validate(created_company)


@router.get("/", response_model=List[CompanyResponse])
async def get_all_companies():
    companies_collection = get_companies_collection()
    
    companies = list(companies_collection.find())
    
    for company in companies:
        company["_id"] = str(company["_id"])
        company.pop("hashed_password", None)
    
    return [CompanyResponse.model_validate(company) for company in companies]
