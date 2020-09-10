from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


def process_items(items: List[str]):
    for item in items:
        print(item)

app = FastAPI()

task_id: int = 0

class Task(BaseModel):
    id: int = task_id
    name: str
    description: str
    is_done: bool = False

class TaskCreateDTO(BaseModel):
    name: str
    description: str

class TaskPatchDTO(BaseModel):
    name: Optional[str]
    description: Optional[str]
    is_done: Optional[bool]

task_list: List[Task] = []



@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/tasks/")
def create_task(taskCreateDTO: TaskCreateDTO):
    global task_id , task_list
    task_id += 1
    task = Task()
    task.id = task_id
    task.description = taskCreateDTO.description
    task.name = taskCreateDTO.name
    task_list.append(task)
    return task


@app.get("/tasks/")
async def get_tasks(is_done: Optional[bool] = None):
    global task_list
    final_task_list: Task = []
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


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    global task_list
    for e in task_list:
        if(e.id == task_id):
            task_list.remove(e)
            return {"Task with id {0} removed!".format(task_id)}
    
    return {"Task with id {0} not found!".format(task_id)}

@app.patch("/tasks/{task_id}")
async def patch_task_(task_id: int, task_patchDTO: TaskPatchDTO):
    global task_list
    for e in task_list:
        if(e.id == task_id):
            #task_list[task_list.index(e)].description = task_patchDTO.description
            if(task_patchDTO.is_done != None):
                e.is_done = task_patchDTO.is_done
            if(task_patchDTO.name):
                e.name = task_patchDTO.name
            if(task_patchDTO.description):
                e.description = task_patchDTO.description

            return e
    
    return {"Task with id {0} not found!".format(task_id)}
    