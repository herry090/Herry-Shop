from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Assurez-vous d'importer messages
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from .models import Article, Category, Commande, Review
from .form import CustomUserForm, LocationForm, ContactForm, ProfileImageForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
import requests 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def inscription(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hachage du mot de passe
            user.save()
            auth_login(request, user)  # Connecter l'utilisateur après l'inscription
            return redirect('connexion')  # Remplacez par l'URL de redirection souhaitée
    else:
        form = CustomUserForm()

    return render(request, 'Shop/inscription.html', {'form': form})

def connexion(request):  # Votre propre fonction de connexion
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Connecter l'utilisateur
            return redirect('asur')  # Remplacez par l'URL de redirection souhaitée
        else:
            messages.error(request, "Identifiants invalides, veuillez ressayer ...")  # Message d'erreur si échec
    else:
        form = AuthenticationForm()
    return render(request, 'Shop/connexion.html', {'form': form})  # Utilisez le même template ou modifiez-le

def acceuil(request):
    list_articles = Article.objects.all()
    paginator = Paginator(list_articles, 8)  # 8 articles par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "Shop/acceuil.html", context)

def user_profile(request):
    if request.user.is_authenticated:  # Vérification si l'utilisateur est authentifié
        if request.method == 'POST':
            form = CustomUserForm(request.POST, request.FILES, instance=request.user)  # Instance de l'utilisateur
            if form.is_valid():
                form.save()
                return redirect('success_url')  # Remplacez par l'URL de redirection souhaitée
        else:
            form = CustomUserForm(instance=request.user)  # Remplir le formulaire avec les données de l'utilisateur
    else:
        return redirect('login_url')  # Rediriger si non authentifié

    return render(request, 'user_profile.html', {'form': form})

def detail(request, id_article):
    article = get_object_or_404(Article, id=id_article)  # Utilisation de get_object_or_404
    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        if review_text:
            Review.objects.create(article=article, user=request.user, text=review_text)
            return redirect('detail', id_article=id_article)  # Rediriger vers la page de détail de l'article
    category = article.category  # Accès à la catégorie de l'article
    relation = Article.objects.filter(category=category)[:5]  # Filtrage des articles par catégorie
    return render(request, 'Shop/detail.html', {"article": article, "relation": relation})

def recherche(request):
    query = request.GET.get('item-name')
    articles = Article.objects.filter(title__icontains=query) if query else Article.objects.all()
    if not articles.exists():  # Vérifiez si des articles ont été trouvés
        messages.info(request, "Aucun article trouvé pour votre recherche.")  # Message d'information
    return render(request, 'Shop/acceuil.html', {'page_obj': articles})

def checkout(request):
    if request.method == "POST":
        items = request.POST.get('items')
        total = request.POST.get('total')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        address = request.POST.get('address')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        zipcode = request.POST.get('zipcode')
        com = Commande(items=items, total=total, nom=nom, email=email, address=address, ville=ville, pays=pays, zipcode=zipcode)
        com.save()
        return redirect('confirmation')
    return render(request, 'Shop/checkout.html')

def confirmation(request):
    info = Commande.objects.all()[:1]
    for item in info:
        nom = item.nom
    return render(request, 'Shop/confirmation.html', {'name': nom})    

def asur(request):
    return render(request, 'Shop/asur.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre message a été envoyé avec succès !')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'Shop/contact.html', {'form': form})

def location_view(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            # Traitez les données du formulaire ici
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            region = form.cleaned_data['region']
            # Vous pouvez ajouter votre logique de traitement ici
            return HttpResponse(f"Pays: {country}, Ville: {city}, Région: {region}")
    else:
        form = LocationForm()
    return render(request, 'asur.html', {'form': form})

   


@login_required
def deconnexion(request):
    logout(request)  # Déconnecter l'utilisateur
    return redirect('inscription')  # Remplacez par l'URL de redirection souhaitée après déconnexion


@login_required(login_url='connexion')
def parametre(request):
    if request.method == "POST":
        # Update account info logic
        # For simplicity, assume the user model has 'email_notifications' and 'sms_notifications' fields
        user = request.user
        user.username = request.POST.get('name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Informations du compte mises à jour avec succès.')
        return redirect('parametre')
    return render(request, 'Shop/parametre.html')

@login_required
def update_notifications(request):
    if request.method == "POST":
        user = request.user
        user.email_notifications = 'email_notifications' in request.POST
        user.sms_notifications = 'sms_notifications' in request.POST
        user.save()
        messages.success(request, 'Préférences de notification mises à jour avec succès.')
        return redirect('parametre')
    return render(request, 'parametre.html')

@login_required
def update_security(request):
    if request.method == "POST":
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if user.check_password(current_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Mot de passe changé avec succès.')
                return redirect('connexion')  # Redirect to login after password change
            else:
                messages.error(request, 'Les mots de passe ne correspondent pas.')
        else:
            messages.error(request, 'Mot de passe actuel incorrect.')
    return render(request, 'parametre.html')

@login_required
def update_profile_image(request):
    if request.method == "POST":
        user = request.user
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
            user.save()
            messages.success(request, 'Image de profil mise à jour avec succès.')
        else:
            messages.error(request, 'Aucune image téléchargée.')
        return redirect('parametre')
    return render(request, 'parametre.html')

@login_required
def leave_review(request, id_article):  # Assurez-vous que le nom de l'argument correspond à l'URL
    article = get_object_or_404(Article, id=id_article)
    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        if review_text:
            Review.objects.create(article=article, user=request.user, text=review_text)
            return redirect('detail', id_article=id_article)  # Rediriger vers la page de détail de l'article
    return render(request, 'Shop/detail.html', {'article': article})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Met à jour la session pour éviter la déconnexion
            messages.success(request, 'Votre mot de passe a été changé avec succès.')  # Message de succès
            return redirect('parametre')  # Redirige vers la page des paramètres
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Shop/parametre.html', {'form': form})

@login_required
def change_profile_image(request):
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            request.user.profile_image = profile_image
            request.user.save()
            messages.success(request, 'Votre image de profil a été mise à jour avec succès.')
            return redirect('parametre')  # Redirige vers la page des paramètres
    return render(request, 'Shop/parametre.html')

@login_required
def update_account_info(request):
    if request.method == 'POST':
        old_name = request.POST.get('old_name')
        new_name = request.POST.get('new_name')
        old_email = request.POST.get('old_email')
        new_email = request.POST.get('new_email')
        
        # Vérifiez si les anciennes informations correspondent
        if request.user.username == old_name and request.user.email == old_email:
            # Mettez à jour les informations de l'utilisateur
            request.user.username = new_name
            request.user.email = new_email
            request.user.save()
            
            messages.success(request, 'Vos informations ont été mises à jour avec succès.')
            return redirect('parametre')  # Redirige vers la page des paramètres
        else:
            messages.error(request, 'Les anciennes informations ne correspondent pas.')