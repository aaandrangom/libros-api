from db import database
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

router_libros = APIRouter()


class LibroActualizar(BaseModel):
    titulo: str
    autor: str
    genero: str


@router_libros.post("/libros/", tags=["Libros"])
async def crear_libro(titulo: str, autor: str, genero: str):
    try:
        conn = database.getConnection()
        cursor = conn.cursor()

        insert_query = "INSERT INTO Libros (titulo, autor, genero) VALUES (%s, %s, %s) RETURNING id, titulo, autor, genero"
        cursor.execute(insert_query, (titulo, autor, genero))
        libro_details = cursor.fetchone()

        conn.commit()
        conn.close()

        if libro_details:
            libro = {
                "id": libro_details[0],
                "titulo": libro_details[1],
                "autor": libro_details[2],
                "genero": libro_details[3]
            }
            return {"mensaje": "Libro creado correctamente", "libro": libro}
        else:
            raise HTTPException(
                status_code=500, detail="Error al obtener detalles del libro creado")

    except Exception as e:
        return {"error": 'Error al crear el libro'}


@router_libros.get("/libros/", tags=["Libros"])
async def obtener_libros():
    try:
        conn = database.getConnection()
        cursor = conn.cursor()

        query = "SELECT id, titulo, autor, genero FROM Libros"
        cursor.execute(query)
        libros = cursor.fetchall()

        conn.close()

        if libros:
            libros_list = []
            for libro_details in libros:
                libro = {
                    "id": libro_details[0],
                    "titulo": libro_details[1],
                    "autor": libro_details[2],
                    "genero": libro_details[3]
                }
                libros_list.append(libro)
            return {"mensaje": "Libros obtenidos correctamente", "libros": libros_list}
        else:
            return []

    except Exception as e:
        return {"error": 'Error al obtener los libros', "exception": e}


@router_libros.get("/libros/{libro_id}", tags=["Libros"])
async def obtener_libro_por_id(libro_id: int):
    try:
        conn = database.getConnection()
        cursor = conn.cursor()

        query = "SELECT id, titulo, autor, genero FROM Libros WHERE id = %s"
        cursor.execute(query, (libro_id,))
        libro_details = cursor.fetchone()

        conn.close()

        if libro_details:
            libro = {
                "id": libro_details[0],
                "titulo": libro_details[1],
                "autor": libro_details[2],
                "genero": libro_details[3]
            }
            return {"mensaje": "Libro obtenido correctamente", "libro": libro}
        else:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

    except Exception as e:
        return {"error": 'Error al obtener el libro por ID'}


@router_libros.put("/libros/{libro_id}", tags=["Libros"])
async def actualizar_libro(libro_id: int, libro_data: LibroActualizar):
    try:
        conn = database.getConnection()
        cursor = conn.cursor()

        update_query = "UPDATE Libros SET titulo = %s, autor = %s, genero = %s WHERE id = %s"
        cursor.execute(update_query, (libro_data.titulo,
                       libro_data.autor, libro_data.genero, libro_id))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        select_query = "SELECT id, titulo, autor, genero FROM Libros WHERE id = %s"
        cursor.execute(select_query, (libro_id,))
        libro_details = cursor.fetchone()

        conn.commit()
        conn.close()

        libro_actualizado = {
            "id": libro_details[0],
            "titulo": libro_details[1],
            "autor": libro_details[2],
            "genero": libro_details[3]
        }

        return {"mensaje": "Libro actualizado correctamente", "libro": libro_actualizado}

    except Exception as e:
        return {"error": 'Error al actualizar el libro'}


@router_libros.delete("/libros/eliminar/{libro_id}", tags=["Libros"])
async def eliminar_libro(libro_id: int):
    try:
        conn = database.getConnection()
        cursor = conn.cursor()

        # Verificar si el libro existe antes de eliminarlo
        existencia_query = "SELECT id FROM Libros WHERE id = %s"
        cursor.execute(existencia_query, (libro_id,))
        existe_libro = cursor.fetchone()

        if not existe_libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        # Eliminar el libro
        delete_query = "DELETE FROM Libros WHERE id = %s RETURNING id, titulo, autor, genero"
        cursor.execute(delete_query, (libro_id,))
        libro_eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        if libro_eliminado:
            libro = {
                "id": libro_eliminado[0],
                "titulo": libro_eliminado[1],
                "autor": libro_eliminado[2],
                "genero": libro_eliminado[3]
            }
            return {"mensaje": "Libro eliminado correctamente", "libro": libro}
        else:
            raise HTTPException(
                status_code=404, detail="Error al eliminar el libro")

    except Exception as e:
        return {"error": 'Error al eliminar el libro'}

