from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel, Field
from datetime import datetime
import json
import os

app = FastAPI()

FILE_NAME = "todo.json"

# ---------- Helpers ----------

def read_todos():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)

def write_todos(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)

def get_next_id(todos):
    return max([t["id"] for t in todos], default=0) + 1

# ---------- Models ----------

class CreateTodo(BaseModel):
    todo: str = Field(
        ...,
        min_length=3,
        max_length=200,
        example="Learn FastAPI"
    )

class Todo(BaseModel):
    id: int
    todo: str
    createDate: datetime

class UpdateTodo(BaseModel):
    todo: str = Field(
        None,
        min_length=3,
        max_length=200,
        example="Learn FastAPI"
    )


# ---------- Routes ----------

#  Create a todo

@app.post("/create", response_model=Todo, status_code=201)
def create_todo(todo: CreateTodo):
    todos = read_todos()

    # 🔒 Duplicate validation
    for t in todos:
        if t["todo"].lower() == todo.todo.lower():
            raise HTTPException(
                status_code=400,
                detail="Todo already exists"
            )

    new_todo = Todo(
        id=get_next_id(todos),
        todo=todo.todo,
        createDate=datetime.utcnow()
    )

    todos.append(new_todo.model_dump(mode="json"))
    write_todos(todos)

    return new_todo

# Read todo

@app.get("/todo" , status_code = 200)
def get_todo():
    todo = read_todos()
    if len(todo) == 0:
        raise HTTPException(
                status_code=400,
                detail="empty todo"
            )
    return{
        "message" : "todo successfull fetch",
        "todos" : todo
    }


# DELETE Todo

@app.delete("/todo/{todo_id}" , status_code = 200)
def delete_todo(todo_id:int):
    todos = read_todos()

    for index , todo in enumerate(todos):
        if todo["id"] == todo_id:
            delete_todo = todos.pop(index)
            write_todos(todos)
            return{
                "message" : "todo successfull deleted",
                "deleted_todo" : delete_todo
                }
        raise HTTPException(
            status_code=400,
            detail="invalid todo"
        )

@app.put("/todo/{todo_id}", status_code = 201)
def update_todo(todo_id: int, update_todo: UpdateTodo):
    todos = read_todos()

    for todo in todos:
        if todo["id"] == todo_id:
            todo["todo"] = update_todo.todo   # ✅ correct update

            write_todos(todos)

            return {
                "message": "Successfully updated todo",
                "updated_todo": todo
            }

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )