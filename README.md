# Gestion Commerciale

Une application web de gestion commerciale en Python/Flask pour PME avec facturation en ariary, gestion stock et rapports de ventes.

## Fonctionnalités

- **Tableau de bord** avec statistiques en temps réel
- **Gestion des produits** avec alertes de stock faible
- **Gestion des clients** avec informations de contact
- **Création de ventes** avec génération automatique de factures
- **Facturation PDF** avec mise en forme professionnelle
- **Rapports et statistiques** avec graphiques interactifs
- **Devise Ariary (MGA)** pour les entreprises malgaches

## Technologies utilisées

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: Bootstrap 5, JavaScript, Chart.js
- **PDF**: ReportLab
- **Déploiement**: Render, Gunicorn

## Structure du projet

```
gestion-commerciale/
│
├── app/
│   ├── __init__.py           # Configuration de l'application Flask
│   ├── models.py             # Modèles de base de données
│   ├── utils.py              # Utilitaires (PDF, formatage)
│   ├── main.py               # Point d'entrée de l'application
│   └── routes/
│       ├── __init__.py       # Enregistrement des blueprints
│       ├── base.py           # Routes principales (accueil, factures, rapports)
│       ├── produits.py       # Gestion des produits
│       ├── clients.py        # Gestion des clients
│       └── ventes.py         # Gestion des ventes
│
├── templates/                # Templates Jinja2
├── static/                   # CSS, JavaScript, images
├── Procfile                  # Configuration Render
└── README.md
```

## Installation et déploiement

### Déploiement sur Render

1. **Fork ou clonez** ce repository sur GitHub

2. **Créez une nouvelle Web Service** sur [Render](https://render.com):
   - Connectez votre repository GitHub
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app.main:app --bind 0.0.0.0:$PORT`

3. **Configurez la base de données PostgreSQL**:
   - Créez une PostgreSQL database sur Render
   - Ajoutez la variable d'environnement `DATABASE_URL`

4. **Variables d'environnement optionnelles**:
   - `SESSION_SECRET`: Clé secrète pour les sessions (générée automatiquement si non définie)

### Installation locale

```bash
# Cloner le repository
git clone <your-repo-url>
cd gestion-commerciale

# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données
export DATABASE_URL="postgresql://user:password@localhost:5432/gestion_commerciale"

# Lancer l'application
python -m app.main
```

## Utilisation

1. **Accédez à l'application** via l'URL fournie par Render
2. **Ajoutez vos premiers produits** dans la section Produits
3. **Créez vos clients** dans la section Clients
4. **Enregistrez des ventes** qui génèrent automatiquement des factures
5. **Consultez les rapports** pour analyser votre activité

## Sécurité

- Protection CSRF intégrée
- Validation des données côté serveur
- Gestion sécurisée des sessions
- Support HTTPS via Render

## Support

Cette application est conçue pour les petites et moyennes entreprises malgaches nécessitant un système de gestion commerciale simple et efficace.

## Licence

Open Source - Libre d'utilisation et de modification.