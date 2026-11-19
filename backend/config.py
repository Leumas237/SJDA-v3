"""Configuration de l'application, surchargeable par variables d'environnement."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("BC_DATA_DIR", os.environ.get("SJDA_DATA_DIR", BASE_DIR / "data")))
UPLOADS_DIR = DATA_DIR / "uploads"
# cartes d'étudiant du KYI : jamais servies publiquement, accès modos uniquement
KYI_DIR = DATA_DIR / "kyi"
DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("BC_DATABASE_URL", os.environ.get("SJDA_DATABASE_URL", ""))

APP_NAME = os.environ.get("BC_APP_NAME", os.environ.get("SJDA_APP_NAME", "BC Connect"))
SUPPORT_EMAIL = os.environ.get("BC_SUPPORT_EMAIL", os.environ.get("SJDA_SUPPORT_EMAIL", "support@bc-connect.app"))

# Vérification établissement : l'inscription est LIBRE (sans restriction de domaine).
# Le contrôle d'appartenance à l'IUT-FV se fait via le KYI obligatoire (carte étudiante).
# BC_EMAIL_DOMAINS n'est plus utilisé pour l'inscription, mais conservé pour compatibilité.
EMAIL_DOMAINS = {
    d.strip().lower().lstrip("@")
    for d in os.environ.get(
        "BC_EMAIL_DOMAINS",
        os.environ.get("SJDA_EMAIL_DOMAINS", ""),
    ).split(",")
    if d.strip()
}

# Code modérateur (BC_MOD_CODE) : optionnel à l'inscription. Quelqu'un qui
# fournit le bon code devient modérateur (et peut s'inscrire avec n'importe
# quel email). Vide par défaut = personne ne devient modo par code.
MOD_CODE = os.environ.get("BC_MOD_CODE", os.environ.get("SJDA_MOD_CODE", "")).strip()

# Emails administrateurs (séparés par des virgules) : ces comptes voient
# le tableau de bord de modération. Ex. BC_ADMIN_EMAILS="toi@email.com"
ADMIN_EMAILS = {
    e.strip().lower()
    for e in os.environ.get("BC_ADMIN_EMAILS", os.environ.get("SJDA_ADMIN_EMAILS", "")).split(",")
    if e.strip()
}

# Économie des likes : quota quotidien, et suspension automatique pour spam
# après trop de tentatives au-delà du quota (chaque tentative rejetée compte).
DAILY_LIKES = int(os.environ.get("BC_DAILY_LIKES", os.environ.get("SJDA_DAILY_LIKES", "15")))
SPAM_STRIKES_BAN = int(os.environ.get("BC_SPAM_STRIKES_BAN", os.environ.get("SJDA_SPAM_STRIKES_BAN", "30")))

MAX_PHOTO_BYTES = 5 * 1024 * 1024  # 5 Mo
SESSION_DAYS = 30

DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
KYI_DIR.mkdir(parents=True, exist_ok=True)
