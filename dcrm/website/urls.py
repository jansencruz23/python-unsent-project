from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('letter/<int:pk>', views.view_letter, name='letter'),
    path('delete_letter/<int:pk>', views.delete_letter, name='delete_letter'),
    path('add_letter/', views.add_letter, name='add_letter'),
    path('update_letters/<int:pk>', views.update_letter, name='update_letter'),
    path('profile/', views.profile, name='profile'),
    path('user/<int:pk>', views.view_user, name='view_user'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)