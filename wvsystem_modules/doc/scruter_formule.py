


def get_token_at_cursor(text, pos):
    """Retourne le mot sous le curseur (variable, fonction, etc.)"""
    m = re.search(r'\b\w+\b', text[pos:] + ' ')
    return m.group(0) if m else None


def resolve_import(text, alias):
    """Résout un alias d'import : import module as alias"""
    for m in re.finditer(r'import (\w+)(?: as (\w+))?', text):
        name, asname = m.groups()
        if alias == (asname or name):
            return name + ".py"
    return None


def resolve_variable_assignment(text, varname):
    """Résout une affectation de type : var = module.Class"""
    m = re.search(r'%s\s*=\s*([\w\.]+)' % re.escape(varname), text)
    return m.group(1) if m else None


def split_chain(expr):
    """Découpe une chaîne d'attributs (ex: a.b.c)"""
    return expr.split('.') if expr else []


def open_module_file(modname):
    """Ouvre un fichier module.py via l'API Notepad++"""
    ui.openPage(modname + ".py")


def find_in_text(text, keyword):
    """Cherche une classe ou fonction dans un texte"""
    return re.search(r'^\s*(def|class)\s+' + re.escape(keyword) + r'\b', text, re.M)


def extract_assignment_target(text, name):
    """Retourne l'expression affectée à une variable donnée"""
    m = re.search(r'%s\s*=\s*([^\n#]+)' % re.escape(name), text)
    return m.group(1).strip() if m else None


def resolve_chain(texts_by_file, current_file, chain):
    """
    Suit une chaîne d'attributs avec résolution d'affectations au moment où elles sont rencontrées.
    """
    i = 0
    while i < len(chain):
        head = chain[i]
        text = texts_by_file.get(current_file)
        if not text:
            return None

        new_file = resolve_import(text, head)
        if new_file and new_file in texts_by_file:
            current_file = new_file
            i += 1
            continue

        resolved = resolve_variable_assignment(text, head)
        if resolved:
            new_chain = split_chain(resolved) + chain[i+1:]
            return resolve_chain(texts_by_file, current_file, new_chain)

        if i+1 < len(chain):
            next_attr = chain[i+1]
            found = find_in_text(text, next_attr)
            if not found:
                return None

        i += 1

    return current_file, chain[-1] if chain else None


def follow_chain(texts_by_file, current_file, expression):
    """Point d'entrée : découpe l'expression et suit la chaîne"""
    chain = split_chain(expression)
    return resolve_chain(texts_by_file, current_file, chain)


# -------------------- TESTS --------------------

# Remarque : 'assert' signifie "vérifie que cette condition est vraie"
# Si la condition est fausse, Python lève une exception AssertionError
# Utile pour écrire des tests simples et rapides

def test_get_token_at_cursor():
    assert get_token_at_cursor("abc.def", 0) == "abc"
    assert get_token_at_cursor("abc.def", 4) == "def"
    assert get_token_at_cursor("abc", 10) is None

def test_resolve_import():
    code = "import os\nimport platform as pform"
    assert resolve_import(code, "os") == "os.py"
    assert resolve_import(code, "pform") == "platform.py"
    assert resolve_import(code, "unknown") is None

def test_resolve_variable_assignment():
    code = "x = mod.Class\ny = autre"
    assert resolve_variable_assignment(code, "x") == "mod.Class"
    assert resolve_variable_assignment(code, "y") == "autre"
    assert resolve_variable_assignment(code, "z") is None

def test_split_chain():
    assert split_chain("a.b.c") == ["a", "b", "c"]
    assert split_chain("abc") == ["abc"]
    assert split_chain("") == []

def test_find_in_text():
    code = "class MaClasse:\n    pass\n\ndef ma_fonction():\n    pass"
    assert find_in_text(code, "MaClasse")
    assert find_in_text(code, "ma_fonction")
    assert not find_in_text(code, "autre")

def test_extract_assignment_target():
    code = "val = module.truc\nnom = 'chaine'"
    assert extract_assignment_target(code, "val") == "module.truc"
    assert extract_assignment_target(code, "nom") == "'chaine'"
    assert extract_assignment_target(code, "absent") is None

def test_follow_chain():
    texts = {
        "main.py": "import mod as m\nx = m.Class\n",
        "mod.py": "class Class:\n    pass\n"
    }
    result = follow_chain(texts, "main.py", "x")
    assert result == ("mod.py", "Class")


def run_all_tests():
    test_get_token_at_cursor()
    test_resolve_import()
    test_resolve_variable_assignment()
    test_split_chain()
    test_find_in_text()
    test_extract_assignment_target()
    test_follow_chain()
    print("Tous les tests sont passés avec succès.")
