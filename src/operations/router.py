import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy import select, insert
from src.operations.models import operation
from .schemas import OperationCreate
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix='/operation',
    tags=["Operation"]
)


@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "xdfsdfjsndf sjd f"


@router.get('/')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = session.execute(query)
        return {
            'status': 'success',
            'data': result.all(),
            'detail': None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'detail': None
        })


@router.post('/')
async def add_specific_operatons(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stms = insert(operation).values(**new_operation.dict())
    await session.execute(stms)
    await session.commit
    return {'status': 'success'}
