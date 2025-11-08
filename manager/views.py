from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from .forms import *
import subprocess
from django.contrib.admin.views.decorators import staff_member_required
import logging
from utils import logging_utils
from django.conf import settings
import os
import random
import string
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages

# Vue du menu principal
def menu_view(request):
    return render(request, 'menu.html')

# Créer un utilisateur
def create_user_view(request):
    message = None
    error = None

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                # Créer l'utilisateur
                subprocess.run(
                    ['sudo', 'adduser', '--disabled-password', '--gecos', '', username],
                    check=True
                )
                # Définir le mot de passe
                subprocess.run(
                    ['sudo', 'chpasswd'],
                    input=f"{username}:{password}".encode(),
                    check=True
                )
                # Log
                logging_utils.log_user_event(username, password, "Création")
                message = f"L'utilisateur '{username}' a été créé avec succès."
                form = UserCreationForm()  # Réinitialise le formulaire

            except subprocess.CalledProcessError as e:
                # Affiche l'erreur complète dans la console (log)
                logging.error(f"Erreur subprocess : {e}")

                # Message plus simple pour l'utilisateur
                error = "Une erreur est survenue lors de la création de l'utilisateur. Veuillez vérifier les informations et réessayer."


    else:
        form = UserCreationForm()

    return render(request, 'create_user.html', {
        'form': form,
        'message': message,
        'error': error
    })

# Créer un groupe
def create_group_view(request):
    message = None
    error = None
    if request.method == 'POST':
        # TODO: Ajouter la logique de création de groupe
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group_name']
            try:
                # Créer le groupe
                subprocess.run(['sudo', 'addgroup', group_name], check=True)
                message= f"Groupe '{group_name}' créé avec succès."
                form = GroupCreationForm()
            except subprocess.CalledProcessError as e:
                logging.error(f"Erreur lors de la création du groupe : {e}")
                error= "Erreur lors de la création du groupe."
    else:
        form = GroupCreationForm()
    return render(request, 'create_group.html', {
        'form': form,
        'message': message,
        'error': error
    })

# Ajouter un utilisateur à un groupe
def add_user_to_group_view(request):
    message = None
    error = None
    if request.method == 'POST':
        form = AddUserToGroupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            group_name = form.cleaned_data['group_name']

            try:
                # Créer l'utilisateur
                subprocess.run(
                    ['sudo', 'usermod', '-aG', group_name, username],
                    check=True
                )
                # Message de succès
                message = f"L'utilisateur '{username}' a été ajouté au groupe '{group_name}' avec succès."
                form = AddUserToGroupForm()  # Réinitialise le formulaire

            except subprocess.CalledProcessError as e:
                # Affiche l'erreur complète dans la console (log)
                logging.error(f"Erreur subprocess : {e}")

                # Message plus simple pour l'utilisateur
                error = "Une erreur est survenue lors de l'ajout de l'utilisateur au groupe. Veuillez vérifier les informations et réessayer."


    else:
        form = AddUserToGroupForm()

    return render(request, 'add_user_to_group.html', {
        'form': form,
        'message': message,
        'error': error
    })
# Ajouter un utilisateur au groupe sudo
def add_user_to_group_sudo(request):
    message = None
    error = None
    if request.method == 'POST':
        form = AddUserToGroupSudoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            group_name = 'sudo'
            try:
                # Créer l'utilisateur
                subprocess.run(
                    ['sudo', 'usermod', '-aG', group_name, username],
                    check=True
                )
                # Message de succès
                message = f"L'utilisateur '{username}' a été ajouté au groupe '{group_name}' avec succès."
                form = AddUserToGroupSudoForm()  # Réinitialise le formulaire

            except subprocess.CalledProcessError as e:
                # Affiche l'erreur complète dans la console (log)
                logging.error(f"Erreur subprocess : {e}")

                # Message plus simple pour l'utilisateur
                error = "Une erreur est survenue lors de l'ajout de l'utilisateur au groupe. Veuillez vérifier les informations et réessayer."


    else:
        form = AddUserToGroupSudoForm()

    return render(request, 'add_user_to_group_sudo.html', {
        'form': form,
        'message': message,
        'error': error
    })

# Retirer un utilisateur d’un groupe
def remove_user_from_group_view(request):
    message = None
    error = None
    if request.method == 'POST':
        form = RemoveUserToGroupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            group_name =form.cleaned_data['group_name']
            try:
                # Créer l'utilisateur
                subprocess.run(
                    ['sudo', 'gpasswd', '-d', group_name, username],
                    check=True
                )
                # Message de succès
                message = f"L'utilisateur '{username}' a été supprimer du groupe '{group_name}' avec succès."
                form = RemoveUserToGroupForm()  # Réinitialise le formulaire

            except subprocess.CalledProcessError as e:
                # Affiche l'erreur complète dans la console (log)
                logging.error(f"Erreur subprocess : {e}")

                # Message plus simple pour l'utilisateur
                error = "Une erreur est survenue lors de la suppression de l'utilisateur du groupe. Veuillez vérifier les informations et réessayer."


    else:
        form = RemoveUserToGroupForm()

    return render(request, 'remove_user_from_group.html', {
        'form': form,
        'message': message,
        'error': error
    })

# Supprimer un groupe
def delete_group_view(request):
    message = None
    error = None
    if request.method == 'POST':
        form = DeleteGroupForm(request.POST)
        if form.is_valid():
            group_name =form.cleaned_data['group_name']
            try:
                # Supprimer le groupe
                subprocess.run(
                    ['sudo', 'groupdel', group_name],
                    check=True
                )
                # Message de succès
                message = f"Le groupe '{group_name}' a été supprimer avec succès."
                form = DeleteGroupForm()  # Réinitialise le formulaire

            except subprocess.CalledProcessError as e:
                # Affiche l'erreur complète dans la console (log)
                logging.error(f"Erreur subprocess : {e}")

                # Message plus simple pour l'utilisateur
                error = "Une erreur est survenue lors de la suppression du groupe. Veuillez vérifier les informations et réessayer."


    else:
        form = DeleteGroupForm()

    return render(request, 'delete_group.html', {
        'form': form,
        'message': message,
        'error': error
    })
# Supprimer un utilisateur
def delete_user_view(request):
    message = None
    error = None
    if request.method == 'POST':
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            username =form.cleaned_data['username']
            try:
                # Supprimer l'utilisateur
                subprocess.run(
                    ['sudo', 'userdel', username],
                    check=True
                )
                # Message de succès
                message = f"L'utilisateur '{username}' a été supprimer avec succès."
                form = DeleteUserForm()  # Réinitialise le formulaire

            except subprocess.CalledProcessError as e:
                # Affiche l'erreur complète dans la console (log)
                logging.error(f"Erreur subprocess : {e}")

                # Message plus simple pour l'utilisateur
                error = "Une erreur est survenue lors de la suppression de l'utilisateur. Veuillez vérifier les informations et réessayer."


    else:
        form = DeleteUserForm()

    return render(request, 'delete_user.html', {
        'form': form,
        'message': message,
        'error': error
    })

# Voir les groupes d’un utilisateur
def show_user_groups_view(request):
    user_groups = []
    error = None
    username = None

    if request.method == 'POST':
        form = GroupToUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                result = subprocess.run(
                    ['groups', username],
                    capture_output=True,
                    text=True,
                    check=True
                )
                # Exemple de sortie : "manoach : manoach adm dialout ..."
                output = result.stdout.strip()
                parts = output.split(':')
                if len(parts) == 2:
                    groups = parts[1].strip().split()
                    user_groups = groups
                else:
                    error = "Format de sortie inattendu pour la commande `groups`."
                form = GroupToUserForm()  # Réinitialise le formulaire

            except subprocess.CalledProcessError as e:
                logging.error(f"Erreur subprocess : {e}")
                error = "Une erreur est survenue lors de la récupération des groupes de l'utilisateur. Veuillez vérifier les informations et réessayer."

    else:
        form = GroupToUserForm()

    return render(request, 'show_user_groups.html', {
        'form': form,
        'username': username,
        'user_groups': user_groups,
        'error': error
    })

# Voir les utilisateurs dans un groupe
def show_group_users_view(request):
    group_users = []
    error = None
    group_name = None

    if request.method == 'POST':
        form = UserToGroupForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group_name']
            try:
                result = subprocess.run(
                    ['getent', 'group', group_name],
                    capture_output=True,
                    text=True,
                    check=True
                )
                # Exemple de sortie : "user1:x:1000"
                output = result.stdout.strip()
                parts = output.split(':')
                if len(parts) >= 4:
                    users = parts[3].strip().split(',')
                    group_users = users
                else:
                    error = "Format de sortie inattendu pour la commande `getent group`."
                form = UserToGroupForm()  # Réinitialise le formulaire

            except subprocess.CalledProcessError as e:
                logging.error(f"Erreur subprocess : {e}")
                error = "Une erreur est survenue lors de la récupération des utilisateurs du groupe. Veuillez vérifier les informations et réessayer."

    else:
        form = UserToGroupForm()

    return render(request, 'show_group_users.html', {
        'form': form,
        'group_name': group_name,
        'group_users': group_users,
        'error': error
    })
# Lister tous les utilisateurs et
# #Rechercher un utilisateur
def list_users_search_view(request):
    user_list = []
    error = None

    if request.method == 'POST':
        form = SearchUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            if username == '':
                # Champ vide → on affiche tous les utilisateurs
                try:
                    result = subprocess.run(
                        ['getent', 'passwd'],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    output = result.stdout.strip()
                    for line in output.split('\n'):
                        parts = line.split(':')
                        if len(parts) >= 7:
                            user_list.append({
                                'username': parts[0],
                                'uid': parts[2],
                                'gid': parts[3],
                                'home_directory': parts[5],
                                'shell': parts[6]
                            })
                except subprocess.CalledProcessError as e:
                    logging.error(f"Erreur lors de la récupération des utilisateurs : {e}")
                    error = "Erreur lors de la récupération des utilisateurs."
            else:
                # Recherche des utilisateurs dont le nom commence par la chaîne
                try:
                    result = subprocess.run(
                        ['getent', 'passwd'],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    output = result.stdout.strip()
                    found = False
                    for line in output.split('\n'):
                        parts = line.split(':')
                        if len(parts) >= 7 and parts[0].startswith(username):
                            user_list.append({
                                'username': parts[0],
                                'uid': parts[2],
                                'gid': parts[3],
                                'home_directory': parts[5],
                                'shell': parts[6]
                            })
                            found = True
                    if not found:
                        error = f"Aucun utilisateur trouvé commençant par « {username} »."
                except subprocess.CalledProcessError as e:
                    logging.error(f"Erreur lors de la récupération des utilisateurs : {e}")
                    error = f"Erreur système lors de la recherche de l'utilisateur « {username} »."

    else:
        form = SearchUserForm()
        # GET → afficher tous les utilisateurs
        try:
            result = subprocess.run(
                ['getent', 'passwd'],
                capture_output=True,
                text=True,
                check=True
            )
            output = result.stdout.strip()
            for line in output.split('\n'):
                parts = line.split(':')
                if len(parts) >= 7:
                    user_list.append({
                        'username': parts[0],
                        'uid': parts[2],
                        'gid': parts[3],
                        'home_directory': parts[5],
                        'shell': parts[6]
                    })
        except subprocess.CalledProcessError as e:
            logging.error(f"Erreur lors de la récupération des utilisateurs : {e}")
            error = "Erreur lors de la récupération des utilisateurs."

    return render(request, 'list_users.html', {
        'form': form,
        'user_list': user_list,
        'error': error
    })
# Lister tous les groupes et
# Recherche de groupe
def list_groups_view(request):
    # TODO: Ajouter la logique pour lister les groupes
    group_list = []
    error = None

    if request.method == 'POST':
        form = SearchGroupForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group_name'].strip()
            if group_name == '':
                # Champ vide → on affiche tous les groupes
                try:
                    result = subprocess.run(
                        ['getent', 'group'],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    output = result.stdout.strip()
                    for line in output.split('\n'):
                        parts = line.split(':')
                        if len(parts) >= 4:
                            group_list.append({
                                'group_name': parts[0],
                                'gid': parts[2],
                                'member': parts[3]
                            })
                except subprocess.CalledProcessError as e:
                    logging.error(f"Erreur lors de la récupération des groupes : {e}")
                    error = "Erreur lors de la récupération des groupes."
            else:
                # Recherche par nom
                try:
                    result = subprocess.run(
                        ['getent', 'group', group_name],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    output = result.stdout.strip()
                    if output:
                        parts = output.split(':')
                        if len(parts) >= 4:
                            group_list.append({
                                'group_name': parts[0],
                                'gid': parts[2],
                                'member': parts[3]
                            })
                    else:
                        error = f"Aucun groupe trouvé avec le nom « {group_name} »."
                except subprocess.CalledProcessError as e:
                    logging.error(f"Erreur lors de la recherche du Groupe : {e}")
                    error = f"Erreur système lors de la recherche du groupe « {group_name} »."
    else:
        form = SearchGroupForm()
        # GET → afficher tous les groupes
        try:
            result = subprocess.run(
                ['getent', 'group'],
                capture_output=True,
                text=True,
                check=True
            )
            output = result.stdout.strip()
            for line in output.split('\n'):
                parts = line.split(':')
                if len(parts) >= 4:
                    group_list.append({
                        'group_name': parts[0],
                        'gid': parts[2],
                        'member': parts[3]
                    })
        except subprocess.CalledProcessError as e:
            logging.error(f"Erreur lors de la récupération des groupes : {e}")
            error = "Erreur lors de la récupération des groupes."

    return render(request, 'list_groups.html', {
        'form': form,
        'group_list': group_list,
        'error': error
    })
# Voir les utilisateurs connectés
def logged_in_users_view(request):
    # TODO: Ajouter la logique pour afficher les utilisateurs connectés
    message = None
    error = None
    users = []
    if request.method == 'POST':
        form = SearchLoggedInUsersForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
    else:
        form = SearchLoggedInUsersForm()
        username = ''

    try:
        # 'who -u' ajoute la colonne PID
        result = subprocess.run(
            ['who', '-u'],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()

        for line in output.split('\n'):
            parts = line.split()
            if len(parts) >= 7:
                users.append( {
                    'username': parts[0],
                    'terminal': parts[1],
                    'login_time': f"{parts[2]} {parts[3]}",
                    'host': parts[5] if parts[5] != '(:0)' else 'localhost',
                    'pid': parts[6]
                })
            else:
                user_data = {
                    'username': parts[0],
                    'terminal': parts[1],
                    'login_time': f"{parts[2]} {parts[3]}",
                    'host': parts[4] if parts[4] != '(:0)' else 'localhost',
                    'pid': parts[5] if len(parts) > 5 else 'N/A'
                }
                if not username or username in parts[0]:
                    users.append(user_data)

        if username and not users:
            error = f"Aucun utilisateur trouvé avec le nom « {username} »."
        elif not username:
            message = "Liste des utilisateurs connectés récupérée avec succès."

    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur lors de la récupération des utilisateurs connectés : {e}")
        error = "Erreur lors de la récupération des utilisateurs connectés."

    return render(request, 'logged_in_users.html', {
        'form': form,
        'users': users,
        'message': message,
        'error': error
    })

#Afficher l'historique des informations
def hystori_info(request):
    
    return render(request,'hystori_info.html')

# Changer le mot de passe
# Mettre à jour le mot de passe
def passwd_forget(request):
    message = None
    error = None

    if request.method == 'POST':
        form = PasswordForgetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']

            try:
                # Mettre à jour le mot de passe
                subprocess.run(
                    ['sudo', 'chpasswd'],
                    input=f"{username}:{new_password}".encode(),
                    check=True
                )
                logging_utils.log_user_event(username, new_password, "Changement de mot de passe")
                message = f"Le mot de passe de l'utilisateur '{username}' a été mis à jour avec succès."
                form = PasswordForgetForm()  # Réinitialise le formulaire

            except subprocess.CalledProcessError as e:
                logging.error(f"Erreur subprocess : {e}")
                error = "Une erreur est survenue lors de la mise à jour du mot de passe. Veuillez vérifier les informations et réessayer."

    else:
        form = PasswordForgetForm()

    return render(request, 'passwd_forget.html', {
        'form': form,
        'message': message,
        'error': error
    })
# Changer le mot de passe de l'utilisateur
def change_passwd(request):
    message = None
    error = None

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            new_password = form.cleaned_data['new_password']

            try:
                # Appelle la commande `passwd` en utilisant subprocess
                process = subprocess.run(
                    ['sudo', 'passwd', username],
                    input=f'{new_password}\n{new_password}\n',
                    capture_output=True,
                    text=True
                )
                if process.returncode == 0:
                    # Log
                    logging_utils.log_user_event(username, new_password, "Changement de mot de passe")
                    message = f"Mot de passe de l’utilisateur « {username} » modifié avec succès."
                else:
                    logging.error(f"Erreur passwd: {process.stderr}")
                    error = f"Erreur : {process.stderr.strip()}"
            except Exception as e:
                logging.error(f"Erreur lors de la modification du mot de passe : {e}")
                error = "Erreur lors de la modification du mot de passe."
    else:
        form = ChangePasswordForm()

    return render(request, 'change_passwd.html', {
        'form': form,
        'message': message,
        'error': error
    })
# Demander l'accès aux logs
def request_log_access(request):
    if request.method == "POST":
        form = LogInfoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]

            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            # Enregistrement dans la session
            request.session["log_access_email"] = email
            request.session["log_access_code"] = code
            request.session["log_access_time"] = datetime.now().isoformat()  # ⏰ ici

            send_mail(
                "Code d'accès aux logs",
                f"Voici votre code d'accès : {code}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return redirect("verify_log_code")
    else:
        form = LogInfoForm()

    return render(request, "request_log_access.html", {"form": form})

# Vérifier le code d'accès aux logs
from datetime import datetime, timedelta

def verify_log_code(request):
    if request.method == "POST":
        form = LogCodeForm(request.POST)
        if form.is_valid():
            code_entered = form.cleaned_data["code"]
            expected_code = request.session.get("log_access_code")
            code_time_str = request.session.get("log_access_time")

            # Vérifie l'expiration
            if code_time_str:
                code_time = datetime.fromisoformat(code_time_str)
                if datetime.now() > code_time + timedelta(minutes=5):
                    return render(request, "verify_log_code.html", {
                        "form": form,
                        "error": "Code expiré. Veuillez redemander un nouveau code."
                    })

            if code_entered == expected_code:
                request.session["log_access_granted"] = True
                return redirect("view_logs_html")
            else:
                return render(request, "verify_log_code.html", {
                    "form": form,
                    "error": "Code incorrect"
                })
    else:
        form = LogCodeForm()

    return render(request, "verify_log_code.html", {"form": form})

#Réinitialiser le code d'accès aux logs

def resend_log_code(request):
    email = request.session.get("log_access_email")

    if not email:
        messages.error(request, "Adresse email non disponible. Veuillez recommencer.")
        return redirect("request_log_access")

    # Nouveau code
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # Stockage session
    request.session["log_access_code"] = code
    request.session["log_access_time"] = datetime.now().isoformat()

    # Envoi email
    send_mail(
        "Nouveau code d'accès aux logs",
        f"Voici votre nouveau code d'accès : {code}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    messages.success(request, "Un nouveau code a été envoyé à votre adresse email.")
    return redirect("verify_log_code")


# Afficher les logs HTML
#@staff_member_required
def view_logs_html(request):
    log_path = os.path.join(settings.BASE_DIR, "var/log/log_info.html")

    if not os.path.exists(log_path):
        return render(request, "log_wrapper.html", {
            "log_html": "<p class='text-danger'>Aucun log trouvé.</p>"
        })

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    return render(request, "log_wrapper.html", {
        "log_html": content
    })


def test_404(request):
    return HttpResponseNotFound(render(request, '404.html'))
