from django.contrib import admin
from .models import CustomUser, Article, Category, Commande, Contact, Review


admin.site.site_header = "Adminstrator Herry"
admin.site.site_title = "Herry-Shop"
admin.site.index_title = "Manageur"

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')  # Champs à afficher
    search_fields = ('username', 'email')  # Champs pour la recherche

class AdminArticle(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'created_at', 'updated_at' )

class AdminCommande(admin.ModelAdmin):
    list_display = ('items','nom','email','address', 'ville', 'pays','total', 'date_commande', )

class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'date_added' )

class AdminContact(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message')

class AdminReview(admin.ModelAdmin):
    list_display = ('user', 'article', 'text', 'created_at')

admin.site.register(Article, AdminArticle)
admin.site.register(Category, AdminCategory)
admin.site.register(Commande, AdminCommande)
admin.site.register(Contact, AdminContact)
admin.site.register(Review, AdminReview)


# ... autres enregistrements si nécessaire ...