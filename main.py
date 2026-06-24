from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn
from pathlib import Path
from msgresponse.msgres import MessageResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

BASE_DIR = Path(__file__).parent
acc_db = BASE_DIR / "database" / "accounts.json"
msg_db = BASE_DIR / "database" / "messages.json"
msg_res = MessageResponse(
    json_acc_database_path=acc_db,
    json_msg_database_path=msg_db
)

@app.get("/")
async def root(request: Request):
    messages = msg_res.list_messages("standard_api")["messages"]
    return templates.TemplateResponse(
        "index.html",
        {"request":request, "msg":"Hello from FastAPI!", "messages":messages}
    )

# LOGIN / SIGNUP
@app.get("/login_page/")
async def login_page(request: Request):
    
    return templates.TemplateResponse(
        "login_page.html",
        {"request":request}
    )

@app.post("/login_page/login/")
async def login_func(username: str = Form(...), password: str = Form(...)):
    result = msg_res.login(username=username, password=password)

    if not result.success:
        return {"error": "Login failed"}

    response = RedirectResponse("/", status_code=303)

    response.set_cookie(
        key="session_id",
        value=result.data["session_id"]
    )

    return response

@app.post("/login_page/signup/")
async def signup_func(username: str = Form(...), password: str = Form(...)):
    return msg_res.signup(username=username, password=password)

# CHAT FUNCTIONS
@app.post("/send_msg/")
async def send_msg(request: Request, message: str = Form(...)):

    session_id = request.cookies.get("session_id")

    if not session_id:
        return RedirectResponse("/login_page/", status_code=303)

    msg_res.send_message(
        msg=message,
        session_id=session_id
    )

    return RedirectResponse("/", status_code=303)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)