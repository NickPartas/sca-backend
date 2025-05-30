# app/schemas.py
from pydantic import BaseModel, Field, validator
import httpx, functools, os

CAT_API_URL = "https://api.thecatapi.com/v1/breeds"


@functools.lru_cache(maxsize=1)
def _breeds() -> set[str]:
    r = httpx.get(CAT_API_URL, timeout=10)
    r.raise_for_status()
    return {b["name"].lower() for b in r.json()}



class CatCreate(BaseModel):
    name: str
    years_experience: int = Field(ge=0)
    breed: str
    salary: float = Field(gt=0)

    @validator("breed")
    def breed_exists(cls, v: str) -> str:
        if v.lower() not in _breeds():
            raise ValueError("Unknown cat breed")
        return v


class CatRead(CatCreate):
    id: int
    model_config = {"from_attributes": True}

class SalaryPatch(BaseModel):
    salary: float = Field(gt=0)

class TargetOut(BaseModel):
    id: int
    name: str
    country: str
    notes: str
    complete: bool
    model_config = {"from_attributes": True}

class MissionRead(BaseModel):
    id: int
    complete: bool
    cat_id: int | None
    targets: list[TargetOut]
    model_config = {"from_attributes": True}