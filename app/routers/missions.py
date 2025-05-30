# app/routers/missions.py
from fastapi import APIRouter, HTTPException, Body, Path
from typing import List, Optional
from sqlmodel import Session, select
from ..db import engine
from ..models import Mission, Target, Cat
from pydantic import BaseModel, Field, validator

router = APIRouter(prefix="/missions", tags=["missions"])

# ────────────────────────────
# Pydantic schemas
# ────────────────────────────
class TargetIn(BaseModel):
    name: str
    country: str
    notes: str = ""

class MissionCreate(BaseModel):
    cat_id: Optional[int] = None
    targets: List[TargetIn]

    @validator("targets")
    def validate_targets_len(cls, v):
        if not (1 <= len(v) <= 3):
            raise ValueError("Mission must contain 1-3 targets")
        return v

class TargetPatch(BaseModel):
    notes: Optional[str] = None
    complete: Optional[bool] = None

class MissionRead(BaseModel):
    id: int
    complete: bool
    cat_id: Optional[int]
    targets: List[TargetIn]

    class Config:
        orm_mode = True

# ────────────────────────────
# Helpers
# ────────────────────────────
def get_mission(session: Session, mid: int) -> Mission:
    mission = session.get(Mission, mid)
    if not mission:
        raise HTTPException(404, "Mission not found")
    return mission

def get_cat(session: Session, cid: int) -> Cat:
    cat = session.get(Cat, cid)
    if not cat:
        raise HTTPException(404, "Cat not found")
    if cat.mission:                                                   # already on a mission
        raise HTTPException(409, "Cat already assigned to a mission")
    return cat

# ────────────────────────────
# Endpoints
# ────────────────────────────

@router.post("/", response_model=MissionRead, status_code=201)
def create_mission(payload: MissionCreate):
    with Session(engine) as s:
        # optional cat assignment
        cat: Optional[Cat] = None
        if payload.cat_id is not None:
            cat = get_cat(s, payload.cat_id)

        mission = Mission(cat_id=cat.id if cat else None)
        s.add(mission)
        s.flush()                                    # mission.id available

        for t in payload.targets:
            target = Target(
                mission_id=mission.id,
                name=t.name,
                country=t.country,
                notes=t.notes,
            )
            s.add(target)

        s.commit()
        s.refresh(mission)
        return mission


@router.get("/", response_model=List[MissionRead])
def list_missions():
    with Session(engine) as s:
        return s.exec(select(Mission)).all()


@router.get("/{mid}", response_model=MissionRead)
def get_single(mid: int = Path(..., gt=0)):
    with Session(engine) as s:
        return get_mission(s, mid)


@router.patch("/{mid}/assign", response_model=MissionRead)
def assign_cat(mid: int, cat_id: int = Body(..., embed=True)):
    with Session(engine) as s:
        mission = get_mission(s, mid)
        if mission.complete:
            raise HTTPException(409, "Mission already completed")
        if mission.cat_id is not None:
            raise HTTPException(409, "Mission already assigned to a cat")

        cat = get_cat(s, cat_id)
        mission.cat_id = cat.id
        s.add(mission)
        s.commit()
        s.refresh(mission)
        return mission


@router.patch("/{mid}/targets/{tid}", response_model=MissionRead)
def update_target(
    mid: int,
    tid: int,
    payload: TargetPatch,
):
    with Session(engine) as s:
        mission = get_mission(s, mid)
        if mission.complete:
            raise HTTPException(409, "Mission already completed")

        target: Target = s.get(Target, tid)
        if not target or target.mission_id != mission.id:
            raise HTTPException(404, "Target not found in this mission")

        if target.complete:
            raise HTTPException(409, "Target already completed")

        if payload.notes is not None:
            target.notes = payload.notes
        if payload.complete is not None:
            target.complete = payload.complete

        s.add(target)

        # auto-complete mission if all targets complete
        all_done = all(t.complete for t in mission.targets)
        if all_done:
            mission.complete = True
            s.add(mission)

        s.commit()
        s.refresh(mission)
        return mission


@router.delete("/{mid}", status_code=204)
def delete_mission(mid: int):
    with Session(engine) as s:
        mission = get_mission(s, mid)
        if mission.cat_id is not None:
            raise HTTPException(409, "Cannot delete: mission already assigned to a cat")

        # cascade delete targets
        for t in mission.targets:
            s.delete(t)
        s.delete(mission)
        s.commit()
