from fastapi import APIRouter, Depends, HTTPException
from db import database

router_usuarios = APIRouter()


@router_usuarios.post("/login/", tags=["Usuarios"])
async def login(username: str, password: str):
    try:
        conn = database.getConnection()
        cursor = conn.cursor()

        query = "SELECT * FROM Usuarios WHERE username = %s AND contrasena = %s"
        cursor.execute(query, (username, password))
        row = cursor.fetchone()

        conn.close()

        if row:
            return {
                "usuario_id": row[0],
                "nombre": row[1],
                "direccion": row[2],
                "telefono": row[3],
                "username": row[4],
                "contrasena": row[5],
                "es_admin": row[6],
            }
        else:
            raise HTTPException(
                status_code=401, detail="Credenciales inválidas")

    except Exception as e:
        return {"error": 'Error al iniciar sesión'}
