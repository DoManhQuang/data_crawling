from fastapi import FastAPI #import class FastAPI() từ thư viện fastapi
app = FastAPI() # gọi constructor và gán vào biến app

@app.get("/")
async def index():
   return {"message": "Hello World"}