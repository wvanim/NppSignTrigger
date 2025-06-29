# coding: utf-8

import ctypes
import re
import os
import inspect
from Npp import notepad
from ctypes import wintypes
import subprocess

# ON_DEBUG_... : voir string_

DEBUG_PARSER       = True
DEBUG_BATCH_PARSER = False
ON_DEBUG_HOT_WORD  = False

# Passage du reload du fichier main au fichier 'project'
RELOAD = None

# Indice pour les variables zone_de_texte*
ID_START = 0
ID_END   = 1

# Titre de colonne_inscrutée
TITLE_MENU     = "menu"
TITLE_FUNCTION = "functions"


# Pour initialiser le projet
# - création du fichier de commandes à effacer : ../wvsystem_datas/cmd_erased.txt
# - initialisation du fichier de retour à position précédante : ../wvsystem_datas/pos_rewind.txt
ON_INIT_PROJECT              = False 
    # Combinaison de touches pour executer WvHotWord
RUN_KEYS                     = "Alt-w"

SEARCH_CLIPBOARD             = "search_all_w" #TODO
    # Commandes WvHotWord (Item_cible*) 
CMD_NAME_POS_PREVIOUS_SPACE  = "space_rewind"
CMD_NAME_POS_PREVIOUS_CLIP   = "xc"
CMD_NAME_POS_NEXT_CLIP       = "xxc"
CMD_EDIT_CLEAN_KEYWORD       = 'clean_key_word'

CAR_COMMAND_IS_FUNCTION      = '#'
CAR_COMMAND_SEARCH           = '>x'

    # Labels utilisés dans le fichier ".system_setting.txt"
SET_LEBEL_PYTHON             = "PYTHON"
SET_LEBEL_JAVASCRIPT         = "JAVASCRIPT"
SET_LEBEL_ALL_NOTEPAD        = "ALL_NOTEPAD"

#________________________________________________________________________________
#
#                                       S E R V I C E   G O T O
#________________________________________________________________________________
# Valeurs initiales du fichier
REWIND_DEFAULT_VALUE           = [-1,0]
# Jeton du rewind' : indique la position du rewind courante
# Note : les position indique le numéro de ligne (et non pas, le numéro du 'rewind')
REWIND_POS_CURR                = 0
# Position maximum
REWIND_POS_MAX                 = 1  
# Nombre d'éléments pour définir une position 
REWIND_ITEM_LEN                = 3 
# Offset de la position du curseur
REWIND_OFFSET_CARET            = 0
# Offset de la position du numéro de ligne
REWIND_OFFSET_LINE             = 1
# Offset du chemin du fichier
REWIND_OFFSET_FILE             = 2

#________________________________________________________________________________
#
#                                       F I C H I E R S
#________________________________________________________________________________
#wv_system.datas = os.path.dirname(__file__)+os.sep
NOTEPAD_PATH          = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+os.sep
SYSTEM_MODULES_PATH   = NOTEPAD_PATH        +"wvsystem_modules"+os.sep
SYSTEM_DATA_PATH      = SYSTEM_MODULES_PATH +"datas"+os.sep
# Memorise le fichier qui comporte une colonne-incrustée*
COLUMN_INLAID_FILE    = SYSTEM_DATA_PATH    +"tempo_column_inlaid.txt"
SYSTEM_SETTING_FILE   = SYSTEM_DATA_PATH    +".system_setting.txt"
SYSTEM_FUNCS_PY_FILE  = SYSTEM_DATA_PATH    +"functions.py"
# Liste des commandes persistantes dans le presse-papier - pour répétition. ex : "xc" et "xxc"
CMD_CLIPBOARD_FILE    = SYSTEM_DATA_PATH    +".cmd_clipboard.txt"
                                            
SYSTEM_MESSAGES       = SYSTEM_DATA_PATH    +".message_"
SYSTEM_ERROR_MESSAGES = SYSTEM_DATA_PATH    +".error_"
SYSTEM_HOT_WORD_FILE  = SYSTEM_DATA_PATH    +".hot_word_fr.txt"
SYSTEM_GLOSSARY       = SYSTEM_DATA_PATH    +".glossary.doc"
SYSTEM_HOT_WORD_DOC   = SYSTEM_DATA_PATH    +"WvHotWord.doc"
                                                                                  
# Mémorise le positions de retour           
REWING_STACK_FILE     = SYSTEM_DATA_PATH    +"tempo_rewind_stack.txt"
# Memorise la recherche-répétée             
SEARCH_NEXT_FILE      = SYSTEM_DATA_PATH    +"tempo_search.txt"

#________________________________________________________________________________
#
#                                       S E T T I N G
#________________________________________________________________________________
USER_FOLDER           = None

# Nom des variables setting
SET_PROJECT_NAME    = "project_name"
SET_VERSION         = "version"
SET_LANGAGE         = "langage"
SET_DESCRIPTION     = "description"
    # Pour la sélection de mot_cibles, accepte la simple présence du curseur dans le mot 
SET_ON              = "on"          # true / false
    # Chemin du dossier WvHotWord
SET_PATH_SYSTEM     = "system_path"
    # Chemin du dossier de donnée de WvHotWord
SET_PATH_SYSTEM_DATA= "system_path_data"
    # Chemin du dossier utilisateur
SET_PATH_USER       = "user_path"
    # Chemin du dossier de données utilisateur
SET_PATH_USER_DATA  = "user_path"
    # Lexique de WvHotWord
SET_GLOSSARY        = "glossary"
    # Lexique de l'utilisateur
SET_USER_GLOSSARY   = "user_glossary"
    # Liste des fichiers à scruter lors des traitements par lot
    # - "PYTHON" : scrute tous les fichier Python du dossier-utilisateur (cf. setting/SET_PATH_USER)
    # - "ALL_NOTEPAD" : scrute tous les onglets de Notepad
SET_DOC_BATCH       = "doc_batch"
SET_EXT_DOC_BATCH   = "ext_batch"
    # unsused
SET_COMMAND_EDITOR  = "command_editor" 
USER_FOLDER         = "user_folder"               
LANGAGE_PROG        = "langage_prog"               

doc_batch       = None


INLAID_UPDATE_PRESENT   = 20
INLAID_LOAD_PRESENT     = 21
INLAID_SOURCE_EMPTY     = 22
INLAID_DataColumnSource_EXPECTED = 23



