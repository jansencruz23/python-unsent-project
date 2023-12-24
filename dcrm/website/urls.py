from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('letter/<int:pk>', views.view_letter, name='letter'),
    path('delete_letter/<int:pk>', views.delete_letter, name='delete_letter'),
    path('add_letter/', views.add_letter, name='add_letter'),
    path('update_letters/<int:pk>', views.update_letter, name='update_letter'),
    path('profile/', views.profile, name='profile'),
    path('user/<int:pk>', views.view_user, name='view_user'),
    path('about', views.about, name='about'),
    path('mailbox', views.mailbox, name='mailbox'),
    path('letter_notif/<int:pk>', views.letter_notif, name='letter_notif'),
    path('clear_notif', views.clear_notif, name='clear_notif'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)