from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 
from .import views

urlpatterns = [
    path('', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('acceuil/', views.acceuil, name='acceuil'),
    path('recherche/', views.recherche, name='recherche'),
    path('asur/contact/', views.contact, name='contact'), 
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('checkout/', views.checkout, name="checkout"),
    path('asur/', views.asur, name="asur"),
    path('asur/', views.location_view, name='location'),
    path('confirmation/', views.confirmation, name="confirmation"),
    path('article/<int:id_article>', views.detail, name="detail"),
    path('asur/parametre/', views.parametre, name='parametre'),
    path('update_notifications/', views.update_notifications, name='update_notifications'),
    path('update_security/', views.update_security, name='update_security'), 
    path('article/<int:id>/leave_review/', views.leave_review, name='leave_review'), 
    path('change_password/', views.change_password, name='change_password'), 
    path('change_profile_image/', views.change_profile_image, name='change_profile_image'),
    path('update_account_info/', views.update_account_info, name='update_account_info'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
