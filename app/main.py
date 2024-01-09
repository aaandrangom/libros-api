from fastapi import FastAPI
from usuarios import router_usuarios
from libros import router_libros

app = FastAPI()

app.include_router(router_usuarios, prefix="/api/v1")
app.include_router(router_libros, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
