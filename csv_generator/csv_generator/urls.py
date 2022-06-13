"""csv_generator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from re import template
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from schemas.views import DataSetListView, SchemaListView, SchemaCreateView, SchemaEditView, SchemaDeleteView, dataset_generate
from users.forms import LoginForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
           template_name='users/login.html',
           redirect_authenticated_user=True,
           authentication_form=LoginForm),
        name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', SchemaListView.as_view(
            template_name='schemas/home.html'), 
        name='home'),
    path('schema/create/', SchemaCreateView.as_view(
            template_name='schemas/schema.html'),
        name='schema-create'),
    path('schema/<int:pk>/edit/', SchemaEditView.as_view(
            template_name='schemas/schema.html'),
        name='schema-edit'),
    path('schema/<int:pk>/delete/', SchemaDeleteView.as_view(), name='schema-delete'),
    path('schema/<int:pk>/datasets/', DataSetListView.as_view(
            template_name='schemas/datasets.html'), 
        name='schema-datasets'),
    path('dataset/generate/', dataset_generate, name='dataset-generate')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
