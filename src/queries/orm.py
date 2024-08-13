from src.database import async_engine, sync_engine, sync_session, async_session, Base
from src.models import *

from sqlalchemy import text, insert, select, delete, func, cast, and_
from sqlalchemy.orm import aliased, joinedload, selectinload

from src.schemas import WorkersRelDTO, ResumesRelVacanciesRelationDTO


class SyncORM:
    @staticmethod
    def create_tables():
        Base.metadata.drop_all(sync_engine)
        # sync_engine.echo = False
        Base.metadata.create_all(sync_engine)
        # sync_engine.echo = True

    @staticmethod
    def insert_data():
        with sync_session() as session:
            worker_Bobr = WorkersOrm(username="Bobr")
            worker_Volk = WorkersOrm(username="Volk")
            session.add_all([worker_Bobr, worker_Volk])
            session.flush()
            session.commit()

    @staticmethod
    def select_data():
        with sync_session() as session:
            query = select(WorkersOrm)
            result = session.execute(query)
            workers = result.scalars().all()
            print(f'{workers=}')

    @staticmethod
    def update_data(worker_id: int = 2, new_username: str = "Sonya"):
        with sync_session() as session:
            worker = session.get(WorkersOrm, worker_id)
            worker.username = new_username
            session.commit()

    @staticmethod
    def insert_additional_resumes():
        with sync_session() as session:
            workers = [
                {'id': 3, "username": "Artem"},  # id 3
                {'id': 4, "username": "Roman"},  # id 4
                {'id': 5, "username": "Petr"},  # id 5
            ]
            resumes = [
                {"title": "Python программист", "compensation": 60000, "workload": "fulltime", "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000, "workload": "parttime", "worker_id": 3},
                {"title": "Python Data Scientist", "compensation": 80000, "workload": "parttime", "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000, "workload": "fulltime", "worker_id": 4},
                {"title": "Python Junior Developer", "compensation": 100000, "workload": "fulltime", "worker_id": 5},
            ]
            insert_workers = insert(WorkersOrm).values(workers)
            insert_resumes = insert(ResumesOrm).values(resumes)
            session.execute(insert_workers)
            session.execute(insert_resumes)
            session.commit()

    @staticmethod
    def insert_self_additional_resumes(title: str, compensation: int, workload: str, worker_id: int):
        with sync_session() as session:
            new_resume = ResumesOrm(title=title, compensation=compensation, workload=workload, worker_id=worker_id)
            session.add(new_resume)
            session.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_languages: str = "Python"):
        with sync_session() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation")
                )
                .select_from(ResumesOrm)
                .where(and_(
                    ResumesOrm.title.contains(like_languages),
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
            )
            result = session.execute(query)
            print(f'{result.all()=}')

    @staticmethod
    def select_resumes_workload(workload: str = 'fulltime'):
        with sync_session() as session:
            query = (
                select(
                    ResumesOrm.title,
                    ResumesOrm.compensation,
                    ResumesOrm.worker_id,
                    ResumesOrm.workload,
                )
                .select_from(ResumesOrm)
                .filter_by(
                    workload=workload
                )
            )
            result = session.execute(query)
            print(f'{result.all()=}')

    @staticmethod
    def select_workers_with_lazy_relationships():
        with sync_session() as session:
            query = (
                select(WorkersOrm)
            )
            res = session.execute(query)
            result = res.scalars().all()
            worker_1_resumes = result[0].resumes
            print(f'{worker_1_resumes=}')
            worker_2_resumes = result[1].resumes
            print(f'{worker_2_resumes=}')

    @staticmethod
    def select_workers_with_joined_relationships():
        with sync_session() as session:
            query = (
                select(WorkersOrm)
                .options(joinedload(WorkersOrm.resumes))
            )
            res = session.execute(query)
            result = res.unique().scalars().all()
            worker_1_resumes = result[0].resumes
            print(f'{worker_1_resumes=}')
            worker_2_resumes = result[1].resumes
            print(f'{worker_2_resumes=}')

    @staticmethod
    def select_workers_with_selected_relationships():
        with sync_session() as session:
            query = (
                select(WorkersOrm)
                .options(selectinload(WorkersOrm.resumes))
            )
            res = session.execute(query)
            result = res.scalars().all()
            worker_1_resumes = result[0].resumes
            print(f'{worker_1_resumes=}')
            worker_2_resumes = result[1].resumes
            print(f'{worker_2_resumes=}')

    @staticmethod
    def selected_workers_with_condition_relationships():
        with sync_session() as session:
            query = (
                select(WorkersOrm)
                .options(selectinload(WorkersOrm.resumes_parttime))
            )
            res = session.execute(query)
            result = res.scalars().all()
            print(result)

    @staticmethod
    def convert_workers_to_dto():
        with sync_session() as session:
            query = (
                select(WorkersOrm)
                .options(selectinload(WorkersOrm.resumes))
                .limit(2)
            )

            res = session.execute(query)
            result_orm = res.scalars().all()
            print(f"{result_orm=}")
            result_dto = [WorkersRelDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto

    @staticmethod
    def add_vacancies_and_replies():
        with sync_session() as session:
            new_vacancy = VacanciesOrm(title='Python developer', compensation=14980)
            resume_1 = session.get(ResumesOrm, 1)
            resume_2 = session.get(ResumesOrm, 2)
            resume_1.vacancies_replied.append(new_vacancy)
            resume_2.vacancies_replied.append(new_vacancy)
            session.commit()

    @staticmethod
    def select_resumes_with_all_relationships():
        with sync_session() as session:
            query = (
                select(ResumesOrm)
                .options(joinedload(ResumesOrm.worker))
                .options(selectinload(ResumesOrm.vacancies_replied).load_only(VacanciesOrm.title))
            )
            res = session.execute(query)
            result = res.unique().scalars().all()
            result_dto = [ResumesRelVacanciesRelationDTO.model_validate(row, from_attributes=True) for row in result]
            return result_dto

class AsyncORM:
    @staticmethod
    async def async_insert_data():
        async with async_session() as session:
            worker_Bobr = WorkersOrm(username="Bobr")
            worker_Volk = WorkersOrm(username="Volk")
            session.add_all([worker_Bobr, worker_Volk])
            await session.commit()

    @staticmethod
    async def join_cte_subquery_window_func(like_languages: str = "Python"):
        async with async_session() as session:
            r = aliased(ResumesOrm)
            w = aliased(WorkersOrm)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.compensation)
                    .over(partition_by=r.workload)
                    .cast(Integer)
                    .label("avg_workload_compensation"),
                )
                .join(r, r.worker_id == w.id).subquery("helper1")
            )
            cte = (
                select(
                    subq.c.worker_id,
                    subq.c.username,
                    subq.c.compensation,
                    subq.c.workload,
                    subq.c.avg_workload_compensation,
                    (subq.c.compensation - subq.c.avg_workload_compensation).label("compensation_diff"),
                )
                .cte("helper2")
            )
            query = (
                select(cte)
                .order_by(cte.c.compensation_diff.desc())
            )
            res = await session.execute(query)
            result = res.all()
            print(f'{result=}')