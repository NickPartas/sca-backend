from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Mission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    complete: bool = False
    cat_id: Optional[int] = Field(default=None, foreign_key="cat.id")


    cat: Optional["Cat"] = Relationship(back_populates="mission")

    targets: List["Target"] = Relationship(back_populates="mission")


class Cat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    years_experience: int
    breed: str
    salary: float


    mission: Optional[Mission] = Relationship(back_populates="cat")


class Target(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mission_id: int = Field(foreign_key="mission.id")
    name: str
    country: str
    notes: str = ""
    complete: bool = False

    mission: Mission = Relationship(back_populates="targets")
