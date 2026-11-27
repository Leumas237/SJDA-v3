# BC Connect 💚 — Plateforme de rencontres IUT-FV Bandjoun

Une PWA (application web installable sur téléphone) pour connecter les étudiants de l'Institut Universitaire de Technologie Fotso Victor (IUT-FV) de Bandjoun, Cameroun. Amitié, amour, ou les deux — si affinités !

## Fonctionnalités

- 🌿 **Découverte façon swipe** : glisse à droite pour liker, à gauche pour passer, ↺ pour annuler ton dernier swipe. Jusqu'à **6 photos par profil**, avec carrousel sur la carte (tap gauche/droite pour changer de photo)
- ⚙️ **Filtres de découverte** : par âge (min/max) et par filière/classe
- 💚 **Match** quand deux personnes se likent mutuellement
- 💛 **Économie des likes** : quota quotidien (15 par défaut, `BC_DAILY_LIKES`) ; s'acharner au-delà du quota accumule des strikes et finit en **suspension automatique pour spam** (`BC_SPAM_STRIKES_BAN`, 30 par défaut), avec alerte aux modos
- 👀 **« Qui m'a liké » anonyme** : un compteur, jamais les noms
- 🕶️ **Mode invisible (AFK)** : tu disparais de la découverte et le swipe est bloqué tant qu'il est actif ; tes matchs existants restent
- 🟢 **Badge « actif récemment »** sur les cartes (activité < 3 jours)
- 🗑️ **Suppression de compte en libre-service** : mot de passe exigé, tout est effacé immédiatement (profil, photos, dossier KYI, matchs, abonnements push)
- 🔔 **Notifications push** : nouveau match, demande d'inscription et signalement (admins), inscription acceptée — clés VAPID générées automatiquement au premier lancement, rien à configurer
- 🔓 **Réseaux débloqués par le match** : chacun renseigne son Instagram, Snapchat et WhatsApp dans son profil ; ils restent secrets et ne sont révélés qu'à tes matchs, avec des liens directs. Pas de messagerie interne à surveiller — la conversation continue là où les étudiants discutent déjà
- 🤝 **Mode amitié / couple** : chacun choisit ce qu'il cherche, l'app ne propose que des profils compatibles
- ✋ **Inscriptions validées à la main** : chaque demande d'inscription doit être acceptée par un admin avant que l'étudiant accède à l'app
- 🪪 **KYI (vérification d'identité)** : juste après l'inscription et avant toute personnalisation du compte, l'étudiant soumet un dossier obligatoire — nom et prénom officiels, date de naissance, filière/classe, photo de la carte étudiante IUT-FV. Les modos valident sur dossier ; la carte est stockée hors du dossier public (`data/kyi/`), servie uniquement aux modos via un endpoint authentifié, et supprimée si la demande est refusée
- 🏫 **Inscription libre** : tout email valide est accepté. Le contrôle d'appartenance à l'IUT-FV se fait via le KYI obligatoire. Le champ « Code modérateur (optionnel) » permet de devenir modo validé d'office
- 🎨 **Charte graphique IUT-FV** : vert principal #007A3D, vert profond #004D2A, or #F5B800, bleu institutionnel #004A99
- 📱 **PWA** : installable sur l'écran d'accueil, fonctionne sur tous les téléphones
- 🛡️ **Modération en temps réel** : tableau de bord admin avec statistiques, fil d'activité en direct, demandes d'inscription, signalements et bannissement

## Lancer en local

```bash
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:password@localhost:5432/bc_connect
export BC_ADMIN_EMAILS=ton@email.com
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Sous PowerShell :
```powershell
$env:DATABASE_URL = "postgresql://user:password@localhost:5432/bc_connect"
$env:BC_ADMIN_EMAILS = "ton@email.com"
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Puis ouvre http://localhost:8000 — sur téléphone, utilise l'IP de ton PC (ex. `http://192.168.1.10:8000`) en étant sur le même Wi-Fi.

> ⚠️ L'installation PWA et le WebSocket sécurisé nécessitent du HTTPS en production (Render, Railway, Fly.io… le fournissent automatiquement).

## Mise en ligne

Un `Dockerfile` est fourni — l'app tourne partout où Docker tourne.
Démarrage sans Docker : `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.

**Render / Railway (le plus simple)** :
1. Connecte ce repo GitHub, choisis « Web Service » (Render détecte le Dockerfile)
2. Configure les variables d'environnement : `BC_ADMIN_EMAILS` (ton email) et éventuellement `BC_MOD_CODE` (code modérateur secret)
3. Configure `DATABASE_URL` avec l'URL de ta base PostgreSQL managée.
4. ⚠️ **Important — persistance** : les photos, cartes KYI et clés VAPID vivent dans `./data`. Sur les offres gratuites, le disque est effacé à chaque redéploiement. Ajoute un **disque persistant** (Render : "Disk", Railway : "Volume", Fly : "Volume") monté sur `/app/data`, ou définis `BC_DATA_DIR` vers le point de montage.
5. Ouvre l'URL en HTTPS sur ton téléphone → « Ajouter à l'écran d'accueil » pour l'installer comme une vraie app.

## Configuration (variables d'environnement)

| Variable | Défaut | Rôle |
|---|---|---|
| `BC_APP_NAME` | `BC Connect` | Nom affiché de l'app |
| `BC_SUPPORT_EMAIL` | `sjda.beta@protonmail.com` | Adresse de support affichée dans l'application |
| `BC_EMAIL_DOMAINS` | *(vide)* | Domaines email autorisés (vide = inscription libre). La validation se fait via KYI. |
| `BC_MOD_CODE` | *(vide)* | Code modérateur secret : fourni à l'inscription, il rend le compte modo (et permet de s'inscrire sans email étudiant). Vide = désactivé |
| `BC_ADMIN_EMAILS` | *(vide)* | Emails toujours admins (promus à la connexion si besoin) |
| `BC_DAILY_LIKES` | `15` | Quota de likes par jour et par personne |
| `BC_SPAM_STRIKES_BAN` | `30` | Tentatives au-delà du quota avant suspension automatique |
| `DATABASE_URL` | *(requis)* | URL de connexion PostgreSQL |
| `BC_DATA_DIR` | `./data` | Dossier des photos, cartes KYI et clés VAPID |

L'inscription est libre (tout email valide accepté). Les admins peuvent aussi promouvoir/rétrograder un modo depuis la liste des étudiants du tableau de bord.

## Architecture

```
backend/          API FastAPI + PostgreSQL
  main.py         Routes : auth, profils, découverte, swipe, matchs, chat, WebSocket
  auth.py         Mots de passe PBKDF2 + sessions par jeton
  db.py           Schéma PostgreSQL + get_db()
  config.py       Configuration
  push.py         Notifications Web Push (VAPID) ; génère et stocke les clés tout seul au premier démarrage
frontend/         PWA en HTML/CSS/JS vanilla (aucun build nécessaire)
  index.html      Toutes les vues (auth, swipe, matchs, chat, profil)
  app.js          Logique SPA + swipe tactile + WebSocket
  sw.js           Service worker (cache hors-ligne de la coquille)
  manifest.json   Manifeste PWA
  style.css       Tout le style ; les couleurs sont des variables CSS dans :root
  icons/          Icônes PNG 192 et 512 + logo SVG
data/             ← créé automatiquement au premier lancement (gitignoré)
  bc_connect.db   base PostgreSQL (en local SQLite possible via config)
  uploads/        photos de profil (servies publiquement sur /uploads)
  kyi/            cartes étudiantes (JAMAIS servies publiquement)
  vapid_private.pem clés de push (à sauvegarder ! si tu les perds, tous les abonnements push existants deviennent invalides)
```

## Modération

Déclare les comptes modérateurs avec `BC_ADMIN_EMAILS` (l'onglet 🛡️ Administration apparaît pour eux). Le tableau de bord montre :

- les **demandes d'inscription** avec le dossier KYI complet (identité, date de naissance, filière, carte étudiante consultable) : tout nouveau compte est en attente jusqu'à ce qu'un admin l'accepte. Une fois son KYI soumis, l'étudiant peut préparer son profil en attendant ; sa page se débloque automatiquement à l'acceptation. Refuser supprime le compte et son dossier
- les **statistiques** (étudiants validés, actifs 7j, demandes KYI, matchs, signalements, bannis)
- un **fil d'activité en direct** (demandes, inscriptions, matchs, signalements — poussé par WebSocket, sans recharger la page)
- les **signalements** : chaque étudiant peut signaler un match via le bouton ⚠️ de la fiche ; le match est supprimé immédiatement et les deux ne se recroisent plus. L'admin voit le motif, puis bannit ou classe sans suite
- la **liste des étudiants** avec bannissement/rétablissement en un clic (le bannissement coupe les sessions et bloque la connexion)
- la **promotion/rétrogradation** des modérateurs

Respect de la vie privée : il n'y a **pas de messagerie interne**, donc rien à surveiller — et les réseaux sociaux d'un profil ne sont jamais visibles avant un match mutuel.

## Sécurité & vie privée

- Mots de passe hachés (PBKDF2, 200 000 itérations), jamais stockés en clair
- Les réseaux sociaux (Insta/Snap/WhatsApp) ne sont exposés qu'aux matchs
- Les photos sont limitées à 5 Mo (JPEG/PNG/WebP)
- La politique de confidentialité est accessible sur `/privacy`, avec consentement obligatoire à l'inscription, export des données depuis le profil et suppression définitive du compte.
- **Protection des mineurs** : la recherche de relation amoureuse (intent "couple") est réservée aux personnes majeures (18 ans et plus)
- **Cartes étudiantes** : stockées dans `data/kyi/`, jamais servies en statique, accessibles uniquement aux admins via endpoint authentifié, supprimées lors du refus d'inscription ou suppression de compte

## Recette de test manuel (avant chaque mise en prod)

En local avec des quotas réduits pour aller vite :
```bash
BC_ADMIN_EMAILS=admin@x.com BC_DAILY_LIKES=2 BC_SPAM_STRIKES_BAN=3 uvicorn backend.main:app --port 8000
```

- □ Inscription email quelconque → acceptée, écran KYI, profil bloqué (PUT → 403)
- □ Soumission KYI → écran d'attente, profil débloqué
- □ Admin : demande visible avec dossier + carte consultable
- □ Accepter → l'écran de l'étudiant se débloque seul (≤ 5 s)
- □ Refuser → compte supprimé, carte effacée de data/kyi/
- □ Swipe mutuel → « C'est un Match ! » → réseaux visibles des 2 côtés
- □ 3e like du jour → 429 ; insister 3 fois → suspension auto + fil admin
- □ Mode invisible → absent du deck des autres, swipe bloqué
- □ Signalement depuis la fiche match → match fermé, alerte admin
- □ Suppression de compte → login impossible, fichiers effacés
- □ Mineur (< 18 ans) tente intent "couple" → refusé
- □ Sur téléphone (HTTPS) : installation PWA + réception d'un push

## Idées pour la suite

1. **RECYCLAGE DES « PASSÉS »** : dans un campus, le deck s'épuise vite. Fais expirer les swipes `liked=0` après ~3 semaines (un DELETE périodique ou un filtre sur `created_at` dans discover). ATTENTION : ne recycle jamais les paires issues d'un signalement (elles ont un swipe `liked=0` dans les DEUX sens — c'est le marqueur de blocage ; exclue les paires mutuelles du recyclage).
2. Filtre par centres d'intérêt.
3. Statistiques d'usage pour l'admin (matchs/jour, rétention).
4. PostgreSQL + stockage objet si > ~1000 utilisateurs actifs.

Bon code, et prends soin de cette app — elle va créer des amitiés (et peut-être plus) bien réelles. 💚💛

— L'équipe de développement BC Connect