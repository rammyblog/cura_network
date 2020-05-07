
from django.urls import path, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.schemas import get_schema_view as get_core_api_schema
from api import views

API_TITLE = 'Cura Network API'
API_DESCRIPTION = 'A Web API for getting hotels in a region and booking hotels'

schema_view = get_schema_view(
    openapi.Info(
        title=API_TITLE,
        default_version='v1',
        description=API_DESCRIPTION,

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.API_Root.as_view(), name='API Root'),
    path('api/', include('api.urls')),
    path('schema/', get_core_api_schema),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='api_docs')
]
