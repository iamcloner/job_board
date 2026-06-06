from datetime import datetime,timezone
from typing import List, Literal

from bson import ObjectId

from app.core.utils import ResponseUtils
from app.models.companies import CreateCompany, Company, CompanyShow, CompanyList
from app.database.database import db

async def create_company(company_info:CreateCompany,owner_id:str) -> CompanyShow:
    init_time = datetime.now(tz=timezone.utc)
    company = Company(**company_info.model_dump(),owner_id=ObjectId(owner_id),created_at=init_time,updated_at=init_time)
    company_id = await db.companies.insert_one(company.model_dump())
    return CompanyShow(**company.model_dump(exclude="owner_id"),id=str(company_id.inserted_id),owner_id=owner_id)

async def get_companies(owner_id:str,page:int,count:int,sort_by:Literal['name','created_at','is_active','employee_count'],sort_mode:Literal['asc','desc']) -> List[CompanyList]:
    companies_data = await db.companies.find({"owner_id":ObjectId(owner_id)},{"name":1,"is_active":1,"created_at":1,"owner_id":1,"employee_count":1}).sort(sort_by,1 if sort_mode == 'asc' else -1).skip((page-1)*count).limit(count).to_list(length=None)
    companies:List[CompanyShow] = []
    for company in companies_data:
        company = ResponseUtils.ObjectId_Serializer(company,'owner_id')
        company = ResponseUtils.ObjectId_Serializer(company,'_id','id')
        companies.append(CompanyList(**company))
    return companies

async def get_company(company_id:str) -> CompanyShow:
    company = await db.companies.find_one({"_id":ObjectId(company_id)})
    company = ResponseUtils.ObjectId_Serializer(company,'owner_id')
    company = ResponseUtils.ObjectId_Serializer(company,'_id','id')
    return CompanyShow(**company)