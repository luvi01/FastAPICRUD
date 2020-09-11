from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title = "Lista de Tarefas")

task_id: int = 0

class Task(BaseModel):
    id: int = task_id
    name: Optional[str]
    description: Optional[str]
    is_done: bool = False

class TaskPatchDTO(BaseModel):
    name: Optional[str]
    description: Optional[str]
    is_done: Optional[bool]

class TaskCreateDTO(BaseModel):
    name: str
    description: str

task_list: List[Task] = []


@app.post("/tasks/", tags=["Tasks Controller"], status_code=201,
    summary="Cria uma Tarefa",
    description="Rota responsavel por criar uma nova tarefa",
    response_description="Nova tarefa",
    response_model=Task)
def create_task(taskCreateDTO: TaskCreateDTO, response: Response):
    global task_id , task_list
    task_id += 1
    task = Task()
    task.name = taskCreateDTO.name
    task.description = taskCreateDTO.description
    task.id = task_id
    task_list.append(task)
    return task


@app.get("/tasks/", tags=["Tasks Controller"], status_code=200,
    summary="Consulta de tarefas",
    description="Rota responsavel por consultar as tarefas na base de dados. Caso a query seja vazia retorna todas as tarefas, caso True retorna apenas as tarefas concluidas, caso False retorna as tarefas não concluidas.",
    response_description="Tarefas",
    response_model=List[Task])
async def get_tasks(is_done: Optional[bool] = None):
    global task_list
    final_task_list: List[Task] = []
    if(is_done == None):
        return task_list
    elif(is_done):
        for e in task_list:
            if (e.is_done):
               final_task_list.append(e) 
        return final_task_list
    else:
        for e in task_list:
            if (not e.is_done):
               final_task_list.append(e) 
        return final_task_list


@app.delete("/tasks/{task_id}", tags=["Tasks Controller"], status_code=200,
    summary="Deleta uma tarefa",
    description="Rota responsavel por deletar uma tarefa pelo seu task_id",
    response_description="Status")
async def delete_task(task_id: int, response: Response):
    global task_list
    for e in task_list:
        if(e.id == task_id):
            task_list.remove(e)
            return {"Task with id {0} removed!".format(task_id)}


    raise HTTPException(status_code=404, detail="Task with id {0} not found!".format(task_id))

@app.patch("/tasks/{task_id}", tags=["Tasks Controller"], status_code=200,
    summary="Modifica uma tarefa",
    description="Rota responsavel por modificar uma tarefa pelo seu task_id",
    response_description="Tarefas",
    response_model=Task)
async def patch_task_(task_id: int, task_patchDTO: TaskPatchDTO, response: Response):
    global task_list
    for e in task_list:
        print("OI")
        if(e.id == task_id):
            if(task_patchDTO.is_done != None):
                e.is_done = task_patchDTO.is_done
            if(task_patchDTO.name):
                e.name = task_patchDTO.name
            if(task_patchDTO.description):
                e.description = task_patchDTO.description

            return e

    raise HTTPException(status_code=404, detail="Task with id {0} not found!".format(task_id))

    