# WV-HOT-WORD pour Notepad++ 
**Un couteau-suisse de navigation par symboles**  
*(.classes, #définitions, >recherche, etc.)*

---

## ❓ Aide recherchée  
- [ ] Documenter le code (je suis dyslexique).  
- [ ] Compléter avec de nouvelles idées.  
- [ ] Tester sur différents systèmes.  

> **Contact** : [Votre email/Discord ici].  
---

## 🚀 Fonctionnalités Clés
- **Recherche intelligente** :
  - `.maClasse` → Cherche les déclarations de classe
  - `#define` → Trouve les définitions
  - `>mot` → Recherche itérative
- **Navigation** :
  - ` ` (espace) → Retour à la position précédente
  - `*terme` → Cherche dans le glossaire
- **Gestion de projet** :
  - Historique des positions (`Alt+W` pour naviguer)
  - Support multi-fichiers

---

## 📦 Structure des Fichiers
| Fichier               | Rôle                                                                 |
|-----------------------|----------------------------------------------------------------------|
| `WvJsBasic.py`        | Point d'entrée principal                                            |
| `editor_.py`          | Interface avec Notepad++ (curseur, sélections, etc.)                |
| `hot_commands.py`     | Dictionnaire des commandes (`#help`, `>search`, etc.)               |
| `hot_goto.py`         | Gestion des sauts de position et recherches                         |
| `hot_parser.py`       | Analyse les symboles (`.`, `#`, `>`)                                |
| `project_.py`         | Initialisation du projet et gestion des dépendances                 |

---

## 🛠 Installation
1. Copiez tous les fichiers dans `plugins/PythonScript/scripts/` de Notepad++
2. Lancez `WvJsBasic.py` via le menu *PythonScript* > *Run...*
3. Dans un fichier dans Notepad++, ajoutez les signes ou les opérateurs autour des mots + Alt-W

---

## 🎯 Exemples d'Usage
```python
# Trouver une classe
.maClasse  # → Saute à la déclaration "class maClasse"

# Chercher une définition
#setup  # → Trouve "def setup()"

# Naviguer
monMot >  # → Cherche "monMot" dans tous les fichiers ouverts
