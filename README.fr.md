# GoToProjects

Un outil en ligne de commande pour naviguer rapidement vers vos projets de développement et exécuter automatiquement des commandes prédéfinies.

- [Doc anglaise](README.md)

## Sommaire

- [Fonctionnalités](#fonctionnalites)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
  - [Option 1 : Installation automatique (recommandée)](#option-1-installation-automatique-recommandee)
  - [Option 2 : Installation manuelle (usage local)](#option-2-installation-manuelle-usage-local)
- [Configuration](#configuration)
  - [Créer votre fichier de configuration](#creer-votre-fichier-de-configuration)
  - [Options de configuration](#options-de-configuration)
- [Utilisation](#utilisation)
  - [Après installation (recommandé)](#apres-installation-recommande)
  - [Utilisation locale (sans installation)](#utilisation-locale-sans-installation)
  - [Exemples](#exemples)
- [Dépannage](#depannage)
  - [Le changement de répertoire ne persiste pas](#le-changement-de-repertoire-ne-persiste-pas)
  - [Projet non trouvé](#projet-non-trouve)
  - [Erreurs de chemin](#erreurs-de-chemin)
  - [Script temporaire non généré](#script-temporaire-non-genere)
- [Désinstallation](#desinstallation)
- [Informations techniques](#informations-techniques)
  - [Architecture](#architecture)
  - [Fichiers temporaires](#fichiers-temporaires)
- [Historique des versions](#historique-des-versions)
- [License](#license)

## Fonctionnalités

- 🚀 Navigation rapide vers vos projets
- 📂 Changement de répertoire persistant dans le shell
- 🔄 Pull automatique des dernières modifications Git
- 💻 Exécution automatique de commandes personnalisées
- 🖥️ Ouverture automatique dans VS Code
- ⚙️ Configuration flexible via JSON

## Structure du projet

```
GoToProjects/
├── go_to_project.py     # Script Python principal
├── gtp                  # Script shell wrapper
├── install.sh           # Script d'installation
├── config.json          # Configuration des projets
├── config_example.json  # Exemple de configuration
├── requirements.txt     # Dépendances Python
└── README.md            # Ce fichier
```

## Installation

### Option 1: Installation automatique (Recommandée)

1. Clonez ou téléchargez ce dépôt

```bash
git clone https://github.com/VivicatcHub/GoToProjects.git
cd GoToProjects
```

2. Exécutez le script d'installation (nécessite sudo) :

```bash
sudo ./install.sh
```

3. Le script va :
   - Vérifier que tous les fichiers nécessaires existent
   - Créer un script `gtp` avec les chemins absolus intégrés
   - L'installer dans `/usr/bin/gtp`
   - Rendre le binaire accessible depuis n'importe où

### Option 2: Installation manuelle (usage local)

Si vous préférez utiliser l'outil sans installation système :

```bash
# Depuis le répertoire GoToProjects
source ./gtp <project_name>
```

Cette méthode ne nécessite pas de privilèges root mais fonctionne seulement depuis le répertoire du projet.

## Configuration

### Créer votre fichier de configuration

1. Copiez le fichier d'exemple :

```bash
cp config_example.json config.json
```

2. Éditez `config.json` selon vos projets :

```json
{
  "mon-projet": {
    "path": "/home/user/Projets/mon-projet/",
    "vscode": true,
    "pull": true,
    "commands": ["npm install", "npm run dev"]
  },
  "autre-projet": {
    "path": "/home/user/Travail/autre-projet/",
    "vscode": false,
    "pull": false,
    "commands": ["docker-compose up -d", "echo 'Projet démarré!'"]
  }
}
```

### Options de configuration

Pour chaque projet, vous pouvez définir :

- **`path`** (obligatoire) : Chemin absolu vers le répertoire du projet
- **`vscode`** (optionnel) : `true` pour ouvrir automatiquement VS Code
- **`pull`** (optionnel) : `true` pour exécuter `git pull` automatiquement
- **`commands`** (optionnel) : Liste des commandes à exécuter dans l'ordre

## Utilisation

### Après installation (recommandé)

Utilisez simplement la commande `gtp` depuis n'importe où :

```bash
gtp <nom-du-projet>
```

### Utilisation locale (sans installation)

Depuis le répertoire GoToProjects :

```bash
source ./gtp <nom-du-projet>
```

### Exemples

```bash
# Aller au projet "wow"
gtp wow

# Le script va :
# 1. Naviguer vers /incroyable/wow/
# 2. Exécuter git pull
# 3. Exécuter toutes les commandes définies
# 4. Ouvrir VS Code si configuré
```

## Dépannage

### Le changement de répertoire ne persiste pas

**Problème** : Après avoir exécuté `gtp`, vous êtes toujours dans le répertoire d'origine.

**Solutions** :

- ✅ Utilisez `gtp <project>` après installation système
- ✅ Utilisez `source ./gtp <project>` pour usage local
- ❌ N'utilisez jamais `./gtp <project>` (s'exécute dans un sous-shell)

### Projet non trouvé

Le script suggère des projets similaires basés sur la première lettre :

```bash
$ gtp zf
❓ Project 'ma' not found.
📋 Available projects: marin-kitagawa
```

### Erreurs de chemin

Vérifiez que :

- Le chemin dans `config.json` est correct
- Vous avez les permissions pour accéder au répertoire
- Le répertoire existe

### Script temporaire non généré

**Problème** : Message "❌ No script generated for project 'X'"

**Causes possibles** :

- Le projet n'existe pas dans `config.json`
- Erreur dans le script Python
- Permissions insuffisantes pour écrire dans `/tmp/`

**Solution** : Vérifiez que le projet existe et que le fichier `config.json` est valide.

## Désinstallation

Pour supprimer `gtp` du système :

```bash
sudo rm /usr/bin/gtp
```

## Informations techniques

### Architecture

1. **`go_to_project.py`** : Script Python principal qui :

   - Lit la configuration JSON
   - Génère un script shell temporaire avec les commandes
   - Place le script dans `/tmp/gtp_<project_name>.sh`

2. **`gtp`** : Script shell wrapper qui :

   - Appelle le script Python
   - Source le script temporaire généré
   - Nettoie le fichier temporaire

3. **`install.sh`** : Script d'installation qui :
   - Crée une version de `gtp` avec chemins absolus
   - L'installe dans `/usr/bin/`

### Fichiers temporaires

Les scripts temporaires sont créés dans `/tmp/gtp_<project_name>.sh` et automatiquement supprimés après usage.

## Historique des versions

### v1.2 (Actuelle)

- ✅ Support de l'option `never_ask` pour exécuter les commandes sans confirmation
- ✅ Demande de confirmation intégrée dans le script bash généré (compatible zsh)

### v1.1

- ✅ Installation système dans `/usr/bin/`
- ✅ Gestion améliorée des erreurs
- ✅ Nettoyage automatique des fichiers temporaires

### v1.0

- ✅ Version initiale avec fonction zsh
- ✅ Support des projets via JSON
- ✅ Commandes personnalisées

## License

Ce projet est open source. Modifiez, Partagez et Utilisez-le à votre guise.
