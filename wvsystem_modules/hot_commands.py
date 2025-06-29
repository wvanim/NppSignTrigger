# coding: utf-8

import subprocess
import sys


import system       as sys_ 
import string_      as str__
import hot_const    as val_
import column_inlaid      as inlaid_

import hot_goto     as goto_

"""
Commandes déclenchées par  Hotword

mot : 
    - traité comme #command - si key de COMMANDS_HOTWORD : exécute la fonction associé à cette key
    - traité comme '>search' : recherche par étape (recherche répétée à chaque appel 'Alt-w')
.f<|>onction : recherche la déclaration de fonction + efface le point
fichier.f<|>onction : recherche la déclaration de fonction (pas d'effacement)
"""
        
#@str__.wv_automat py
def list_menu(expression):
    """ 
    Ouvre une liste-inclue-dans-le-texte 
    C'est un "menu" extrait du fichier "hot_word.txt" 
    """ 
    #f str__.ON_DEBUG: #rint("e ditor.py/hot_commands.list_menu()  ")   
    script = sys_.io.read_citation_langage("menu",val_.SYSTEM_HOT_WORD_FILE )
    #colinlaid_display(tab.split(ln), None, "menu", expression) # m
    inlaid_.columns_inlaid.add_column(script)
    return True

#@str__.wv_automat    
def list_func_py_(command):
    """ Lister les fonctions d'un fichier .py """
    text = command.text
    path = sys_.ui.getCurrentFilename()
    if command.item=="self":
        scroll = None
    else: 
        scroll = scroll_memo() 
        
        
    #lister les fonction du text édité
    funcs_py = str__.get_functions_by_def(text)
    if scroll: scroll_restore(  scroll  )
    
    if len(funcs_py)<1: return False
    funcs_py.sort()
    max_length = max(map(len, funcs_py))
    func_list = []
    for py in funcs_py:
        pos_def = py.find("def")
        func_list.append ('~'+py[pos_def+4:]+(' '*(max_length-len(py))))
    uni.colinlaid_add(val_.TITLE_FUNCTION, [func_list, None], situation)
    return True

    
def select_menu(line):
     """ TODO exécuter le menu """
def select_error(line):
    print("***ERROR*** sélection sans règle "+line)
    
#@str__.wv_automat            
def dot_command_before( expression ):
    """ 
    Liste des membres de Python, ou de Javascript
    
    TODO : pour l'instant ne recherche que dans Python 
    TODO : utiliser la propriété de fichier 'setter' 
    """
    text = expression.text
    start  = expression.item_area[val_.ID_START] 

    return goto_.init_search_by_step(u"def "+ expression.item )
    #return goto_.select_function_declaration_py_(expression.item, start,  expression.text)
    
def dot_command_after( expression ):
    func_list = sys_.ui.list_func_py(expression) 
    # Ouvre la colonne_incrustee*
    if func_list:
        inlaid_.columns_inlaid.colinlaid_add("members", [func_list, None], "copy_member_init", sys_.ui.get_situation()) 
        #colinlaid_display(func_list, "copy_member_init", "copy_member", expression)
    
def goto_body(aa): return goto("WvBody") 

def goto(word):
    """ 
    Recherche un mot dans l'éditeur et sélectionne la première occurrence trouvée.
    
    Paramètres:
    - word (str): Le mot à rechercher dans le texte de l'éditeur.
    
    Retour:
    - bool: True si le mot est trouvé et sélectionné, False sinon.
    """
    text = sys_.ui.getText()
    # Obtenir la longueur du texte
    text_length = len(text)
        
    # Rechercher le mot
    start = text.find( word )
    
    if start>=0:  # Si une occurrence est trouvée
        start8 = _convert_pos_unicode_to_utf8(start,text)
        word8  = word.encode("utf-8")
        sys_.ui.select_file(start8, start8 + len(word8))
        return True
    else:
        return False


def reinit_project(expression): 
    setting = sys_.io.init_setting()
    sys_.io.write_dictionary(seng, val_.SYSTEMTTING_FILE)

    sys_.io.write_list([1,0],val_.REWING_STACK_FILE)
    goto_.pos_rewind = goto_.RewindStack()
    print("> Projet ré-initialisé.\n")
def activate_command(unused):
    sys_.io.write_item_dictionary(True, val_.SET_ON, val_.SYSTEM_SETTING_FILE)
    print("Command hotword : active")
def inhib_command(unused):
    sys_.io.write_item_dictionary(False, val_.SET_ON, val_.SYSTEM_SETTING_FILE)
    print("mand hotword : inactive")
def zzz_(): print("zzz_ : TODO system") 

def goto_hot_word0(unused): return goto_.select_item_in_system_file("COMMAND_"+"PYTHON", "hot_word.py")
def goto_hot_word1(unused): return goto_.select_item_in_system_file("Une sélection dans notepad déclenche l'action", "hot_word.py")
#@str__.wv_automat
def goto_hot_word2(unused): return goto_.select_item_in_system_file("def "+"hotword_action", "hot_word.py")
def goto_hot_word3(unused): return goto_.select_item_in_system_file("CAR_"+"COMMAND = {", "hot_commands.py")
 
def open_py_file(unused): 
    sys_.ui.open(val_.SYSTEM_FUNCS_PY_FILE)
    return True
def open_hotword_doc(unused): 
    sys_.ui.open(val_.SYSTEM_HOT_WORD_DOC)
    return True
#@str__.wv_automat
def hotname_exec(expression):
    """ 
    Si le signe est une key de "COMMANDS_HOTWORD{}"    - efface ce signe dans Notepad++, si indiqué par
      - un signe 'moins' ('-') suit l'item_cible*
      - le signe est désigné comme effacable*
        l'indicateur d'effacement est placé dans la table-de-commande, en 2ème position
        - sauf si l'item-cible* est suivi d'un signe 'plus' ('+')
    """
    if str__.ON_DEBUG_HOT_WORD: print(">>hot_word.py/hotname_exec expression = '{}'".format(expression.item))
    if not expression: return False
    item = expression.item
        
    # Execute la commande    
    try:
        # Recupérer la table-de-commande,
        # cette table comporte : la fonction à éxécuter et l'indicateur-d'effacement
        print("COMMANDS_HOTWORD["+item+"]")
        exec_ = COMMANDS_HOTWORD[item]
        #suppr:
        print("COMMANDS_HOTWORD["+item+"] {}"+format(exec_))

        # Effacer l'item, dans notepad++, s'il est suivi des signe '-'
        print("SUPPR {}".format((len(exec_)>1 and exec_[COMMAND_SUPPR])))
        if expression.key_command_edit != '+' and ((len(exec_)>1 and exec_[COMMAND_SUPPR]) or expression.key_command_edit == '-'):
            expression.suppr_formula()
            
        return exec_[COMMAND_FUNC](expression)
    except KeyError as e: 
        return False 
#@str__.wv_automat
def colinlaid_suppr_all(context):
    print("hot_commands.py.colinlaid_suppr_all()")
    str_.t # Pour interromptre le traitement
    #inlaid_.columns_inlaid.colinlaid_suppr_all()
def exec_python(context):
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print( context.item )
    print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    exec context.item
    
def print_help(unused):
    print('>'+sys_.io.message_("HELP_COMMAND"))

COMMAND_FUNC        = 0
COMMAND_SUPPR       = 1
COMMAND_SUPPR_LEN   = 1
   
SUPPRESSED = True
NOT_SUPPRESSED = False
def set_path_setting(unused):
    sys_.ui.set_path_setting() 
    
COMMANDS_HOTWORD = {
    "on"            : [activate_command             , SUPPRESSED],
    "off"           : [inhib_command                , SUPPRESSED],
                    #inlaid_.columns_inlaid.colinlaid_add(tab)
    "mnu"           : [list_menu                     , SUPPRESSED],
                    # kc = kill all column_inserted 
    "ga"            : [goto_body                    , SUPPRESSED],
                    # Retour position précédante déclenché par la sélection d'un espace
    "space_rewind"  : [goto_.pos_rewind_previous     ,NOT_SUPPRESSED],           
                    # Retour position précédante déclenché par le text 'x'
    "x"             : [goto_.pos_rewind_previous     , SUPPRESSED],       
                    # Vers position suivante déclenché par le text 'xx'
    "xx"            : [goto_.pos_rewind_next         , SUPPRESSED],           
                    # Retour position précédante déclenché par le text 'xc' et placé dans le presse-papier
    "xc"            : [goto_.pos_rewind_previous_clip, SUPPRESSED],  
                    # Vers position suivante déclenché par le text 'xx'
    "xxc"           : [goto_.pos_rewind_next_clip    , SUPPRESSED],      
                    # Recherche multiple avec le presse-papier
    "search_all"    : [goto_.display_next            , NOT_SUPPRESSED],
    "reinit_w"      : [reinit_project                , SUPPRESSED],
                    # Ouvre le fichier 'functions.py', qui liste les fonctions Pytons de tous les fichiers Python
    "open_py"       : [open_py_file                  , SUPPRESSED],
                    # Le fichier, édité dans Notepad++, définit le dossier_utilisateur ou dossier_de_travail*
    "pth"           : [set_path_setting       , SUPPRESSED],
                    # Affiche l'aide
    "hlp"           : [ print_help                  , SUPPRESSED],
    #_____________________________________________
    # Accès aux pages systèmes  
                    # Accède à l'onglet : hot_word.py/COMMANDS_HOTWORD
    "hw0"           : [goto_hot_word0               , SUPPRESSED],
    "hwa"           : [goto_hot_word0               , NOT_SUPPRESSED],
                    # Accède à l'onglet : hot_word.py/Une  sélection dans notepad déclenche l'action
    "hw1"           : [goto_hot_word1               , SUPPRESSED],
    "hwb"           : [goto_hot_word1               , NOT_SUPPRESSED],
                    # Accède à l'onglet : hot_word.py/def  hotword_action
    "hw2"           : [goto_hot_word2               , SUPPRESSED],
    "hwc"           : [goto_hot_word2               , NOT_SUPPRESSED],
    "hotword_"+"action": [goto_hot_word2            , NOT_SUPPRESSED],
                    # Accède à l'onglet : hot_word.py/CAR_ COMMAND =
    "hw3"           : [goto_hot_word3               , SUPPRESSED],
    "hwd"           : [goto_hot_word3               , NOT_SUPPRESSED],
                    # Ouvre le fichier : functions. py
    "py"            : [goto_.list_functions_py      , SUPPRESSED],
    "docwv"         : [open_hotword_doc             , SUPPRESSED],
                    # TODO 
    "zzz"           : [zzz_                         , NOT_SUPPRESSED]
}
#@str__.wv_automat    
def _car_exec(expression):
    """
    Exécute un signe_de_commande_wv*  
    et efface le signe et/ou l'item_cible* si requis  
    """
    try:
        #suppr:
        print("~~~~~~~~~~expression~~à~traiter~~~~~~~~~~")
        print("key command : '{}'".format(expression.key_command))
        print("parametre   : '"+expression.item+"'")
        str__.print_class(expression,"  ")
        print("----------~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # Récupérer la table de l'action qui comporte : la fonction_Python* et le paramètre 'effacable*'
        if not expression.key_command in CAR_COMMAND:
            return False
        action = CAR_COMMAND[expression.key_command]
        # Effacer l'item, dans notepad++, s'il est suivi des signe '-'
        if expression.key_command_edit != '+' and ((len(action)>1 and action[COMMAND_SUPPR]) or expression.key_command_edit == '-'):
            expression.suppr_sign()
        action[COMMAND_FUNC](expression)
    except KeyError:
        if str__.ON_DEBUG_HOT_WORD: print(">>_car_exec /"+expression.key_command+"/ ERROR")
        return False       

def init_copy_member(expression):
    """ """
def copy_member(expression):
    """ """
def clean_clipboard(expression): 
    str__.clean_clipboard()
CAR_COMMAND = {
    ">x"         : [goto_.init_search_word_by_step   ,  True ],
    '#'          : [hotname_exec                     , False ],
    '.x'         : [dot_command_before               , False ], #TODO fonction .x rechercher l'item 
    'x.'         : [dot_command_after                , False ], #TODO fonction x. ouverture de colinlaid
    'x*'         : [goto_.goto_glossary              , False ], 
    '?'          : [print_help                       ,  True ],
    'x<'         : [goto_.goto_glossary              , False ], 
    ' '          : [goto_.pos_rewind_previous        , False ],
    'clean_key_word' : [clean_clipboard              , False  ],
    '"""{'       : [exec_python                      , False  ]
}
CAR_COMMAND_BEFORE = ('>','#','.')
CAR_COMMAND_AFTER  = ('.','*','<')
CAR_UNIC           = ('?')

""" 
Règles de sélection dans chaque colonne_incrustee*
"""
COLINLAID_RULE = {
    "menu"             : select_menu,
    "init_copy_member" : init_copy_member,
    "copy_member"      : copy_member,
    "select_error"     : select_error
}      
COLINLAID_INIT = {
    "copy_member" : print_help,
    "select_error": select_error
}      

