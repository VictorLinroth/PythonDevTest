
import subprocess
import asyncio

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

class ListFolder(BaseModel):
    folder_name: str
    delay_call: int

app = FastAPI()

@app.get("/")
async def list_current():
    result=subprocess.run(['ls'],capture_output=True,text=True)
    return {"folder_content": result.stdout.splitlines()}

@app.post("/ls/")
async def list_folder(item: ListFolder):

    if item.delay_call > 0:
        await asyncio.sleep(item.delay_call)

    result = subprocess.run(['ls',item.folder_name],capture_output=True,text=True)
    if result.returncode != 0:
        raise HTTPException(status_code=404, detail=''.join(result.stderr.splitlines()))
        #raise HTTPException(status_code=404, detail="No folder named "+item.folder_name)
    
    return {"folder_content": result.stdout.splitlines()}
