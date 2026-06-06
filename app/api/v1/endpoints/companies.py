from typing import List, Literal

from fastapi import APIRouter, HTTPException, Depends, status

from app.models.companies import CompanyShow, CreateCompany, CompanyList
from app.models.users import UserShow
from app.services.companies import create_company as create_company_service
from app.services.companies import get_companies as get_companies_service
from app.services.companies import get_company as get_company_service
from app.services.users import authenticate_user

router = APIRouter()

@router.get("",response_model=List[CompanyList])
async def get_my_companies(page:int=1,count:int=10,sort_by:Literal['name','created_at','is_active','employee_count']='name',sort_mode:Literal['asc','desc']='asc',current_user:UserShow = Depends(authenticate_user)):
    try:
        return await get_companies_service(current_user.id,page,count,sort_by,sort_mode)
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal Server Error")

@router.get("/{company_id}",response_model=CompanyShow)
async def get_company(company_id:str,current_user:UserShow=Depends(authenticate_user)):
    try:
        company = await get_company_service(company_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Company not found")
    if company.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return company
@router.post("",response_model=CompanyShow, status_code=status.HTTP_201_CREATED)
async def create_company(company_info:CreateCompany,current_user:UserShow = Depends(authenticate_user)):
    try:
        return await create_company_service(company_info,current_user.id)
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal Server Error")


