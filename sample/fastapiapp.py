from fastapi import FastAPI #import class FastAPI() từ thư viện fastapi
from string_helper import isnull
app = FastAPI() # gọi constructor và gán vào biến app


@app.get("/welcome") # giống flask, khai báo phương thức get và url
async def root(name: str, age: int): # do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
    return isnull(name)
    return {"name": name, "age": age}