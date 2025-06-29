# Documentation externe : HotWord Parser

## Présentation
Le module **HotWord Parser** permet d'extraire une "formule hotword" à partir du contexte d'édition dans Notepad++.

Cette formule peut déclencher :
- une commande personnalisée (fonction Python associée)
- une action sur l'éditeur (ex : suppression de la formule)

La formule hotword est identifiée par un **item** accompagné de signes caractéristiques situés avant, après ou en fin :

Note : cette présentation simplifie les manipulations de l'utilisateur final : clic + Alt-w
	il suffit de placer le curseur sur, ou après la formule = 1 seul clic, 
    Note: la sélection de l'item revient à placer le curseur au début de l'item
	La sélection est uniquement indispensable pour sélectionner 1 ou plusieurs espaces
	- 1 seul espace = rewind, positionner le curseur à la position précédante
    - plusieurs espaces : vide le presse-papier

**Exemple de hotword** : `.item*+`
- `.` : signe préfixe ("car_prev"), utilisé comme déclencheur de fonction (si aucun signe suffixe n'est présent).
- `item` : mot-clé cible ("item") repéré dans la sélection ou autour du curseur.
- `*` : signe suffixe ("car_next"), prioritaire sur le préfixe pour définir la commande principale ("key_command").
- `+` : signe final ("key_command_edit"), déclenche une action sur l'éditeur (par exemple : éviter la suppression de la formule).

---

## Analyse syntaxique

### Éléments clés :
- **item** : mot repéré dans le texte, ou sélectionné par l'utilisateur
- **signe préfixe** (`cars_before`) : caractère positionné juste avant l'item, ex: `.` ou `:`
- **signe suffixe** (`cars_after`) : caractère juste après l'item, ex: `*` ou `.`
- **commande d'édition** (`COMMANDS_EDITION`) : caractères finaux comme `+`, `-`

### Format d'appel
```python
hot_command = HotWord()
hot_command.init_tabs(before, after, unic, items_command, edit_commands)
hot_command.hot_parser()
```

---

## Ordre des priorités d'analyse
La méthode `hot_parser()` suit un ordre de priorité strict :

1. **Sélection d'espaces uniquement**
   - Si la sélection contient plusieurs espaces :
     - `key_command = clean_key_word`
     - `item = ''`

2. **Hotword spécial dans le presse-papier**
   - Si le texte se termine par une signature connue
   - Le contenu devient l'item, et `key_command = '#'`

3. **Curseur dans une colonne incrustée**
   - Cas d'une liste structurée détectée par `columns_inlaid`

4. **Analyse de sélection textuelle**
   - Si la sélection contient un item, l'analyse passe à l'étape suivante
   - Si la sélection est ambiguë (sans item), l'analyse s'arrête

5. **Analyse contextuelle via le curseur**
   - Recherche d'un item autour du curseur
   - Analyse des signes à gauche/droite de l'item

6. **Lecture en arrière (cas sans item)**
   - Si aucun item trouvé, recherche d'une formule à gauche du curseur

---

## Sortie du parser

L'objet `HotWord` retourne les propriétés suivantes :

```python
hot_command.key_command        # Commande principale ex: '>x', 'x*', 'clean_key_word'
hot_command.item               # Mot clé détecté
hot_command.key_command_edit   # Commande d'édition (ex: '+', '-')
hot_command.get_formula()      # Formule complète (chaine extraite)
```

---

## Exemples complets
```python
Texte:     "  .mon_client*+ est appelé"
             |--<hotword>--|
Détection :
- item = "mon_client"
- key_command = "x*" (caractère après = '*')
- key_command_edit = '+'
- formule = ".mon_client*+"

---
Texte:     "  mon_client est appelé"
             |<hotword>-|
Détection :
- item = "mon_client"
- key_command = ">" (caractère généré automatiquement)
- key_command_edit = None
- formule = "mon_client"

---
Texte:     " mon_client est appelé"
                      { }<-sélection
Détection :
- item = None
- key_command = "x" (commande 'rewind' )
- key_command_edit = None
- formule = " "
```

---

## Notes techniques
- Les signes suffixes sont prioritaires sur les signes préfixes
- Les espaces seuls peuvent être considérés comme commandes de nettoyage
- La zone `formula_area` permet de délimiter la zone à éventuellement supprimer dans l'éditeur
- L'analyse peut être influencée par les données du presse-papier

---

## Voir aussi
- `debug_hotword.py` : module de test automatique
- `hot_const.py` : définitions des constantes et caractères reconnus
- `string_.py` : fonctions utilitaires sur les chaînes

---

## Auteur
Équipe WvHotWord - Avril 2025

---