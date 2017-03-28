from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from swapapp.handlers import handlers, studenthandlers, instructorhandlers
from swapapp import views
from swapapp.auth import auth

urlpatterns = [
    # view stuff displays pages
    url(r'^$',views.index),
    url(r'^login$',views.login),
    url(r'^join$',views.join),
    url(r'^search$', views.search),
    url(r'^search/(?P<user>[0-9a-zA-Z]+)$', views.search),
    url(r'^student/(?P<user>[0-9a-zA-Z]+)$',views.student),
    url(r'^addequipment$', views.addStudentEquipment),
    url(r'^enroll$',views.enroll),
    url(r'^instructor/(?P<user>[0-9a-zA-Z]+)$',views.instructor),
    url(r'^addclass$',views.addclass),
    url(r'^addequipment/class/(?P<classid>[0-9a-zA-Z]+)$', views.instructor_addequip),

    # api stuff gets passed off to the handler
    url(r'^api/student/equipment/add', studenthandlers.addequipment),
    url(r'^api/student/equipment/delete', studenthandlers.deleteequipment),
    url(r'^api/student/equipment/update', studenthandlers.updateequipment),
    url(r'^api/student/class/enroll', studenthandlers.enroll),
    url(r'^api/student/class/drop', studenthandlers.drop),


    url(r'^api/instructor/class/add', instructorhandlers.addclass),
    url(r'^api/instructor/equipment/add', instructorhandlers.addequipment),

    url(r'^api/auth/login$', auth.login),
    url(r'^api/auth/join$', auth.join),
    url(r'^api/auth/logout', auth.logout),

    url(r'^api/equipment/add$', handlers.equipment),
    url(r'^api/equipment/delete$', handlers.equipment),
    url(r'^api/equipment/get$', handlers.equipment),
    url(r'^api/equipment/search', handlers.searchequipment),
	
	url(r'^api/trades/findtrades$', handlers.findtrade),
    url(r'^api/trades/add$', handlers.trade),
    url(r'^api/trades/delete$', handlers.trade),
    url(r'^api/trades/get$', handlers.trade),

    url(r'^api/course/add$', handlers.course),
    url(r'^api/course/delete$', handlers.course),
    url(r'^api/course/get$', handlers.course),

    url(r'^api/instructor/add$', handlers.instructor),
    url(r'^api/instructor/delete$', handlers.instructor),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

