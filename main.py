from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = FastAPI(title="RBAC E-Commerce Catalog API")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
security = HTTPBearer()


# Pydantic Schemas
class CategoryResponse(BaseModel):
    id: int
    name: str

class ItemCreate(BaseModel):
    name: str
    category_id: int
    price: float = Field(..., gt=0)
    in_stock: bool = True

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool
    category_id: int
    categories: Optional[CategoryResponse] = None

class UserLogin(BaseModel):
    email: str
    password: str


# --- AUTH & RBAC DEPENDENCIES ---

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_response.user
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


# Admin Role Check Dependency
def require_admin(user = Depends(verify_token)):
    user_metadata = user.user_metadata or {}
    user_role = user_metadata.get("role")
    
    if user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admin privileges required"
        )
    return user


# --- ENDPOINTS ---

@app.post("/login")
def login(credentials: UserLogin):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        return {"access_token": res.session.access_token, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid credentials")


# Public Read Access
@app.get("/items", response_model=List[ItemResponse])
def get_items():
    response = supabase.table("items").select("*, categories(*)").execute()
    return response.data


# Admin-Only Write Access
@app.post("/items", response_model=List[ItemResponse])
def create_item(item: ItemCreate, admin_user = Depends(require_admin)):
    try:
        data = item.model_dump()
        response = supabase.table("items").insert(data).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))