from datetime import date
from views import Index, Contacts, PTests, Adm_Panel, CoursesList, CreateCourse, CreateCategory, CategoryList, \
    CopyCourse


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
#     '/': Index(),
#     '/about/': About(),
    '/contacts/': Contacts(),
    '/tests/': PTests(),
    # '/admpanel/': Adm_Panel(),
#     '/courses-list/': CoursesList(),
#     '/create-course/': CreateCourse(),
#     '/create-category/': CreateCategory(),
#     '/category-list/': CategoryList(),
#     '/copy-course/': CopyCourse()
}
