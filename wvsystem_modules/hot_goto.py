# coding: utf-8

import __main__
import os
import subprocess
import re
import sys
import glob
from collections import namedtuple
import unicodedata

from Npp import notepad
import system as sys_
import hot_const as val_
import string_ as str__
import editor_ as edit_

"""
Traitement des actions_hotword* effectuant des changement d'onglet ou de position de curseur
"""

#************************************************************************************************************************
#************************************************************************************************************************
#                                       R  E  W  I  N  D
#************************************************************************************************************************
#************************************************************************************************************************
REWIND_POS_CURR       = val_.REWIND_POS_CURR
REWIND_POS_MAX        = val_.REWIND_POS_MAX  
REWIND_DEFAULT_VALUE  = val_.REWIND_DEFAULT_VALUE
REWIND_ITEM_LEN       = val_.REWIND_ITEM_LEN  
REWIND_OFFSET_CARET   = val_.REWIND_OFFSET_CARET
REWIND_OFFSET_LINE    = val_.REWIND_OFFSET_LINE 
REWIND_OFFSET_FILE    = val_.REWIND_OFFSET_FILE 
     
class RewindStack(object):
    """
    #________________________________________________________________________________________________________________________
    #
    #                                        C O N S T R U C T O R  - D E S T R U C T O R
    #________________________________________________________________________________________________________________________
    """
    def __init__(self):
        """
        Pile de rewind (rewind_stack*) 
        Mémorise les positions du curseur à chaque appel wvhotword*
        
        """
        try:
            self.stack = sys_.io.read_list(val_.REWING_STACK_FILE)  # Lit tout le contenu du fichier
            self.stack[REWIND_POS_CURR] = int(self.stack[REWIND_POS_CURR])
            self.stack[REWIND_POS_MAX] = int(self.stack[REWIND_POS_MAX])
        except Exception as e:
            # Les 2 premières cases sont réservées pour la position-actuelle, et la longueur max de la table
            self.stack = val_.REWIND_DEFAULT_VALUE[:]
            sys_.io.write_list(val_.REWIND_DEFAULT_VALUE[:],val_.REWING_STACK_FILE)
    def pos_save(self):
        """ Sauvegarde la table des 'retour' de position """
        sys_.io.write_list(self.stack,val_.REWING_STACK_FILE)
    def pos_add(self):
        """ 
        Ajoute une position dans la liste 'rewind' 
        Note: pas de mémorisation si la position est à moins 50 caractère du rewind précédant
        """
        file = sys_.ui.getCurrentFilename()
        if not file: return False
        tab = self.stack
        pos = tab[REWIND_POS_CURR]
        
        # Si la position ctrl-pos_ est la position courante => quitter 
        if pos>REWIND_POS_MAX and self.pos_is_curr(pos): 
            return
        
        if len(tab)<=pos:
            tab.append(None)
        pos += REWIND_ITEM_LEN 
        tab[REWIND_POS_CURR] = pos 
        if tab[REWIND_POS_MAX]<pos: tab[REWIND_POS_MAX]=pos

        tab.insert(pos, file)
        tab.insert(pos, sys_.ui.getFirstVisibleLine())
        tab.insert(pos, sys_.ui.getCurrentPos())
       
        return True

    def pos_previous(self):
        """ 
        Affiche le rewind* précédant dans Notepad++  : changement de page + déplacement de curseur
        Déplace le jeton* vers le rewind* précédant, si possible
        Puis affiche la nouvelle position dans Notepad++
        """
        tab = self.stack        
        pos = tab[REWIND_POS_CURR] 
        # si pos pointe sur 0 ou 1 (cases réservés) - la table pos_rewind est vide
        if pos <= REWIND_POS_MAX+REWIND_ITEM_LEN:
            #rint("*** TODO: traduction - Plus aucune position de retour.\nLe clipboard est vidé\n")
            print("___________________\n1st rewind : End of search")
            str__.clean_clipboard()
            return True

        if self.pos_is_curr(pos): 
            #suppr:
            print("PREVIOUS "+str(pos))
            # Si le curseur-notepad est positionné sur le ctrl-pos_ courrant,
            # => recherche le ctrl-pos_ précédant dans la table
            pos -= REWIND_ITEM_LEN
            tab[REWIND_POS_CURR]=pos
        #suppr:
        print("previous value {} - {}".format(tab[0], pos))
        
        return self._pos_goto(pos)
        
    def pos_next(self):
        """
        Affiche le rewind*-suivant Notepad++ : changement de page + déplacement de curseur  
        Déplace le jeton* vers le rewind* Suivant, si possible
        Puis affiche la nouvelle position dans Notepad++
        """
        # Récupère la position du rewind*-courant
        tab = self.stack        
        pos = tab[REWIND_POS_CURR]
        
        # Vérifie si c'est le dernier rewind*
        if pos>=tab[REWIND_POS_MAX]: return True 
        
        # Passe au goto suivant
        pos += REWIND_ITEM_LEN 
        tab[REWIND_POS_CURR]=pos
        
        # Change l'affichage pour positionner le curseur dans la page du rewind*-suivant
        return self._pos_goto(pos)
        
    def _pos_goto(self, pos): 
        """ 
        Positionne le curseur à l'endroit indiqué dans les 3 lignes désignés par pos
        - position du curseur    : pos + REWIND_OFFSET_CARET
        - position d l'ascenseur : pos + REWIND_OFFSET_LINE
        - fichier à sélectionner : pos + REWIND_OFFSET_FILE
        """
        #rint("hot_goto.py/_pos_goto()-------------")
        #rint(self.to_script())
        # Récupérer les paramètre de rewind*
        tab   = self.stack      
        caret = int(tab[pos+REWIND_OFFSET_CARET])
        line  = int(tab[pos+REWIND_OFFSET_LINE ])
        file  = tab[pos+REWIND_OFFSET_FILE]
        
        # Changer de page Notepad++ (si nécessaire), puis la position du curseur et l'ascenseur
        sys_.ui.display_open_at_pos(caret, file)
        return True
    def pos_is_curr(self, pos):
        """  
        Vérifie si la posirion actuel du curseur est proche de la position précédante
        Dans ce cas, ne mémorise pas la posrition
        """
        caret = sys_.ui.getCurrentPos()
        pos_stack = int(self.stack[pos+REWIND_OFFSET_CARET]) 
        try:
            return self.stack[pos+REWIND_OFFSET_FILE] == sys_.ui.getCurrentFilename() and pos_stack > caret-50 and pos_stack < caret+50  
        except Exception as e:
            return True
    def to_script(self):
        txt = "pos_stack : _____________________________\n"
        for datas in self.stack:
            #txt += str(type(datas))+"\n"
            if isinstance(datas, (int)): 
                txt += str(datas)+'\n'
            else:
                txt += datas+'\n'    
        txt += "------------------------------------------\n"
        return txt
pos_rewind = RewindStack() 

def pos_rewind_next(unused):
    display_pos_rewind("next")    
    return pos_rewind.pos_next() 
def pos_rewind_previous(unused=None):
    display_pos_rewind("rewind*")
    return pos_rewind.pos_previous()
def pos_rewind_next_clip(unused): 
    display_pos_rewind("next")
    str__.set_clipboard(val_.CMD_NAME_POS_NEXT_CLIP+str__.CLIPBOARD_SIGNATURE)    
    return pos_rewind.pos_next()
def pos_rewind_previous_clip(unused):
    display_pos_rewind("rewind*") 
    str__.set_clipboard(val_.CMD_NAME_POS_PREVIOUS_CLIP+str__.CLIPBOARD_SIGNATURE)    
    return pos_rewind.pos_previous()
# 
def display_pos_rewind(message):
    pos = sys_.io.read_list(val_.REWING_STACK_FILE)
    print(">"+message+" pos="+str(pos[0])+"  max="+str(pos[1]))
    
#@str__.wv_automat    
def goto_glossary(command):
    scroll = sys_.ui.scroll_memo()
    if not _goto_glossary(command):
        sys_.ui.scroll_restore(scroll)
    return True

def _goto_glossary(command):
    """ 
    Recherche la définition d'un mot dans un lexique
    Préparation :
        dans le lexique, le mot est inscrit suivi de (*). Exemple : item_cible(*) 
        - note : il peut être inscrit n'importe où, le contexte est indifférent
    Appel: placer une astérisque('*') à la suite du mot recherché 
        + déclencher WvHotWord
     Args:
        command (NotepadSituation): situation de la commande
            item, file, text, cursor_pos, scroll_line,
            pos_start, pos_end, key_command, pos_command
    """
    #suppr:
    print("hot_goto()._goto_glossary() {} {}".format(command, command.item))
    text = sys_.ui.getText()
    if not text: return False
    pos_end = command.formula_area[val_.ID_END]
    if pos_end and pos_end<len(text)-2:
        view = text[pos_end + 1]
        if  view=="0" or view=="1" or view=="2": 
            view = int(view)
            if view==2:             view = None 
        else:                       view = 1
    else:                           view = 1
    
    item =  str__.remove_accents(command.item).lower()    
    car_selector = '(*)'    
    # Rechercher l'item du lexique utilisateur
    file_path = sys_.io.get_setting( "user_glossary" )
    if file_path and sys_.ui.select_word_in_file(item, car_selector, file_path, view):
        return True
        
    # Recherche dans le lexique système
    file_path = sys_.io.get_setting("glossary")
    #suppr:
    print("file_path="+file_path)
    if file_path and sys_.ui.select_word_in_file(item, car_selector, file_path, view):
        return True
    print("file_path="+file_path+"---")
        
    # Recherche dans les scripts_utilisateurs*    
    return sys_.ui.select_word_in_user_files(item, car_selector)   

def select_item_in_system_file(item, file_name):    
    return sys_.ui.select_item_in_file(item, val_.SYSTEM_MODULES_PATH + file_name)    
#************************************************************************************************************************
#************************************************************************************************************************
#                                       L I S T E   D E S   F O N C T O N S   ' P Y '
#************************************************************************************************************************
#************************************************************************************************************************
#@str__.wv_automat
def list_functions_py(unused=None):
    """
    Contruire la liste des fonctions pour chaque fichier "py" 
    pour l'inscrire dans "fichiers.py"
    """
    script_iter = sys_.io.get_scripts_of_project()
    content = ""
    for f in script_iter:
        """ Extrait la liste des fonctions """
        funcs = list_function_names_sorted(sys_.ui.get_script_of_projet(script_iter, True), "\n")  # Lire le texte du fichier
        
        if len(funcs)>0:
            """ Ecriture dans 'functions.py' """
            # Extrait le dossier et le nom du fichier
            pos = f.lower().find(r"pythonscript\scripts")
            #rint("\n______o______"+str(pos)+"  "+f+" \n")

            if len(content)==0:
                # Première ligne du fichier 'functions.py' : chemin vers Python """ 
                content = f[0:pos+20]+"\n    (ci-dessus : chemin vers le dossier de travail)" 
                content += "\n\npy <- pour reconstituer cette librairie, cliquez sur 'py!' + exécutez WvHotWord (Alt+W)" 
            if pos>=0: 
                # Ecriture de d'un fichier
                content +="\n\n#"+f[pos+20:]+"\n"
                content += funcs
    """ Save 'functions.py' """
    sys_.io.save(content,val_.SYSTEM_FUNCS_PY_FILE)
    return True 
        

#@str__.wv_automat
def list_function_names_sorted(text, ln):
    """
    Extrait tous les noms suivant '#@val_.wv_automat
  ' dans le texte et les trie par ordre alphabétique.
    
    :param text: Chaîne contenant du code Python.
    :return: Liste triée des noms de fonctions.
    """
    pattern = re.compile(r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)', re.MULTILINE)  # Regex pour extraire les noms des fonctions
    function_names = pattern.findall(text)  # Trouver tous les noms de fonction
    funcs = sorted(function_names) 
    lines = []
    for f in funcs:
        f = "def "+f+'('
        posStart = text.find(f)
        posEnd   = text.find("\n",posStart)
        if posEnd<0: posEnd   = len(text)
        posEnd = text.rfind(':',0, posEnd)
        if(posEnd<0): continue
        lines.append(text[posStart:posEnd+1])
    return ln.join(lines)
    
    
def _goto_if_function_py(command):
    text = command.text
    item = command.item
    pos_start = command.forrmula_area[val_.ID_START]
    print("TODO__________...")
    return True 

#@str__.wv_automat
def select_function_declaration_py_(item, start, text):
    """
    Sélection la déclaration de la fonction passé en paramètre
    Args: 
        command (NotepadSituation): situation de la commande
            item/, file, text/, cursor_pos, scroll_line,
            pos_start/, pos_end, key_command, pos_command
    """
    scroll = None 
    print(" z11 item unicode={}".format(isinstance(item, unicode)))
    
    # si le point n'est pas précédé de mot, supprimer le point
    if start>1 and text[start-1]=='.' and str__.CARS_NAME_SPAR[ord(text[start-2])]!=str__.TYPE_CAR_NAME:
        sys_.ui.deleteRange(start-1, 1)
    #_______________________________________________________________________________________
    # A l'intérieur du fichier : function.py
    file_name = os.path.basename(sys_.ui.getCurrentFilename())
    if file_name == "functions.py": 
        return goto_function_from_list_py() 
    #_______________________________________________________________________________________
    # Accède au fichier de déclaration
    file_dest = goto_name(u"def "+item)
    return
    #if filedest
    '''
    print("z40")
    if start<2 or ((text[start-1]=="." and str__.CARS_NAME[ord(text[start-2])]==str__.TYPE_CAR_NAME)):
        print("z41")
        scroll = sys_.ui.scroll_memo()
        alias = str__.get_word_at(start-2, text)

        if alias and alias!="py":
            print("z42")
            init_search_by_step( u"def "+item+u"(" )
            return True
        else:
            # Nom complet de fichier
            offset = 3
            if text[start-1]=='.': offset=4 
            if text[start-offset]=='.': 
                file_name = str__.get_word_at(start-offset-1, text)
                text = edit_.get_text_of_file(file_name+".py")
                print("z43 "+file_name)

        if not text: return False
    
    #_______________________________________________________________________________________
    # Lien vers le fichier py non-trouvé on scrute l'ensemble des fichiers.Py
    scroll = sys_.ui.scroll_memo()
    if text==None: 
        return goto_file_function_py(item) 
    #_______________________________________________________________________________________
    # Recherche dans la liste des items dans le texte
    words = str__.find_all(item, text)
    if words == None:
        if scroll: sys_.ui.scroll_restore(scroll)
        return False
        
    # Recherche la déclaration de fonction
    for w in words:
        start = w[1]
        if start<4: continue
        if text[start-4:start-1]=='def':
            edit_.select_file(w[1], w[2])
            return True
            
    # Fonction non trouvé. C'est donc une variable
    if len(words)==0: 
        sys_.ui.scroll_restore(scroll)
        return False
        
    # Sélection de l'Item
    """
    edit_.select_file(words[0][1], words[0][2])
    '''
    return True
#@str__.wv_automat
def goto_name(name):
    scroll = sys_.ui.scroll_memo()
    files = sys_.ui.getFiles()
    for f in files:
        sys_.ui.notepad_open(f[0])
        text = sys_.ui.getText()
        pos = text.find(name)
        if pos>=0:
            sys_.ui.notepad_open_pos(pos, f[0])
            return True
    sys_.ui.scroll_restore(scroll)
    return False
    
def goto_file_function_py(item):
    """ 
    Récupère le mot sous le curseur pour vérifier si c'est un nom de fonction
    Si oui : affiche le fichier dans Notepad++ et sélectionne la déclaration de fonction
    Process :
    a - recupère le mot sous le curseur
    b - recherche ce mot dans le fichier "liste de fonction python" : fichiers.py
    c - Si présent => recherche la déclaration de cette fonction
    d - affiche le fichier '.py' comportant cette fonction,
    e - sélectionne la déclaration
    
    Args:
        item (str): Mot à rechercher
    """
    # Si le fichier édité présente la liste des fonctions 'py'
    # le jeton* saute directement à cette étape
    file_name = os.path.basename(sys_.ui.getCurrentFilename())
    if file_name == "functions.py": 
        return goto_function_from_list_py() 
        
    # Le nom est-il présent dans la base "fonction py"
    funcs = sys_.io.load(val_.SYSTEM_FUNCS_PY_FILE)
    if funcs==None: return False
    pos = str__.find_word(item, funcs)

    if pos<0: return False
    return goto_function_def(pos, funcs)
#@str__.wv_automat
def goto_function_from_list_py():
    # récupérer le nom du fichier et la position du curseur
    s      = sys_.ui.getText()
    cursor = sys_.ui.getCurrentPos()
    return goto_function_def(cursor, s)
#@str__.wv_automat
def goto_function_def(cursor, s):
    ''' 
    
    '''
    print(" z1 ")
    # Extraire la ligne
    line = str__.get_line_at(cursor, s)
    if line.find("def ")<0: return False
    # edit le fichier trouvé
    path_target = functions_py_build_path(cursor, s)
    return sys_.ui.select_item(line, path_target)
        
#@str__.wv_automat
def functions_py_build_path(pos, script):
    """
    Dans "function.py", construire le chamin complet d'un fichier 'py'
    1 - récupérer la 1ère ligne
    2 - rechercher le nom de fichier : '#end_of_path/file_name.py'
    3 - accoler les 2 parties
    """
    if "\r\n" in script: ln = "\r\n"
    else:                ln = "\n"
    path = script[0:script.find(ln)]
    pos_diese = script.rfind("#",0, pos);
    if pos_diese<0: return None
    return path+script[pos_diese+1:script.find(ln,pos_diese)]
#________________________________________________________________________________________________________________________
#
#                                       R E C H E R C H E   P A R   E T A P E S
#________________________________________________________________________________________________________________________
SEARCH__START_FOUND = 7
#@str__.wv_automat
def init_search_word_by_step( command ): 
    """ """
    init_search_by_step( command.item )
#@str__.wv_automat
def init_search_by_step( item ): 
    """
    Recherche par étape () déclenchée par '>mot' ou par .nom_de_fonction => "def nom_de_fonction("
    La situation de recherche est mémorisée en fichier
    la commande est placée dans le presse-papier pour être répétée à chaque appel e WvHotWord
    """
    #item = str__.get_word_at(position_cursor, text)
    if not item: return True    
      
    t = []
    t.append( u"# Memorise les information de recherche-repetee. ex : >text_à-rechercher" )
        # 1 - Position courante pour 'next_find()'
    t.append( unicode(SEARCH__START_FOUND) )
        # 2 - item à chercher
    t.append( item )
        # 3 - Memorise la position originelle, pour se replacer à la fin
    t.append( str__.convert_to_unicode(sys_.ui.get_situation().serializer()))
    #suppr
    print("> SEARCH '{}'".format(t))
    
    files = sys_.ui.getFiles()
    files_ok = []
    for file_edit in files:
        file = file_edit[0]
        file_name = os.path.basename(file)
        if file_name in files_ok: continue
        
        files_ok.append(file_name)
        search_in_file(item, file, t)
        
    #  du fichier Eriture
    s = '\n'.join(t)
    #suppr:
    #print("yyyyyyyyyyy  w")
    #print(str__.convert_to_utf8(s))
    #print("yyyyyyyyyyyyyyyyyyyyyyyy")
    sys_.io.save( s, val_.SEARCH_NEXT_FILE)
    display_next()
    str__.set_clipboard( val_.SEARCH_CLIPBOARD )
    return True
    
def search_in_file(item, file, t):  
    # Ajoute les positions de l'item et le fichier dans un tableau
    # Note: pour chaque item trouvé, mémorise la position ET le chemin-complet-de-fichier
    #       utilisé pour des invocation*s successives à wvhotword* 
    #       Donc, chaque invocation aura accès à une position est un chemin-de-fichier
    sys_.ui.display_open_page(file)
    item_len = len(item)
    s = sys_.ui.getText()
    print(" z15 item '"+file+"' unicode={}".format(isinstance(s, unicode)))
    token = 0
    while True:
        token = s.find(item, token)
        if token<0: break
        
        # Mémorisation de la position et de du chemin de fichier
        t.append( str(token ))
        t.append( file )
        
        # passe l'item pour rechercher le suivant
        token += item_len
#suppr: azez    
def display_next(unused=None):
    print("goto:display_next()") 
    s = sys_.io.load(val_.SEARCH_NEXT_FILE, True)
    if not s:
        print("Search not running")
        return True
    t = s.split('\n')
    #suppr:
    #print("==============")
    #for el in t: print(el)
    #print("======")
    token = int(t[1]) 
    if token >= len(t):
        print("_____________")
        print("End of search")
        str__.clean_clipboard()
        scroll = sys_.ui.read_situation(t, 3)
        sys_.ui.scroll_restore(scroll)
        return True
    #suppr:
    print("----------  ----")
    print(token)
    print("{}-'{}'".format(t[token],t[token+1]))
    print("----------     ----")
    sys_.ui.notepad_open_pos(int(t[token]), t[token+1])
    
    t[1] = str(token+2)
    sys_.io.save("\n".join(t), val_.SEARCH_NEXT_FILE)
    
    return True

def list_attrs(name):
    """ """
    # Rechercher - fichier ou class
    
    # Lister
    
    # Construire le script de la liste
    
    # Ouvrir la liste