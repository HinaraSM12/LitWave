# Importaciones de módulos internos de la aplicación
from user.Me import ME
from user.SearchAllUsers import SEARCH_ALL_USERS
from user.SearchUserById import SEARCH_USER_BY_ID
from user.UpdateUsers import UPDATE_USERS

# Definición de las rutas y controladores
USER_ROUTES = [{'path': '/user',
                'tag': 'User',
                'instance': ME},
               {'path': '/user',
                'tag': 'User',
                'instance': SEARCH_USER_BY_ID},
               {'path': '/user',
                'tag': 'User',
                'instance': SEARCH_ALL_USERS},
               {'path': '/user',
                'tag': 'User',
                'instance': UPDATE_USERS}
               ]

