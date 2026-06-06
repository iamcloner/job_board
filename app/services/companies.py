from datetime import datetime,timezone
from typing import List

from bson import ObjectId

from app.models.companies import CreateCompany, Company, CompanyShow
from app.database.database import db

async def create_company(company_info:CreateCompany,owner_id:str) -> CompanyShow:
    init_time = datetime.now(tz=timezone.utc)
    company = Company(**company_info.model_dump(),owner_id=ObjectId(owner_id),created_at=init_time,updated_at=init_time)
    company_id = await db.companies.insert_one(company.model_dump())
    return CompanyShow(**company.model_dump(exclude="owner_id"),id=str(company_id.inserted_id),owner_id=owner_id)

async def get_companies(owner_id:str) -> List[CompanyShow]:
    companies_data = await db.companies.find({"owner_id":ObjectId(owner_id)}).to_list()
    companies:List[CompanyShow] = []
    for company in companies_data:
        company["owner_id"] = str(company["owner_id"])
        companies.append(CompanyShow(**company,id=str(company['_id'])))
    return companies