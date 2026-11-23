from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from itertools import count

class Task(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

app = FastAPI()

tasks = []

counter = count(start=1, step=1)


@app.get("/tasks", status_code=200)
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", status_code=200)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

@app.post("/tasks", status_code=201)
def post_task(task: Task):
    if(task.title.strip() == ""):
        raise HTTPException(
            status_code=422,
            detail="Title can't be empty"
        )
    task1 = task.model_dump()

    task1["id"] = next(counter)
    tasks.append(task1)
    return task1

@app.put("/tasks/{task_id}", status_code=200)
def put_tasks(task_id: int, task1: Task):
    if(task1.title.strip() == ""):
        raise HTTPException(
            status_code=422,
            detail="Title can't be empty"
        )
    for i in range(len(tasks)):
        if tasks[i]["id"] == task_id:
            task = task1.model_dump()
            task["id"] = task_id
            tasks[i] = task
            return task
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

@app.delete("/tasks/{task_id}", status_code=204)
def del_tasks(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

