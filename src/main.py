import os
import sys
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from src.queries.orm import SyncORM
from src.queries.orm import AsyncORM
from src.queries.core import SyncCore
from src.queries.core import AsyncCore

# SyncORM.create_tables()
SyncORM.insert_additional_resumes()
SyncORM.add_vacancies_and_replies()
# SyncORM.select_resumes_with_all_relationships()
# SyncORM.select_resumes_avg_compensation()
# SyncORM.insert_self_additional_resumes("Python developer", 200000, 'fulltime', 3)
# SyncORM.select_resumes_workload()
# asyncio.run(AsyncORM.join_cte_subquery_window_func())
# SyncORM.select_workers_with_selected_relationships()
# SyncORM.selected_workers_with_condition_relationships()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

@app.get("/resumes")
async def get_workers():
    workers = SyncORM.select_resumes_with_all_relationships()
    return workers


