from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates


from src.operations.router import get_specific_operations

templates = Jinja2Templates(directory='src/templates')


router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)


@router.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@router.get('/search')
def get_search_page(request: Request, operations=Depends(get_specific_operations)):
    return templates.TemplateResponse('search.html', {'request': request, 'operations': operations['data']})


@router.get('/chat')
def get_chat_page(reuqest: Request):
    return templates.TemplateResponse('chat.html', {'request': reuqest})
