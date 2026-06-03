from datetime import datetime

from bson import ObjectId

from app.models.companies import CreateCompany, Company, CompanyShow
from app.database.database import db

async def create_company(company_info:CreateCompany,owner_id:str):
    init_time = datetime.now()
    company = Company(**company_info.model_dump(),owner_id=ObjectId(owner_id),created_at=init_time,updated_at=init_time)
    company_id = await db.companies.insert_one(company.model_dump())
    return CompanyShow(**company.model_dump(exclude="owner_id"),id=str(company_id.inserted_id),owner_id=owner_id)
