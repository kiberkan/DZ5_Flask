from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List

#Инструкция:
#1- Запустите сервер: uvicorn main:app --reload
#для работы с API,Postman или curl
#для добавления новой задачи POST-запрос к /tasks с JSON-данными:
#{
#  "title": "Новая задача",
#  "description": "Описание новой задачи",
#  "status": false
#}
#Для получения списка всех задач GET-запрос к /tasks.

app = FastAPI()

class Task(BaseModel):
    id: int = None
    title: str = Field(..., title="Заголовок задачи", max_length=100)
    description: str = Field(..., title="Описание задачи", max_length=500)
    status: bool = Field(False, title="Статус выполнения")

    @validator("title")
    def title_must_be_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Заголовок задачи не может быть пустым.")
        return value

    @validator("description")
    def description_must_be_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Описание задачи не может быть пустым.")
        return value

tasks = []
next_id = 1

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Возвращает список всех задач"""
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Возвращает задачу с указанным идентификатором"""
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: Task):
    """Добавляет новую задачу"""
    global next_id
    task.id = next_id
    next_id += 1
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    """Обновляет задачу с указанным идентификатором"""
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    task.title = updated_task.title
    task.description = updated_task.description
    task.status = updated_task.status
    return task

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """Удаляет задачу с указанным идентификатором"""
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    tasks.remove(task)
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)