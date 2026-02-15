from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from typing import List
from app.models.company import CompanyCreate, CompanyUpdate, CompanyResponse
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
async def get_all_companies(skip: int = 0, limit: int = 10):
    companies_collection = get_companies_collection()
    
    if skip < 0:
        raise HTTPException(status_code=400, detail="Skip must be >= 0")
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    
    companies = list(companies_collection.find().skip(skip).limit(limit))
    
    for company in companies:
        company["_id"] = str(company["_id"])
        company.pop("hashed_password", None)
    
    return [CompanyResponse.model_validate(company) for company in companies]


@router.get("/{id}", response_model=CompanyResponse)
async def get_company_by_id(id: str):
    companies_collection = get_companies_collection()
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid company ID")
    
    company = companies_collection.find_one({"_id": ObjectId(id)})
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company["_id"] = str(company["_id"])
    company.pop("hashed_password", None)
    
    return CompanyResponse.model_validate(company)


@router.put("/{id}", response_model=CompanyResponse)
async def update_company(id: str, company_update: CompanyUpdate):
    companies_collection = get_companies_collection()
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid company ID")
    
    
    update_data = company_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    
    try:
        result = companies_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
    except DuplicateKeyError as e:
        if "email" in str(e):
            raise HTTPException(status_code=400, detail="Email already exists")
        elif "mobile" in str(e):
            raise HTTPException(status_code=400, detail="Mobile number already exists")
        raise HTTPException(status_code=400, detail="Duplicate entry")
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Company not found")
    
    updated_company = companies_collection.find_one({"_id": ObjectId(id)})
    updated_company["_id"] = str(updated_company["_id"])
    updated_company.pop("hashed_password", None)
    
    return CompanyResponse.model_validate(updated_company)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(id: str):
    companies_collection = get_companies_collection()
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid company ID")
    
    result = companies_collection.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return None
