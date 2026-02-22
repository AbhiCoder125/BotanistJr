'''import sqlite3
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request

# -------- DATABASE SETUP --------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


# -------- REGISTER FUNCTION --------
async def register(request: Request):
    data = await request.json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return JSONResponse({"error": "All fields required"}, status_code=400)

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, password)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return JSONResponse({
        "message": "User Registered Successfully",
        "user": {
            "id": user_id,
            "name": name,
            "email": email
        }
    })


# -------- ROUTES --------
routes = [
    Route("/register", register, methods=["POST"]),
]

app = Starlette(routes=routes)
import sqlite3
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.templating import Jinja2Templates

# -------- DATABASE SETUP --------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

templates = Jinja2Templates(directory="templates")

# -------- SHOW FORM PAGE --------
async def homepage(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# -------- REGISTER FUNCTION --------
async def register(request: Request):
    form = await request.form()

    name = form.get("name")
    email = form.get("email")
    password = form.get("password")

    if not name or not email or not password:
        return HTMLResponse("<h3>All fields required!</h3>")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, password)
    )
    conn.commit()
    conn.close()

    return HTMLResponse("<h3>User Registered Successfully!</h3>")

routes = [
    Route("/", homepage, methods=["GET"]),
    Route("/register", register, methods=["POST"]),
]

app = Starlette(routes=routes)
import sqlite3
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

# -------- DATABASE SETUP --------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------- TEMPLATES --------
templates = Jinja2Templates(directory="templates")

# -------- SHOW REGISTRATION FORM --------
async def homepage(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# -------- REGISTER FUNCTION --------
async def register(request: Request):
    form = await request.form()

    name = form.get("name")
    email = form.get("email")
    password = form.get("password")

    if not name or not email or not password:
        return HTMLResponse("<h3>All fields required!</h3>")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, password)
    )
    conn.commit()
    conn.close()

    return HTMLResponse("<h3>User Registered Successfully!</h3><br><a href='/users'>View All Users</a>")

# -------- SHOW ALL USERS --------
async def show_users(request: Request):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    conn.close()

    table_html = "<h2>Registered Users</h2><table border='1' style='border-collapse: collapse;'><tr><th>ID</th><th>Name</th><th>Email</th></tr>"
    for user in users:
        table_html += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td></tr>"
    table_html += "</table><br><a href='/'>Back to Registration</a>"

    return HTMLResponse(table_html)

# -------- ROUTES --------
routes = [
    Route("/", homepage, methods=["GET"]),
    Route("/register", register, methods=["POST"]),
    Route("/users", show_users, methods=["GET"]),
]

# -------- CREATE APP --------
app = Starlette(routes=routes)

# -------- MOUNT STATIC FILES --------
app.mount("/static", StaticFiles(directory="static"), name="static")

# app_graphql.py
import sqlite3
import strawberry
from typing import List
from starlette.applications import Starlette
from strawberry.asgi import GraphQL

# -------- DATABASE SETUP --------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------- GRAPHQL TYPES --------
@strawberry.type
class User:
    id: int
    name: str
    email: str

# -------- GRAPHQL QUERIES --------
@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[User]:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [User(id=row[0], name=row[1], email=row[2]) for row in rows]

# -------- GRAPHQL MUTATIONS --------
@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(self, name: str, email: str, password: str) -> User:
        if not name or not email or not password:
            raise ValueError("All fields required")
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return User(id=user_id, name=name, email=email)

# -------- CREATE SCHEMA --------
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

# -------- STARLETTE APP --------
app = Starlette()
app.mount("/graphql", graphql_app)
import sqlite3
import strawberry
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from strawberry.asgi import GraphQL

# -------- DATABASE SETUP --------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------- STARRY GRAPHQL TYPES --------
@strawberry.type
class User:
    id: int
    name: str
    email: str

# -------- GRAPHQL MUTATION --------
@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(self, name: str, email: str, password: str) -> User:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return User(id=user_id, name=name, email=email)

# -------- GRAPHQL QUERY --------
@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [User(id=r[0], name=r[1], email=r[2]) for r in rows]

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

# -------- TEMPLATES & STATIC --------
templates = Jinja2Templates(directory="templates")

async def homepage(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# -------- ROUTES --------
routes = [
    Route("/", homepage, methods=["GET"]),
    Route("/graphql", graphql_app),  # GraphQL endpoint (hidden from users)
]

app = Starlette(routes=routes)
app.mount("/static", StaticFiles(directory="static"), name="static")
import sqlite3
import strawberry
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from strawberry.asgi import GraphQL

# -------- DATABASE SETUP --------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            full_name TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------- GRAPHQL TYPES --------
@strawberry.type
class User:
    id: int
    username: str
    full_name: str

# -------- GRAPHQL MUTATION --------
@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(self, username: str, full_name: str, password: str) -> User:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, full_name, password) VALUES (?, ?, ?)",
            (username, full_name, password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return User(id=user_id, username=username, full_name=full_name)

# -------- GRAPHQL QUERY --------
@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, full_name FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [User(id=r[0], username=r[1], full_name=r[2]) for r in rows]

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

# -------- TEMPLATES & STATIC --------
templates = Jinja2Templates(directory="templates")

async def homepage(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# -------- ROUTES --------
routes = [
    Route("/", homepage, methods=["GET"]),
    Route("/graphql", graphql_app),  # GraphQL endpoint
]

app = Starlette(routes=routes)
app.mount("/static", StaticFiles(directory="static"), name="static")'''
import sqlite3
import strawberry
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.routing import Route
from strawberry.asgi import GraphQL

# -------- DATABASE SETUP --------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            full_name TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------- GRAPHQL TYPES --------
@strawberry.type
class User:
    id: int
    username: str
    full_name: str

# -------- GRAPHQL MUTATION --------
@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(self, username: str, full_name: str, password: str) -> User:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, full_name, password) VALUES (?, ?, ?)",
            (username, full_name, password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return User(id=user_id, username=username, full_name=full_name)

# -------- GRAPHQL QUERY --------
@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, full_name FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [User(id=r[0], username=r[1], full_name=r[2]) for r in rows]

# Create GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

# -------- TEMPLATES & STATIC --------
templates = Jinja2Templates(directory="templates")

async def homepage(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# -------- ROUTES --------
routes = [
    Route("/", homepage, methods=["GET"]),
    Route("/graphql", graphql_app),  # GraphQL endpoint
]

app = Starlette(routes=routes)
app.mount("/static", StaticFiles(directory="static"), name="static")