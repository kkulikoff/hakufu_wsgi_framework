import os
import datetime
from pprint import pprint
from quopri import decodestring

from .constants import CONTENT_TYPE
from .requests import GetRequests, PostRequests

STATIC_DIR_NAME = 'static'
STATIC_DIR = f'{os.getcwd()}/{STATIC_DIR_NAME}'


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']
        # pprint(environ)

        if '/static/' in path:
            file_path = STATIC_DIR + path.replace('/static', '')
            if path[-1] == '/':
                list_files = '<br>'.join(os.listdir(file_path))

                template = f"directory: ${STATIC_DIR} {list_files}"
                start_response('200 OK', [('Content-Type', 'text/html')])
                return [template.encode('utf-8')]

            else:
                status = '200 OK'
                with open(file_path, 'rb') as f:
                    data = f.read()
                content_type = ''

                for k, v in CONTENT_TYPE.items():
                    if k in path:
                        content_type = v

                response_headers = [
                    ('Content-type', content_type),
                    ('Content_Lenght', str(len(data)))
                ]
                start_response(status, response_headers)
                return [data]


        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method
        # pprint(environ)
###################################### Разкоментировать на хостинге ########################################
        # request['referer'] = environ['HTTP_REFERER'] #
        # request['r_address'] = environ['REMOTE_ADDR']


        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = Framework.decode_value(data)
            pprint(f'Нам пришёл post-запрос: {Framework.decode_value(data)}')

###################################### Разкоментировать на хостинге ########################################
            # with open("log/post_log.log", "a", encoding='utf-8') as file_post:
            #     temp_str = ''
            #     today = datetime.datetime.today()
            #     for k_line_post, v_line_post in Framework.decode_value(data).items():
            #         temp_str += f'{k_line_post}: {v_line_post}; '
            #     file_post.write(f'{today.strftime("%Y:%m:%d %H:%M:%S")} - - {temp_str}\n')
############################################################################################################

        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = Framework.decode_value(request_params)
            pprint(f'Нам пришли GET-параметры:'
                  f' {Framework.decode_value(request_params)}')

###################################### Разкоментировать на хостинге ########################################
            # with open("log/get_log.log", "a", encoding='utf-8') as file_get:
            #     temp_str = ''
            #     today = datetime.datetime.today()
            #     for k_line_get, v_line_get in Framework.decode_value(request_params).items():
            #         temp_str += f'{k_line_get}: {v_line_get}; '
            #     if len(temp_str) > 1:
            #         file_get.write(f'{today.strftime("%Y:%m:%d %H:%M:%S")} - - {temp_str}\n')
            #     file_get.write(f'{today.strftime("%Y:%m:%d %H:%M:%S")} - - '
            #                    f' Пользователь {request["r_address"]} пришел от {request["referer"]}\n')
############################################################################################################
        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()
        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data

# Новый вид WSGI-application.
# Первый — логирующий (такой же, как основной,
# только для каждого запроса выводит информацию
# (тип запроса и параметры) в консоль.
class DebugApplication(Framework):

    def __init__(self, routes_obj, fronts_obj):
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


# Новый вид WSGI-application.
# Второй — фейковый (на все запросы пользователя отвечает:
# 200 OK, Hello from Fake).
class FakeApplication(Framework):

    def __init__(self, routes_obj, fronts_obj):
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']