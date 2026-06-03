from fastapi import APIRouter, HTTPException, Depends, status

from app.models.companies import CompanyShow, CreateCompany
from app.models.users import UserShow
from app.services.companies import create_company as create_company_service
from app.services.users import authenticate_user

router = APIRouter()

@router.post("",response_model=CompanyShow)
async def create_company(company_info:CreateCompany,current_user:UserShow = Depends(authenticate_user)):
    try:
        return await create_company_service(company_info,current_user.id)
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal Server Error")
