## 📦 `ColumnsInLaid` – Gestionnaire de colonnes-incrustées

### 🔍 Objectif

Le module `ColumnsInLaid` gère l’affichage et la suppression de **colonnes-incrustées** (ou *cadres contextuels*) dans l’éditeur Notepad++. Ces colonnes servent d’**interfaces visuelles temporaires** où chaque ligne représente un item sélectionnable, déclenchant une commande.

---

### 🧠 Fonctionnement général

Le système repose sur le principe de **liste contextuelle volante** :

- Une seule colonne est visible à un instant donné.
- Chaque colonne encadre visuellement une liste d’items.
- Ces items sont liés à des commandes exécutables via un `parser`.

---

### 🧱 Deux colonnes gérées dans une session

#### 1. `self.openned` (ancienne colonne)

- Chargée automatiquement depuis le fichier `COLUMN_INLAID_FILE`.
- Représente la **colonne précédemment insérée**.
- Elle peut être analysée (parser) ou supprimée (`flush()`).

#### 2. `self.new_colinlaid` (nouvelle colonne)

- Créée à la volée lors d’un appel à `colinlaid_add(...)`.
- Elle est dessinée dans le texte, à la position du curseur.
- Elle remplace l’ancienne colonne, si elle est encore présente.

---

### 🔁 Cycle typique

```
[ Chargement ] → (colonne existante)
      │
      └─► Si présente : suppression avec flush()
                   │
                   ▼
        colinlaid_add() (nouvelle colonne)
                   │
                   └─► Affichage + mémorisation dans COLUMN_INLAID_FILE
```

---

### 🛠️ Principales méthodes

| Méthode              | Rôle principal                                 |
|----------------------|------------------------------------------------|
| `flush()`            | Supprime la colonne actuellement visible       |
| `colinlaid_add()`    | Crée et affiche une nouvelle colonne-incrustée |
| `parser()`           | Traite la sélection d’un item dans un cadre    |

---

### 🧹 Règle de gestion du `flush()` (suppression de colonne)

La suppression automatique de la colonne-incrustée (`flush()`) s'effectue **par défaut en fin d'invocation**, sauf dans **deux cas spécifiques** où elle est exécutée **avant** l'action principale :

#### 🔁 Cas par défaut : suppression en fin d’invocation

- Lorsqu’aucune action particulière ne précède la fin du script, la colonne encore visible est supprimée par `close_process()`.

#### ⏱ Cas où `flush()` est déclenché immédiatement avant :

1. **Ajout d'une nouvelle colonne** (`colinlaid_add()`)  
   → Toute colonne visible est supprimée avant d’insérer la nouvelle.

2. **Sélection d’un item dans une colonne** (`parser()`)  
   → Le processus suit l’ordre suivant :
   - Lecture de l’item actif (ligne dans le cadre)
   - Appel à `flush()` pour supprimer visuellement la colonne
   - Traitement de l’item (`get_command()` → `parse()`)

#### 📌 Résumé des règles

| Contexte                         | `flush()` appelé avant | `flush()` appelé après |
|----------------------------------|-------------------------|------------------------|
| Lancement normal sans interaction|                         | ✅ oui                |
| Ajout d’une nouvelle colonne     | ✅ oui                  |                      |
| Sélection d’un item dans un cadre| ✅ oui                  |                      |

---

### 💾 Fichier mémoire associé

Le fichier `val_.COLUMN_INLAID_FILE` sert à :

- mémoriser les données de la colonne-incrustée affichée,
- permettre sa suppression automatique lors d’un appel suivant.