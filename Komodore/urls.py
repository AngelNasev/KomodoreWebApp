"""
URL configuration for Komodore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from KomodoreApp.views import buyer_registration, seller_registration, home, login_view, car_search, part_search, \
    get_models, get_years, item_list, add, seller_parts, part_details

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buyer/register/', buyer_registration, name='buyer_register'),
    path('seller/register/', seller_registration, name='seller_register'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('get_models/', get_models, name='get_models'),
    path('get_years/', get_years, name='get_years'),
    path('search/car', car_search, name='car_search'),
    path('search/part', part_search, name='part_search'),
    path('search/part/<int:car_id>', part_search, name='part_search_with_car'),
    path('item_list/<str:category>/<int:car_id>/', item_list, name='item_list'),
    path('item_list/<str:category>/', item_list, name='item_list_without_car'),
    path('add/', add, name='add'),
    path('seller/parts', seller_parts, name='seller_parts'),
    path('details/<int:id>/', part_details, name='part_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
