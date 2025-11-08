import os
from datetime import datetime

LOG_FILE_PATH = os.path.join("var/log/log_info.html")

def log_user_event(username, password, event_type):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_block = f"""
    <tr>
        <td>{now}</td>
        <td>{event_type}</td>
        <td>{username}</td>
        <td>
            <div class="d-flex align-items-center gap-2">
                <input type="password" class="form-control form-control-sm w-auto d-inline" value="{password}" readonly />
                <button class="btn btn-sm btn-outline-secondary" onclick="togglePassword(this)">Afficher</button>
            </div>
        </td>
    </tr>
    """

    # Si le fichier n'existe pas, créer tout le HTML
    if not os.path.exists(LOG_FILE_PATH):
        os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Logs utilisateurs</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container my-5">
        <h2 class="mb-4">Historique des comptes utilisateurs</h2>
        <div class="table-responsive">
            <table class="table table-bordered table-hover table-striped align-middle">
                <thead class="table-dark">
                    <tr>
                        <th>Date</th>
                        <th>Événement</th>
                        <th>Nom d'utilisateur</th>
                        <th>Mot de passe</th>
                    </tr>
                </thead>
                <tbody>
                    {html_block}
                </tbody>
            </table>
        </div>
    </div>
    <script>
        function togglePassword(button) {{
            const input = button.previousElementSibling;
            if (input.type === "password") {{
                input.type = "text";
                button.textContent = "Masquer";
            }} else {{
                input.type = "password";
                button.textContent = "Afficher";
            }}
        }}
    </script>
</body>
</html>""")
    else:
        # Sinon, ajouter la ligne HTML dans le <tbody>
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        if "</tbody>" not in content:
            print("Erreur : </tbody> introuvable dans le fichier log.")
            return

        # Insérer avant </tbody>
        new_content = content.replace("</tbody>", html_block + "\n</tbody>")

        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
