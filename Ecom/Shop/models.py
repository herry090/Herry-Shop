from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings 

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name="Titre")
    desc = models.TextField(verbose_name="Description")
    price = models.FloatField(verbose_name="Prix")
    image = models.ImageField(upload_to='images/', verbose_name="Image")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Catégorie", related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    def __str__(self):
        return self.title
    
class Commande(models.Model):
    items = models.CharField(max_length=300)
    total = models.CharField(max_length=200)  # Changement ici
    nom = models.CharField(max_length=150) 
    email = models.EmailField()
    address = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    pays = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=300)
    date_commande = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_commande']

    def __str__(self):
        return self.nom
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name

class Review(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Utilisez AUTH_USER_MODEL
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"