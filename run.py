from wsgiref.simple_server import make_server

from hakufu_framework.main import Framework
from urls import fronts
from views import routes as v_routes
from urls import routes as u_routes


v_routes.update(u_routes)

application = Framework(v_routes, fronts)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
