import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from python_projekt.db import get_db
from python_projekt.models import Mitglied
from python_projekt.schemas import MitgliedRead

app = FastAPI()


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/mitglieder", response_model=list[MitgliedRead])
def list_mitglieder(
    nachname: str | None = None,
    db: Session = Depends(get_db),
) -> list[MitgliedRead]:
    stmt = select(Mitglied)
    if nachname is not None:
        stmt = stmt.where(Mitglied.nachname == nachname)
    return list(db.scalars(stmt).all())


@app.get("/mitglieder/{mitglied_id}", response_model=MitgliedRead)
def get_mitglied(
    mitglied_id: int,
    db: Session = Depends(get_db),
) -> MitgliedRead:
    mitglied = db.get(Mitglied, mitglied_id)
    if mitglied is None:
        raise HTTPException(status_code=404, detail="Mitglied nicht gefunden")
    return mitglied


def main() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8000)
