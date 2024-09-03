from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy import select, insert
from operations.models import operation
from schemas import OperationCreate

router = APIRouter(
    prefix='/',
    tags=["Operation"]
)


@router.get('/')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = session.execute(query)
    return result.all()


@router.post('/')
async def add_specific_operatons(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stms = insert(operation).values(**new_operation.dict())
    await session.execute(stms)
    await session.commit
    return {'status': 'success'}
