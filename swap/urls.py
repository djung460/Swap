from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from swap import handlers
from swap import views

urlpatterns = [
    # view stuff displays pages
    url(r'^$',views.index),
    url(r'^login$',views.login),
    url(r'^join$',views.join),
    #url(r'^(?P<user>[0-9a-zA-Z]+)',views.user),

    # api stuff gets passed off to the handler
    url(r'^api/auth/login$', handlers.user),
    url(r'^api/auth/join$',handlers.user),

    url(r'^api/equipment/add$', handlers.equipment),
    url(r'^api/equipment/delete$', handlers.equipment),
    url(r'^api/equipment/get$', handlers.equipment),
    
    url(r'^api/trades/add$', handlers.trade),
    url(r'^api/trades/delete$', handlers.trade),
    url(r'^api/trades/get$', handlers.trade),
    
    url(r'^api/course/add$', handlers.course),
    url(r'^api/course/delete$', handlers.course),
    url(r'^api/course/get$', handlers.course),
    
    url(r'^api/instructor/add$', handlers.instructor),
    url(r'^api/instructor/delete$', handlers.instructor),
    url(r'^api/instructor/get$', handlers.instructor),	
]

urlpatters = format_suffix_patterns(urlpatterns)

