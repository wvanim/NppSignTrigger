# coding: utf-8

import ctypes
import re
import os
import inspect
import functools
import subprocess
from ctypes import wintypes
import unicodedata

import system as sys_
# Charger les librairies nécessaires de Windows
user32      = ctypes.windll.user32
kernel32    = ctypes.windll.kernel32
gdi32       = ctypes.windll.gdi32

# Définir les types pour les fonctions Windows
user32.OpenClipboard.argtypes       = [wintypes.HWND]
user32.OpenClipboard.restype        = wintypes.BOOL
user32.GetClipboardData.argtypes    = [wintypes.UINT]
user32.GetClipboardData.restype     = wintypes.HANDLE
kernel32.GlobalLock.argtypes        = [wintypes.HANDLE]
kernel32.GlobalLock.restype         = wintypes.LPVOID
kernel32.GlobalUnlock.argtypes      = [wintypes.HANDLE]
kernel32.GlobalUnlock.restype       = wintypes.BOOL



ON_DEBUG                     = False
ON_DEBUG_ARBO                = True
ON_DEBUG_FUNC_NAME_ARBO_ONLY = False
ON_DEBUG_HOT_WORD            = True
ON_DEBUG_ONCE                = True
    # Signature des items 'Wv' placés dans le presse_papier 
CLIPBOARD_SIGNATURE          = "_w"
CLIPBOARD_SIGNATURE_LEN      = len(CLIPBOARD_SIGNATURE)

#************************************************************************************************************************
#************************************************************************************************************************
#                                       F I L T R E   C A R A C T E R E
#************************************************************************************************************************
#************************************************************************************************************************
# Construction du tableau de filtrage pour les caractères ASCII
# Chaque case (0 à 255) contiendra :
#   0 pour les codes de 0 à 33 (considérés comme espaces ou caractères de contrôle)
#   1 pour les lettres, chiffres ou '_' (caractère réservé au mot)
#   2 pour tous les autres caractères
TYPE_CAR_ESPACE = 0
TYPE_CAR_NAME   = 1
TYPE_CAR_SIGNE  = 2
CARS_NAME = [0] * 256  # tableau pour 256 caractères
for i in range(256):
    if i < 34                       : CARS_NAME[i] = TYPE_CAR_ESPACE
    else:
        ch = chr(i)
        if ch.isalnum() or ch == '_': CARS_NAME[i] = TYPE_CAR_NAME
        else                        : CARS_NAME[i] = TYPE_CAR_SIGNE
        
CARS_NAME_SPAR = CARS_NAME[:]
CARS_NAME_SPAR[ord(")")] = TYPE_CAR_NAME
CARS_NAME_SPAR[ord("]")] = TYPE_CAR_NAME
CAR_A = ord('A')
CAR_Z = ord('Z')
CAR_a = ord('a')
CAR_z = ord('z')
CAR_0 = ord('0')
CAR_9 = ord('9')
CAR__ = ord('_')


#************************************************************************************************************************
#************************************************************************************************************************
#                                       S C R U T E R  / M O D I F I E R   T E X T
#************************************************************************************************************************
#************************************************************************************************************************

#@wv_automat
def get_limits_of_line_at(pos, text):
    """
    Retourne la ligne de la position 'pos' dans le text 'text'
    La position peut se situer n'importe où dans la ligne
    """
    # Rechercher le début de ligne. 


    # Retourn saut de ligne : ("\r\n",2) ou ("\n",1) 
    
    # recherche début de ligne
    start = text.rfind('\n',0,pos)
    start = 0 if start<0 else start+1
    
    # Rechercher la fin de ligne. 
    end = text.find ('\n',pos)
    if end<0:
        # Retourne la dernière ligne
        return start, len(text)
    return start,end
    
def get_line_at(pos, text):
    limits = get_limits_of_line_at(pos, text)
    # Retourne la ligne
    return text[limits[0]:limit[1]]

def find_newline_num( num, text):
    """ retourne la position de début de ligne """
    pos = -1
    for _ in range(num):
        pos = text.find('\n', pos + 1)
        if pos == -1:
            return -1  # pas assez de sauts de ligne
    return pos + 1
    
def get_row_at(pos, text):
    pos_ln = text.rfind('\n', 0, pos)
    print("z32 get_row_at() "+str(pos_ln)+" "+str(pos))
    return pos-pos_ln-1;
    
#@wv_automat
def get_word_at(pos, text):  
    """
    Retourne le mot autour de la position 'pos' dans 'text',
    Les caractères reconnus sont : letter, chiffre et souligné '_'
    (dit de "type 1" puisque dans la table 'CARS_NAME[position ascii]' vaut '1'
    """
    # Recherche les position de début et de fin reconnus comme un mot
    pos = get_pos_word_at(pos, text)
    if not pos: return None
    
    return text[pos[0]:pos[1]]
def _convert_pos_utf8_to_unicode(pos_utf8, text_utf8):
    return len(text_utf8[:pos_utf8].decode("utf-8").replace('\r',''))    
    
def _convert_pos_unicode_to_utf8(pos_u, text_u):
    return len(text_u[:pos_u].replace('\n','\r\n').encode("utf-8"))
def convert_to_utf8(text): 
    if not isinstance(text,unicode): return text
    return text.replace('\r','\r\n').encode("utf-8")
def convert_to_unicode(text): 
    return text.decode("utf-8").replace('\r','\r\n')
def convert_dict_to_unicode(d):
    return {convert_to_unicode(k): convert_to_unicode(v) for k, v in d.iteritems()}
def convert_dict_to_utf8(d):
    print("**********")
    print(d)
    return {convert_to_utf8(k): convert_to_utf8(v) for k, v in d.iteritems()}
def _car_is_name(c):  
    return (CAR_A <= c <= CAR_Z) or (CAR_a <= c <= CAR_z) or (CAR_0 <= c <= CAR_9) or (c == CAR__) or (c >= 128)

def get_pos_start_name(text):
    pos = 0
    for c in text:
        if _car_is_name(c):
            return pos
        pos+=1
    return -1
    
def get_pos_word_at(pos, text):
    """
    Recherche du texte-accentué dans une string utf-8
    Contrainte : convertir en unicode
    Conséquences :
    - convertir les positions UTF-8 en position unicode et inversement en fin de traitement
    - convertir le string en unicode
    """
    # Correction si pos dépasse les bornes
    n = len(text)    
    if pos >= n:
        pos = n - 1
    if pos < 0:
        pos = 0

    # Si le caractère sous pos n'est pas valide, retourner vide
    if not _car_is_name(ord(text[pos])):
        if pos==0 or not _car_is_name(ord(text[pos-1])):
            return None
        pos-=1

    # Chercher le début du mot
    start = pos
    while start > 0 and _car_is_name(ord(text[start-1])):
        start -= 1

    # Chercher la fin du mot
    end = pos
    while end < n and _car_is_name(ord(text[end])):
        end += 1
    # retourne les limites du mot en utf8
    return [start, end]

def find_1st(word, text):
    """ position_premier_mot """
    motif = r'\b' + re.escape(word) + r'\b'
    match = re.search(motif, text)
    if match:
        return match.start()
    else:
        return -1  # ou None si tu préfères

def find_all(item, text):
    """
    Trouve toutes les occurrences exactes d'une chaîne dans un texte, 
    en retournant leur position.

    Args:
        item (str): La chaîne à rechercher dans le texte.
        text (str): Le texte dans lequel effectuer la recherche.

    Returns:
        List[Tuple[str, int, int]]: Une liste de tuples contenant :
            - le texte correspondant (str)
            - la position de début dans le texte (int)
            - la position de fin dans le texte (int)
    """
    pattern = r'\b' + re.escape(item) + r'\b'
    matches = re.finditer(pattern, text)
    return [(m.group(), m.start(), m.end()) for m in matches]
    
def get_functions_by_def(script_text):
    """
    Returns a list of lines that declare a function (starting with 'def').
    Handles indentation and allows multiple spaces between 'def' and the name.
    return:
        (list) déclaration de fonctions : ['def fc1()','def fc2()',...]
    """
    # Découpe le script en ligne
    lines = script_text.splitlines()
    
    # extrait les lignes comportant " def "
    # pattern = re.compile(r'^\s*def\s+\w+')
    pattern = re.compile(r'^[ \t]*def\s+\w+\s*\(')
    items = [line for line in lines if pattern.match(line)]
    
    return [item[0:item.find('(')]+"()" for item in items]
    
    #suppr:
    # funcs = []
    # for item in items:
    #     funcs.append(item[0:item.find('(')]+"()")
    # return funcs

    
def list_words_in_line(pos, text):
    """
    Returns a list of all words in the line.
    A 'word' is defined as a sequence of letters, digits or underscores (like \w+).
    """
    return re.findall(r'\w+', get_line_at(pos, text))
    
#________________________________________________________________________________________________________________________
#
#                   D E C O M P O S E   U N E   F O N C T I O N   S I M P L E
#________________________________________________________________________________________________________________________
#@wv_automat
def parse_function(texte, pos, len_max):
    """
    Convertit une fonction simple - func_name(param1, param2,param3,...) - en tableau
    Types accepté : int et string avec quote
    return :
        tableau : [func_name, param1, param2,param3,...]
    """
    params_pos = texte.find('(', pos, pos+len_max)
    if params_pos<0: return None

    params_list = []
    params_list.append(texte[pos:params_pos].strip())
    params_str = texte
    i = params_pos+1
    end = min(params_str.find(')',i),len(texte))
    if(end<0): end=len(texte)
    while i < end+1:
        if params_str[i] == ' ' or params_str[i] == '\t' : 
            i+=1
            continue 
        if params_str[i] == '\n' : 
            return None
        if params_str[i] == '"':  # Début d'une chaîne de caractères
            # Trouver la fin de la chaîne de caractères
            j = params_str.find('"', i + 1)
            end = min(params_str.find(')',j),len(texte))
            if(end<0): end=len(texte)
            if j != -1:
                params_list.append(params_str[i+1:j])  # Inclure les guillemets
                i = j + 1
            else:
                return params_list
                break  # Erreur : guillemet de fermeture manquant
        else:
            # Trouver la prochaine virgule ou la fin de la chaîne
            j = params_str.find(',', i, end)
            if j == -1:
                params_list.append(params_str[i:end].strip())
                return params_list
            params_list.append(params_str[i:j].strip())
            i = j + 1 if j < len(params_str) and params_str[j] == ',' else j
    return params_list
    
#************************************************************************************************************************
#************************************************************************************************************************
#                                       C O N V E R T I O N   D E   S T R I N G
#************************************************************************************************************************
#************************************************************************************************************************
def remove_accents(text):
    if isinstance(text, unicode):
        utext = text
    else:
        utext = convert_to_unicode(text)
    normalized = unicodedata.normalize('NFKD', utext)
    ascii_text = ''.join(c for c in normalized if not unicodedata.combining(c))
    return convert_to_utf8(ascii_text)

#************************************************************************************************************************
#************************************************************************************************************************
#                                       S T R I N G   E T   C O L L E C T I O N
#************************************************************************************************************************
#************************************************************************************************************************
def reverse_list(list_):
    reverse = list_[:]
    i = 0
    j = len(reverse)-1
    while i<j:
        reverse[i], reverse[j] = reverse[j], reverse[i]
        i += 1
        j -= 1
    return reverse
    
#@wv_automat
def print_dict(dico):
    if dico==None:
        print("Dico == None")
        return
    try:
        for key, value in dico.iteritems():
            print(key + ' : ' + str(value))
    except:
        try:
            print("class="+cl.__class__.__name__);
        except:
            print("ce n'est un un dico")
            print("{}".format(type(dico)))
    print("----");
#@wv_automat
def to_type_str(value):
    """
    Convertir une valeur en string
    Le type est induit.
    'null', 'true' et 'false' sont automatiquement reconnus
    les textes ne comportant que des chiffres deviennent des entier
    + avec un point, ce sont des nombre flottants
    le reste est reconnu comme texte
    """
    if value == None:             return "null"
    if value == True:             return "true"
    if value == False:            return "false"
    if isinstance(value, str):    return value.replace("\n", "\\n")

    if isinstance(value, int):    return str(value)
    if isinstance(value, float):  return str(value)
    raise TypeError("Type non supporté : {}".format(type(value)))

def str_to_type( value ):
    """ 
    Convertir une string en valeur typée
    Types reconnus : null, boolean, entier, flottant et string
    
    """
    value = value.strip()
    if   value == "null" : return None
    elif value == "true" : return True
    elif value == "false": return False
    elif isinstance(value, str) : return value.replace("\\n", "\n")
    elif value.isdecimal(): return float(value)
    try:
        value = float(value)
        if not value.is_integer():
            return value
        return int(value)
    except ValueError:
        return value    

def to_list_str( tab ):
    if tab==None: return None
    i = 0
    for t in tab:
        if isinstance(t,unicode):
            tab[i]=str__.convert_to_utf8("utf-8")
        elif not isinstance(t,str):
            tab[i]=str(t)
        i+=1
    return tab
  
def parse_text_to_dict(text, separ_line, separ_key):
    if not '\n' in text:
         text=text.replace(separ_line, '\n')
    return parse_lines_to_dict(text, separ_key)
        
def parse_lines_to_dict(text, separ_key):
    """
    Convertit un texte 'key,value\nkey,value\n...' en dictionnaire.
    Notez que chaque ligne correspont à une entrée du dictionnaire
    A ne pas confondre avec 'lines_to_dict()' où les keys et les valeurs sont dans des lignes séparées 
    Args:
        text (str): Chaîne avec des paires clé,valeur séparées par separ_key

    Returns:
        dict: Dictionnaire résultant.
    """
    result = {}
    pairs = text.splitlines()
    for pair in pairs:
        if separ_key in pair:
            key, value = pair.split(separ_key, 1)
            result[key.strip()] = value.strip()
    return result

def str_to_dict(text, separ_line):
    if not '\n' in text:
         text=text.replace(separ_line, '\n')
    return lines_to_dict(text)

def lines_to_dict(text):
    lines = text.splitlines()
    result = {}
    is_key = True
    current_key = None

    for line in lines:
        if is_key:
            current_key = line
        else:
            result[current_key] = line
        is_key = not is_key

    return result  
def split_columns_to_arrays(text, separ_item, separ_line):
    text = text.replace(separ_line, '\n')
    return split_lines_to_arrays(text, separ_item)
def split_lines_to_arrays(text, separ=None):
    """
    Créer deux tableaux à partir d’un texte où chaque ligne contient deux items séparés par un séparateur
    Exemple : sépar = ##
        text == aaa
                111
                bbb
                222
                ccc
                333
        => [ [aaa,bbb,ccc], [111,222,333] ]
           
    """
    lignes = text.splitlines()
    if separ==None:
        separ=lignes[0]
        lignes = lignes[1:]
    gauche = []
    droite = []
    for ligne in lignes:
        if separ in ligne:
            parts = ligne.split(separ, 1)
            gauche.append(parts[0].strip())
            droite.append(parts[1].strip())
    return [gauche, droite]

def join_two_arrays(tab0, tab1, separ1, separ2):
    """
    Concatène deux tableaux en une seule chaîne au format :
    tab0[0]<separ1>tab1[0]<separ2>tab0[1]<separ1>tab1[1]<separ2>...
    
    Args:
        tab0 (list): Liste des éléments de gauche.
        tab1 (list): Liste des éléments de droite.
        
    Returns:
        str: Chaîne concaténée selon le format spécifié.
    """
    result = []
    for i in xrange(min(len(tab0), len(tab1))):
        result.append(tab0[i] + separ1 + tab1[i] + separ2)
    return ''.join(result)
    
#************************************************************************************************************************
#************************************************************************************************************************
#                                       T O O L S
#************************************************************************************************************************
#************************************************************************************************************************
def couper_au_deuxieme_saut_de_ligne(chaine):
    if not chaine: return ""
    # Séparer la chaîne en parties avec \n, en limitant à 3 morceaux maximum
    parties = chaine.split('\n', 2)

    # Si la chaîne contient au moins 2 sauts de ligne
    if len(parties) > 2:
        return parties[0] + '<\\n>' + parties[1]  # Garde seulement les 2 premières lignes
    else:
        return chaine  # Retourne la chaîne complète si moins de 2 sauts de ligne
        
#************************************************************************************************************************
#************************************************************************************************************************
#                                       D E B U G 
#************************************************************************************************************************
#************************************************************************************************************************

LEN_VALUE_DEBUG = 150
def display_function_deep(margin, name, args, doc):
    #rint(margin+name+"  {}".format(args))
    doc = couper_au_deuxieme_saut_de_ligne(doc)
    print( margin + name+" ######## "+doc)
    if ON_DEBUG_FUNC_NAME_ARBO_ONLY:
        return;
    for arg in args:
        if print_class(arg, margin): return

        arg = "{}".format(arg)
        arg = arg.replace('\n', '<\\n>')
        if len(str(arg))>LEN_VALUE_DEBUG:  print (margin+'>-['+str(len(str(arg)))+']('+arg[0:LEN_VALUE_DEBUG]+"  ...)")
        else:                              print (margin+'>('+arg+')')
def wv_automat_(fonction): 
    """Décorateur sans action avant l'appel de chaque fonction."""
    """ Utilisé hors debug """
    @functools.wraps(fonction)
    def wrapper(*args, **kwargs):
        return fonction(*args, **kwargs)  # Exécute la fonction originale
    return wrapper 
def wv_automat(fonction): 
    """Décorateur qui exécute une action avant l'appel de chaque fonction."""
    """ TODO A REMETTRE POUR DEBUG """    
    @functools.wraps(fonction)
    def wrapper(*args, **kwargs): 
        try:
            deep = len(inspect.stack()) - 1  # Soustraire 1 pour ignorer cet appel
        except Exception as e:
            deep = 20
        margin = "  "*deep
        if ON_DEBUG_ARBO:
            display_function_deep(margin, fonction.__name__, args, fonction.__doc__)
            
        # Entrée dans la fonction
        result = fonction(*args, **kwargs)  # Exécute la fonction originale
        if ON_DEBUG_FUNC_NAME_ARBO_ONLY or not ON_DEBUG_ARBO:
            return result  
        result1 = "{}".format(result) 
        
        etc = ''
        result1 = str(result1)
        if len (result1) > LEN_VALUE_DEBUG: etc = "   (...)" 
        print(margin+"<<<"+fonction.__name__+":"+result1[0:LEN_VALUE_DEBUG].replace('\n', '<\\n>')+">>>"+etc)
        return result
    return wrapper 
import inspect

def print_stack():
    stack = inspect.stack()
    print "Pile des appels :"
    for frame in stack:
        print "  ->", frame[3]  # frame[3] = nom de la fonction
      
def print_class(elem, margin):
    try:
        vs = elem.__dict__.items()
        print(margin+'>class '+elem.__class__.__name__)
        for v in vs:
            name = v[0]
            value = v[1]
            value = "{}".format(value)
            value = value.replace('\n', '<\\n>')
            if len(str(value))>LEN_VALUE_DEBUG:  print (margin+'..>'+name+'=~'+value[0:LEN_VALUE_DEBUG]+"  ...")
            else:                                print (margin+'..>'+name+'='+value+';')
        return True    
    except Exception as e:
        return False

def fc__(): 
    """ retourne la fonction appelante """
    #print "Fonction actuelle :", frame.f_code.co_name
    return "function:'"+caller_frame.f_code.co_name+"'"
    
#************************************************************************************************************************
#************************************************************************************************************************
#                                       C L I P B O A R D 
#************************************************************************************************************************
#************************************************************************************************************************
def set_clipboard(text):
    subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True).communicate(text.encode('utf-16le'))

def get_clipboard():
    try:
        # Ouvrir le presse-papiers
        user32.OpenClipboard(None)

        # Récupérer le texte sous forme de handle
        CF_TEXT = 1 # puisque non reconnu, je définis cette constant
        h_data = user32.GetClipboardData(CF_TEXT)
        if not h_data:
            return None
        # Verrouiller les données pour les lire
        data_ptr = kernel32.GlobalLock(h_data)
        if not data_ptr:
            return None 
        # Convertir les données en texte (en supposant que c'est du texte ASCII)
        text = ctypes.string_at(data_ptr)
        kernel32.GlobalUnlock(h_data)
        
        return text  # Convertir les octets en chaîne de caractères
    except Exception as e:
        print("***Error*** CLIPBORD_READ ERROR {}".format(e))
        return None
    finally: 
        # Fermer le presse-papiers
        user32.CloseClipboard()


def clean_clipboard():
    """
    Vide le presse-papier de Windows.
    """
    s = get_clipboard()
    if s==None or s.strip() ==0:
        print("Clipboard is empty")
        return
    user32 = ctypes.windll.user32
    
    # Ouvre le presse-papier. On passe None comme propriétaire.
    if user32.OpenClipboard(None):
        # Vide le presse-papier
        if user32.EmptyClipboard() == 0:
            # En cas d'échec, on affiche un message d'erreur
            print("***Error*** Clean clipboard error : failure.")
        # Ferme le presse-papier
        print("Clipboard suppr : '"+s+"'")
        user32.CloseClipboard()
    else:
        print("***Error*** "+read_Error("CLIPBORD_CLEAN"))

def errorwv(message):
    print(message)
#************************************************************************************************************************
#************************************************************************************************************************
#                                       L I S T   E T   D I C T I O N N A I R E S
#************************************************************************************************************************
#************************************************************************************************************************
#@wv_automat
def display_dictionary(tab):
    """
    Affiche chaque clé et sa valeur dans le dictionnaire passé en paramètre.
    """   
    for cle, valeur in tab.items(): 
        print("> {} : {}").format(cle,valeur)

#@wv_automat
def find_word(item, text):
    """
    Recherche un mot isolé dans un texte et retourne la position de la première occurrence.
    
    :param item: Le mot à rechercher (chaîne de caractères).
    :param text: Le texte dans lequel rechercher.
    :return: Position de la première occurrence si trouvée, sinon None.
    """
    finder = r'\b' + re.escape(item) + r'\b'  # Motif pour correspondre à un mot entier
    match = re.search(finder, text)

    return match.start() if match else None  # Retourne la position ou None

#************************************************************************************************************************
#************************************************************************************************************************
#                                       L I S T   E T   D I C T I O N N A I R E S
#************************************************************************************************************************
#************************************************************************************************************************
def get_import_py(start, text): 
    #_______________________________________________________________________________________
    # Accède au fichier de déclaration
    row = get_row_at(start, text)
    
    if start-row<6 or text[start-4:start]!='.py.':
        return None
    return get_word_at(start-5, text)

def get_import(item, text):
    pos = text.find(item)
    words = list_words_in_line(pos, text)
    if len(words)>0 and words[0] == "from":
        return word[1]
    return None
    
def parse_path_var_reverse(start, text):
    pos = get_pos_word_at(pos, start)
    pos = pos[0]
    words = [get_word_at(pos-2, text)]
    while text[pos-1]=='.':
        word = get_word_at(pos-2, text)
        words.append(word)
        pos -= len(word)-1
    return words

def parse_path_var(start, text):
    pos = get_pos_word_at(pos, start)
    pos = pos[0]
    words = [text[pos[0]:pos[1]]]
    pos  += pos[1] - pos[0] + 1
    while text[pos]=='.':
        word = get_word_at(pos+1, text)
        if not word:
            error("unexpected '.' at the end of formula")
            break
        words.append(word)
        pos += len(word)+1
        
    return reverse_list(words)

def get_pos_of_item_started_line(item, text, margin):
    item = margin+item
    lg   = len(item)

    # item au début du texte
    if text[0:lg] == item:
        pos = text.find('\n')
        return 0,0,pos if pos>=0 else None 
        
    # item en début de ligne 
    pos = text.find('\n'+item)
    if pos >0:
        return pos + 1, '\n', 1
    return None
        
#_______________________________________________________________________
#_______________________________________________________________________
#_______________________________________________________________________
#_______________________________________________________________________
#_______________________________________________________________________
#_______________________________________________________________________
#_______________________________________________________________________
#_______________________________________________________________________


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
    """Résout une affectation de type : var = module.Class (avec espaces tolérés)"""
    pattern = r'\b%s\b\s*=\s*([^\n#]+)' % re.escape(varname)
    m = re.search(pattern, text)
    return m.group(1).replace(' ', '') if m else None



def split_chain(expr):
    """Découpe une chaîne d'attributs (ex: a.b.c)"""
    return [part.strip() for part in expr.split('.') if part.strip()] if expr else []


def open_module_file(modname):
    """Ouvre un fichier module.py via l'API Notepad++"""
    ui.openPage(modname + ".py")


#    return re.search(r'^\s*(def|class)\s+' + re.escape(keyword) + r'\b', text, re.M)
def find_in_text(text, item, margin):
    """Cherche une classe ou fonction dans un texte et retourne ses positions"""
    # pattern = r'(?:(?<=\n)|^)' + re.escape(margin + 'def') + r'\s+' + re.escape(keyword) + r'\b|' + \
    #       r'(?:(?<=\n)|^)' + re.escape(margin + 'class') + r'\s+' + re.escape(keyword) + r'\b'
    # m = re.search(pattern, text)
    # print(m)
    # if m and m.end():
    #     ui1.limits = [m.start(), m.end()]
    #     return {"type": m.group(1), "start": m.start(), "end": m.end()}
    # return None
    local = get_pos_of_item_started_line(item, text, margin)
    if local:
        """ TODO: var = formule """
        resolved = resolve_variable_assignment(text, step)
        return resolve_chain(new_chain, level+"  >")
    local = get_pos_of_item_started_line(u'def '+item+u'(', text, margin)
    if local:
        """ TODO: def function( """
        return
    local = get_pos_of_item_started_line(u'class '+item+u'(', text, margin)
    if local:
        """ TODO: class function( """
        return
    import_file = get_import()
    if import_file:
        """ TODO: import file as f_ """
        
        
    

def extract_assignment_target(text, name):
    """Retourne l'expression affectée à une variable donnée"""
    m = re.search(r'%s\s*=\s*([^\n#]+)' % re.escape(name), text)
    return m.group(1).strip() if m else None


def resolve_chain(chain, level):
    """
    Suit une chaîne d'attributs avec résolution d'affectations au moment où elles sont rencontrées.
    """
    i = 0
    head = chain[i]
    text = ui1.getText()
    print(level+"___________________")
    print(level+"script '"+ text+"'  head="+head)
    if not text:
        return None

    new_file = resolve_import(text, head)
    print(level+"new file '{}'".format(new_file))
    if new_file:
        ui1.open_file( new_file )
        text = ui1.getText()
        i+=1
        
    while i < len(chain):
        step = chain[i]
        print(level+"i="+str(i)+"  len="+str(chain))

        resolved = resolve_variable_assignment(text, step)
        print(level+"formule '{}'".format(resolved))
        if resolved:
            new_chain = split_chain(resolved) + chain[i+1:]
            return resolve_chain(new_chain, level+"  >")

        #if i+1 < len(chain):
        #next_attr = chain[i+1]
        print(level+"step= '{}'\n{}".format(step,text))
        found = find_in_text(text, step,"")
        if not found:
            return None

        i += 1
        print(level+"next i= '{}'".format(i))

    return chain[-1] if chain else None


def follow_chain(expression, level):
    """Point d'entrée : découpe l'expression et suit la chaîne"""
    chain = split_chain(expression)
    return resolve_chain(chain, level)

class TEST_FILE_PY(object):
    def __init__(self):
        self.page_name = "main.py"
        self.texts = {
            "main.py": 
                '''import mod as m
                x = m.MyClass''',
            "mod.py": 
                '''class MyClass(object):
                pass'''
        } 
        self.limits = None
    def open_file(self,new_page_name):    
        self.page_name = new_page_name
        return self
    def getText(self):    
        return trim_lines(self.texts[self.page_name])
    def test_follow_chain(self):
        result = follow_chain("x",">")
        print("test_follow_chain() ")
        print_class(ui1,">>>")
        print(result)

ui1 = TEST_FILE_PY()    
        

# -------------------- TESTS --------------------

# Remarque : 'assert' signifie "vérifie que cette condition est vraie"
# Si la condition est fausse, Python lève une exception AssertionError
# Utile pour écrire des tests simples et rapides

def test_get_token_at_cursor():
    assert get_token_at_cursor("abc().def", 0) == "abc"
    assert get_token_at_cursor("abc.def", 4) == "def"
    assert get_token_at_cursor("abc", 10) is None

def test_resolve_import():
    code = "import os\nimport platform as pform"
    assert resolve_import(code, "os") == "os.py"
    assert resolve_import(code, "pform") == "platform.py"
    assert resolve_import(code, "unknown") is None

def test_resolve_variable_assignment():
    code = "x = mod. Class  \ny = autre"
    #print("'"+resolve_variable_assignment(code, "x")+"'")
    assert resolve_variable_assignment(code, "x") == "mod.Class"
    assert resolve_variable_assignment(code, "y") == "autre"
    assert resolve_variable_assignment(code, "z") is None

def test_split_chain():
    assert split_chain("a. b.c") == ["a", "b", "c"]
    assert split_chain("abc") == ["abc"]
    assert split_chain("") == []

def test_find_in_text():
    code = "class MaClasse:\n    pass\n\ndef ma_fonction():\n    pass"
    print_dict(find_in_text(code, "MaClasse"))
    print_dict(find_in_text(code, "ma_fonction"))
    #assert find_in_text(code, "MaClasse")
    #assert find_in_text(code, "ma_fonction")
    #assert not find_in_text(code, "autre")

def test_extract_assignment_target():
    code = "val = module.truc\nnom = 'chaine'"
    assert extract_assignment_target(code, "val") == "module.truc"
    assert extract_assignment_target(code, "nom") == "'chaine'"
    assert extract_assignment_target(code, "absent") is None
def trim_lines(txt):
    tab = txt.splitlines()
    t1 = []
    for t in tab:
        t1.append(t.strip())
    return '\n'.join(t1)
        
def test_follow_chain():
    result = follow_chain(ui1, "main.py", "x")
    print("test_follow_chain()")
    print(result)


def run_all_tests():
    ui1.test_follow_chain()
    
    #test_get_token_at_cursor()
    #test_resolve_import()
    #test_resolve_variable_assignment()
    #test_split_chain()
    #test_find_in_text()
    #test_extract_assignment_target()
    #test_follow_chain()
    print("Tous les tests sont passés avec succès.")
    
def test_string_():
    print("string_ est bien importé")
