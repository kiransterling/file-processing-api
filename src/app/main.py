from fastapi import BackgroundTasks, FastAPI,File, UploadFile,Response,HTTPException
from fastapi.responses import FileResponse
from app.modules.process_file import process_file,check_file_status
import aiofiles
import os,re,uuid

app = FastAPI(title="FileProcessingApp",
             description="This application processes a file excel file and converts in csv",
             version="0.0.1",
             contact={
                 "name": "Kashyap Kiran Das",
                 "email": "kashyap.kiran.1729@gmail.com"
             })




@app.post("/api/uploadFile",status_code=201)
async def upload_file(response: Response,background_tasks: BackgroundTasks,file: UploadFile = File(...)):
    process_id = str(uuid.uuid4())
    async with aiofiles.open(process_id+"_"+file.filename, 'wb') as out_file:
        while content := await file.read(1024*2):
            await out_file.write(content)
    background_tasks.add_task(process_file,process_id,file.filename)
    response.status_code = 201
    return {"filename": file.filename,"process_id":process_id,"description":"Please check your file status here --> /api/getFileStatus/"+process_id}


@app.get("/api/getFileStatus/{process_id}")
def get_file_status(response: Response,process_id):
    if check_file_status(process_id)=='NOT_FOUND':
        raise HTTPException(
            status_code=404,
            detail="Process "+process_id+" does not exsists",
            headers={"X-Error": "NOT_FOUND"},
        )
    else:
        response.status_code = 200
        return {"processId": process_id,"Status": check_file_status(process_id)}

@app.get("/api/downLoadFile/{process_id}")
def download_file(response: Response,process_id):
    if check_file_status(process_id)=='NOT_FOUND':
        raise HTTPException(
            status_code=404,
            detail="Process "+process_id+" does not exsists",
            headers={"X-Error": "NOT_FOUND"},
        )
    elif check_file_status(process_id)=='COMPLETED':
       for f in os.listdir('.'):
           if re.match(process_id, f):
              response.status_code = 200
              return FileResponse(path=f, filename=f)
    else:
        response.status_code = 200
        return {"processId": process_id,"Status": check_file_status(process_id),"Description":"Please wait , The file is getting processed. "}



