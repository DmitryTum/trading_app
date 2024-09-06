from fastapi import APIRouter, Depends
from src.auth.base_config import current_user

from .tasks import send_email_report_dashboard


router = APIRouter()


@router.get('/dashboard')
def get_dashboard_report(user=Depends(current_user)):
    send_email_report_dashboard.delay(user.username)
    return {
        'status': 'success',
        'data': 'Leter is send',
        'details': None
    }
