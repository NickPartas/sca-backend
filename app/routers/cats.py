from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..db import engine
from ..models import Cat
from ..schemas import CatCreate, CatRead, SalaryPatch

router = APIRouter(prefix="/cats", tags=["cats"])

@router.post("/", response_model=CatRead, status_code=201)
def create_cat(cat: CatCreate):
    with Session(engine) as s:
        obj = Cat(**cat.dict())
        s.add(obj); s.commit(); s.refresh(obj)
        return obj

@router.get("/", response_model=list[CatRead])
def list_cats():
    with Session(engine) as s:
        return s.exec(select(Cat)).all()

@router.get("/{cat_id}", response_model=CatRead)
def get_cat(cat_id: int):
    with Session(engine) as s:
        obj = s.get(Cat, cat_id)
        if not obj:
            raise HTTPException(404)
        return obj

@router.patch("/{cat_id}", response_model=CatRead)
def update_salary(cat_id: int, payload: SalaryPatch):
    with Session(engine) as s:
        obj = s.get(Cat, cat_id) or HTTPException(404)
        obj.salary = payload.salary
        s.add(obj); s.commit(); s.refresh(obj)
        return obj

@router.delete("/{cat_id}", status_code=204)
def delete_cat(cat_id: int):
    with Session(engine) as s:
        obj = s.get(Cat, cat_id) or HTTPException(404)
        s.delete(obj); s.commit()
