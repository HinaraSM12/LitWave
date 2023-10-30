# Importaciones de librerías estándar de Python
import re
from typing import Literal
from bson import ObjectId

# Importaciones de librerías de terceros
from fastapi import APIRouter, Request, Header

# Importaciones de módulos internos de la aplicación
from book.Book import Book
from db.PaginatedSearch import paginated_search
from jwt_utils.Guard import validate_token

SEARCH_ALL_USER_BOOKS = APIRouter()


@SEARCH_ALL_USER_BOOKS.get("/list/{type_of_list}",
                           response_description="List all user books")
def list_user_books(request: Request,
                    type_of_list: Literal['reading', 'favorite', 'read'],
                    limit=15, page=1,
                    search_param='',
                    authentication: str = Header(...)):
    # TODO: Documentar
    # Validar el token de autenticación utilizando la función validate_token
    token_data = validate_token(authentication)
    user_id = token_data['id']
    query = paginated_search(
        page=int(page), limit=int(limit),
        query={
            "$or": [
                {'title': re.compile(f'{search_param}', re.IGNORECASE)},
                {'author': re.compile(f'{search_param}', re.IGNORECASE)}
            ],
        },
        pre_query=[
            {
                '$match': {
                    type_of_list: True,
                    'user_id': ObjectId(user_id)
                }
            }, {
                '$lookup': {
                    'from': 'books',
                    'localField': 'book_id',
                    'foreignField': '_id',
                    'as': 'book'
                }
            }, {
                '$unwind': {
                    'path': '$book',
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$project': {
                    '_id': '$book._id',
                    'isbn_code': '$book.isbn_code',
                    'title': '$book.title',
                    'author': '$book.author',
                    'image': '$book.image'
                }
            }
        ]
    )
    # Realiza una búsqueda en la base de datos de libros utilizando paginación
    books = list(request.app.database['user_books'].aggregate(
        query))

    # Si se encuentran libros, se crea una respuesta con los datos y metadatos
    response = books[0] if len(books) > 0 else {'data': [], 'metadata': {
        'total': 0,
        'page': 0,
        'total_pages': 0,
    }}
    response['data'] = list(map(lambda x: Book(**x), response["data"]))
    return response
