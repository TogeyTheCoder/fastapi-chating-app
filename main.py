from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pathlib import Path
from msgresponse.msgres import MessageResponse
from contextlib import asynccontextmanager

BASE_DIR = Path(__file__).parent

db_dir = BASE_DIR / "database"

msg_res = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global msg_res

    db_dir.mkdir(exist_ok=True)

    acc_db = db_dir / "accounts.json"
    msg_db = db_dir / "messages.json"

    for file in [acc_db, msg_db]:
        if not file.exists():
            file.write_text("{}")

    msg_res = MessageResponse(
        json_acc_database_path=acc_db,
        json_msg_database_path=msg_db
    )

    yield

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

def ensure_ready():
    if msg_res is None:
        raise HTTPException(status_code=503, detail="Server not ready")

@app.get("/")
async def root(request: Request):
    ensure_ready()
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
    ensure_ready()
    result = msg_res.login(username=username, password=password)

    if not result.success:
        return {"error": "Login failed"}

    response = RedirectResponse("/", status_code=303)

    response.set_cookie(
        key="session_id",
        value=result.data["session_id"],
        httponly=True,
        samesite="lax"
    )

    return response

@app.post("/login_page/signup/")
async def signup_func(username: str = Form(...), password: str = Form(...)):
    ensure_ready()
    return msg_res.signup(username=username, password=password)

# CHAT FUNCTIONS
@app.post("/send_msg/")
async def send_msg(request: Request, message: str = Form(...)):

    ensure_ready()

    session_id = request.cookies.get("session_id")

    if not session_id:
        return RedirectResponse("/login_page/", status_code=303)

    msg_res.send_message(
        msg=message,
        session_id=session_id
    )

    return RedirectResponse("/", status_code=303)