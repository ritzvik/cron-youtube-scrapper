"""code_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.http import JsonResponse
from code_service.logger.logging import setup_logger
from code_service.swagger import swagger_schema_view

# Create your views here.

logger = setup_logger(__name__)


def HealthCheck(request):
    return JsonResponse(
        {"version": "1.2.3", "message": "Code Service Working"}, status=200
    )


urlpatterns = [
    url(r"admin/", admin.site.urls),
    url(r"v1/scrapper/", include("scrapper.urls")),
    url(r"api-docs/", swagger_schema_view.with_ui("swagger", cache_timeout=0)),
    url(r"health-check", HealthCheck, name="Health Check"),
]
