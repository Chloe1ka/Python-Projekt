from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from python_projekt.db import get_db
from python_projekt.models import Mitglied
from python_projekt.schemas import MitgliedCreate, MitgliedRead

app = FastAPI()


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/mitglieder")
def list_mitglieder(
    db: Annotated[Session, Depends(get_db)],
    nachname: str | None = None,
) -> list[MitgliedRead]:
    stmt = select(Mitglied)
    if nachname is not None:
        stmt = stmt.where(Mitglied.nachname == nachname)
    return [MitgliedRead.model_validate(row) for row in db.scalars(stmt).all()]


@app.post("/mitglieder", status_code=201)
def create_mitglied(
    body: MitgliedCreate,
    db: Annotated[Session, Depends(get_db)],
) -> MitgliedRead:
    mitglied = Mitglied(
        vorname=body.vorname,
        nachname=body.nachname,
        email=body.email,
    )
    db.add(mitglied)
    db.commit()
    db.refresh(mitglied)
    return MitgliedRead.model_validate(mitglied)


@app.get("/mitglieder/{mitglied_id}", response_model=MitgliedRead)
def get_mitglied(
    mitglied_id: int,
    request: Request,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> MitgliedRead | Response:
    mitglied = db.get(Mitglied, mitglied_id)
    if mitglied is None:
        raise HTTPException(status_code=404, detail="Mitglied nicht gefunden")
    etag = f'"{mitglied.version}"'
    # Conditional GET returns 304 when If-None-Match matches the ETag (member version).
    if request.headers.get("If-None-Match") == etag:
        return Response(status_code=304, headers={"ETag": etag})
    response.headers["ETag"] = etag
    return MitgliedRead.model_validate(mitglied)


def main() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8001)
