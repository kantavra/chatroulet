from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def home():
    return RedirectResponse("/lobby")

@router.get("/lobby")
def get_lobby(request: Request):
    return templates.TemplateResponse(request=request, name="lobby.html")
