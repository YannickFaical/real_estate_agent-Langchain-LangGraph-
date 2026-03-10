# Agent Immobiliers

Un système d'agent immobilier avec deux versions disponibles.

## 🏠 Description

Ce projet contient un agent immobilier capable de:
- Lister les appartements disponibles
- Afficher les détails d'un appartement
- Rechercher des appartements par critères
- Calculer le total des loyers

## 📁 Fichiers

- `simple_app.py` - Version simplifiée sans dépendances externes
- `app.py` - Version complète avec LangChain (requiert installation de dépendances)
- `agent_graph.py` - Graphe de l'agent LangChain
- `tools.py` - Outils LangChain pour l'agent
- `data.py` - Données des appartements
- `test_simple_app.py` - Tests pour la version simplifiée

## 🚀 Utilisation

### Version simplifiée (recommandée)

Aucune installation requise! Exécutez simplement:

```bash
python simple_app.py
```

**Commandes disponibles:**
- `liste` - Afficher les appartements disponibles
- `détails <ID>` - Afficher les détails d'un appartement (ex: `détails A101`)
- `recherche <loyer_max> <pièces>` - Rechercher des appartements (ex: `recherche 3000 2`)
- `calculer <ID1,ID2,...>` - Calculer le total des loyers (ex: `calculer A101,B201`)
- `aide` - Afficher l'aide
- `quit` - Quitter l'application

### Version complète (avec LangChain)

Si vous avez Microsoft Visual C++ Build Tools installé:

1. Installez les dépendances:
```bash
pip install -r requirements.txt
```

2. Configurez votre clé OpenAI dans un fichier `.env`:
```
OPENAI_API_KEY=votre_clé_api_ici
MODEL_NAME=gpt-4o-mini
```

3. Exécutez l'application:
```bash
python app.py
```

## 🧪 Tests

Pour tester la version simplifiée:

```bash
python test_simple_app.py
```

## 📊 Données

Les données des appartements sont définies dans `data.py` avec la structure suivante:
- `id`: Identifiant unique
- `building`: Nom du bâtiment
- `rooms`: Nombre de pièces
- `rent`: Loyer mensuel en MAD
- `status`: "available" ou "occupied"
- `tenant`: Nom du locataire ou None

## 🔧 Problèmes connus

La version complète avec LangChain requiert Microsoft Visual C++ Build Tools pour compiler certaines dépendances (notamment `greenlet`). Si vous ne pouvez pas installer ces outils, utilisez la version simplifiée qui fonctionne sans aucune dépendance externe.

## 📝 Exemples d'utilisation

```
Vous: liste
Agent: A101 | bâtiment: Panorama | pièces: 2 | loyer: 2500 MAD
B201 | bâtiment: Horizon | pièces: 1 | loyer: 1800 MAD

Vous: détails A101
Agent: Appartement A101
Bâtiment: Panorama
Pièces: 2
Loyer: 2500 MAD
Statut: available
Locataire: Aucun

Vous: recherche 3000 2
Agent: A101 | bâtiment: Panorama | pièces: 2 | loyer: 2500 MAD

Vous: calculer A101,B201
Agent: Total = 4300 MAD (A101: 2500 MAD, B201: 1800 MAD)
```
