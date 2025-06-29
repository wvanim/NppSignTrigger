# HotWord Debugger

Ce module fournit un outil de test automatique pour le parser `HotWord`, destiné à être utilisé dans l’environnement Notepad++ via PythonScript. Il permet de vérifier que les formules "hotword" sont correctement interprétées dans différents contextes de texte, selon la position du curseur ou une sélection.

## 📌 Objectif

Valider le bon fonctionnement du parser `HotWord` en testant automatiquement :

- La détection de l'**item**
- La déduction de la **commande déclenchée** (`key_command`)
- La détection d'une **commande d’édition** (`key_command_edit`)
- La **formule complète** reconnue (`get_formula()`)

Les cas de test sont annotés dans une chaîne de texte à l’aide de :

- `{...}` pour les **sélections**
- `|` pour les **positions de curseur**

## 🔧 Structure principale

### `DebugFormule`

Classe représentant un cas de test.

**Attributs :**

- `text` : texte annoté à analyser
- `expected_command` : commande attendue (`key_command`)
- `expected_item` : mot principal (item)
- `expected_edit` : commande d’édition attendue (`+`, `-`, etc.)
- `expected_formula` : expression hotword complète attendue
- `label` : description du test

**Méthodes principales :**

- `hotword_debug_batch(i)` : exécute tous les tests (sélections et curseurs)
- `_debug_parse_selection(start, end, script)` : analyse une sélection
- `_debug_parse_cursor(cursor, script)` : analyse une position de curseur
- `parse(text)` : extrait les positions de sélection/curseurs et nettoie le texte
- `check_result(command, script)` : vérifie les résultats obtenus

## 🧪 Lancer les tests

### `debug(...)`

Fonction principale qui initialise tous les tests à partir d’un tableau de `DebugFormule`.

**Paramètres :**

- `cars_before` : signes autorisés avant l’item (ex: `>`, `#`, `.`)
- `cars_after` : signes autorisés après l’item (ex: `*`, `.`)
- `cars_unic` : signes isolés déclencheurs
- `items_command` : noms d’item considérés comme commandes
- `COMMANDS_EDITION` : commandes d'édition comme `+` ou `-`

### Exemple de test :

```python
DebugFormule(
  ' 9 - 123  {|it|em|}+| 456', 
  '>', 
  'item', 
  '+', 
  'item+', 
  "item_select+commande_editor+curseur_en_fin"
)
```

## ✅ Résultat attendu

À chaque test, la console Notepad++ affiche :

```
Résultat : 'key_command'  'item'  'edit'  'formule'     *** description
✅ OK ____script____
```

En cas d'erreur :

```
❌ key_command '...', attendu : '...'
❌ item attendu : '...'
❌ edit attendu : '...'
❌ formule: '...', attendu: '...'
```

## 📁 Fichier de test

Le fichier de test à ouvrir dans Notepad++ est défini par :

```python
DEBUG_FILE = val_.SYSTEM_MODULES_PATH + "test.py"
```

## 🛠 Dépendances

Ce module repose sur les composants internes du projet **HotWord** :

- `hot_parser.py`
- `hot_commands.py`
- `editor_.py`
- `string_.py`
- `hot_const.py`

Et sur les objets PythonScript de Notepad++ :

- `notepad`, `editor`, `console`

## 🧠 Remarques

- Ce module s’utilise exclusivement dans l’environnement **Notepad++ + PythonScript**.
- Il est adapté au développement en **TDD (Test Driven Development)** du parser HotWord.

## ✍️ Auteur

Module développé dans le cadre du projet **HotWord** – analyse contextuelle et déclenchement d’actions dans Notepad++.
