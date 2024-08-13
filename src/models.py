import datetime

from typing import Annotated
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base, str_256
import enum

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc',now())"))]
updated_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc',now())"), onupdate=datetime.datetime.utcnow())]


class WorkersOrm(Base):
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String)

    resumes: Mapped[list["ResumesOrm"]] = relationship(
        back_populates='worker'
    )
    resumes_parttime: Mapped[list["ResumesOrm"]] = relationship(
        back_populates='worker',
        primaryjoin="and_(WorkersOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'parttime')",
    )


class Workload(enum.Enum):
    parttime = 'parttime'
    fulltime = 'fulltime'


class ResumesOrm(Base):
    __tablename__ = "resumes"
    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[int | None] = mapped_column(Integer)
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    vacancies_replied: Mapped[list["VacanciesOrm"]] = relationship(
        back_populates='resumes_replied',
        secondary='vacancies_replies',
    )

    repr_cols_num = 10
    repr_cols = 'title'

    worker: Mapped["WorkersOrm"] = relationship(
        back_populates='resumes',
    )


class VacanciesOrm(Base):
    __tablename__ = "vacancies"

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[int | None] = mapped_column(Integer)

    resumes_replied: Mapped[list["ResumesOrm"]] = relationship(
        back_populates='vacancies_replied',
        secondary='vacancies_replies',
    )


class VacanciesRepliesOrm(Base):
    __tablename__ = "vacancies_replies"

    resumes_id: Mapped[intpk] = mapped_column(
        ForeignKey("resumes.id", ondelete='CASCADE'),
        primary_key=True,
    )
    vacancies_id: Mapped[intpk] = mapped_column(
        ForeignKey("vacancies.id", ondelete='CASCADE'),
        primary_key=True,
    )
    cover_latter: Mapped[str | None] = mapped_column(String)


metadata = MetaData()

workers_table = Table(
    'workers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50)),
)
