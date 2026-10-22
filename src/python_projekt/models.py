from sqlalchemy import Identity, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Mitglied(Base):
    __tablename__ = "mitglied"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    vorname: Mapped[str] = mapped_column(Text)
    nachname: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text)
