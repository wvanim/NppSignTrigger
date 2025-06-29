# coding: utf-8

import ctypes
import re
import os
import glob
from ctypes import wintypes
from Npp import console
console.show()
console.clear()

"""
# Vérification de la version de Python
if sys.version_info[0] == 2:
    # Python 2.x : reload est disponible directement
    reload = __import__('__builtin__').reload
elif sys.version_info[0] == 3:
    # Python 3.x : reload est dans importlib à partir de 3.4
    if sys.version_info[1] >= 4:
        # Pour Python 3.4 et plus : importer depuis importlib
        from importlib import reload
    else:
        # Pour Python 3.0 à 3.3 : reload est dans sys
        from imp import reload
"""
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "wvsystem_modules")))        
import system   as sys_
reload(sys_)

import hot_const as val_
reload = val_.RELOAD

import string_ as str__
reload(str__)
import file_
reload(file_)
import column_inlaid as inlaid_
reload(inlaid_)


import editor_ as edit_
reload(edit_)

sys_.io = file_.FileIO()
sys_.ui = edit_.NppAdaptater()

import hot_parser as parser
reload(parser)
import hot_parser_debug as parser_debug
reload(parser_debug)
import hot_commands as comm_
reload(comm_)
import hot_goto as goto_
reload(goto_)
import hot_parser as pars_
reload(pars_)
import column_list_handler as coldata_
reload(coldata_)



def project_init():
    #teste la recherche de déclaration proposé par l'IA
    #str__.run_all_tests()
    ret = _project_init()
    return ret
 

def _project_init():
    if not os.path.exists(val_.SYSTEM_SETTING_FILE) or sys_.io.read_item(val_.SET_ON, val_.SYSTEM_SETTING_FILE)==None:
        setting = sys_.io.init_setting()
        sys_.io.write_dictionary(setting, val_.SYSTEM_SETTING_FILE)
        # vider la pile de rewind 
        print("> Projet initialisé.\n veuillez relancer votre commande")
        return True
    return False  
    
COMMANDS_EDITION=('+','-')    

""" TODO: faire l'aiguillage de debug/play"""
def debug_invocation():
    ''' initialise les composants fixes '''
    parser.hot_command = HotWord()

    ''' Récupère les setting '''
    # Récupère "quels documents" seront traité par lot
    val_.doc_batch = sys_.io.get_setting(val_.SET_DOC_BATCH)
    
    hot_parser_debug.debug(comm_.CAR_COMMAND_BEFORE, comm_.CAR_COMMAND_AFTER, comm_.CAR_UNIC, comm_.COMMANDS_HOTWORD, COMMANDS_EDITION)
    return True

def play_invocation():
    ''' initialise les composants fixes '''
    # initialise l'outils de lecture de Notepad
    # Convertit la formule_hotword* en expression_hotword*
    parser.hot_command = parser.HotWord()
    
    # initialise les colonnes incrustées
    coldata_.column_list_init(parser.hot_command, sys_.io, sys_.ui)

    ''' Récupère les setting '''
    # Récupère "quels documents" seront traité par lot
    val_.doc_batch = sys_.io.get_setting(val_.SET_DOC_BATCH)
    
    # Ajoute la position du curseur dans la pile rewind*
    goto_.pos_rewind.pos_add()    
    

    # Récupération de la formule-hotword* et du contexte dans Notepad++    
    formule = pars_.hot_command
    formule.init_tabs(comm_.CAR_COMMAND_BEFORE, comm_.CAR_COMMAND_AFTER, comm_.CAR_UNIC, comm_.COMMANDS_HOTWORD, COMMANDS_EDITION)
    # Exécute la formule
    if formule.hot_parser():
        comm_._car_exec(formule)
    
    sys_.ui.grabFocus()
    #i str__.ON_DEBUG: #rint("WvJsBasic : action formulewv = {}").format(ret)

def project_close(): 
    # Fermeture et sauvegarde-infos pour colonne-Incrustée* (cadre incrusté)
    inlaid_.columns_inlaid.close_process()
 
    # Sauvegarde des position-rewind (position de retour)
    goto_.pos_rewind.pos_save()
