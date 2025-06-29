# coding: utf-8

console.show()
console.clear()

import ctypes
import re
import os
import glob
from Npp import notepad, editor
from ctypes import wintypes

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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "wvsystem_modules"))) 
import hot_const as val_
reload(val_)
val_.RELOAD = reload
import project_
reload( project_)
import editor_ as edit_
reload(edit_)
import file_
reload(file_)
import string_ as str__
reload(str__)

# TODO _pos_goto ajouter la 'view'
#________________________________________________________________________________________________________________________
#
#                   E X E C U T E   U N E   E T A P E   D E   W V - H O T - W O R D
#________________________________________________________________________________________________________________________
def main():
    if project_.project_init(): return

    #try:
    project_.play_invocation()
        #f str__.ON_DEBUG: #rint("WvJsBasic : action formulewv = {}").format(ret)
    #except Exception, e:
    #    # Code de gestion de l'erreur
    #    print "Une erreur s'est produite :", e  
    #finally:
    """ """
    project_.project_close()
#______________________________________________________________________
# TEST
# f = notepad.getCurrentFilename()
# file = path, id-buffer, num_onglet[0-n], view[0-1]
# files = notepad.getFiles()  
# for f in files: print(str(f[3])+" "+f[0])

#edit_.notepad_open(val_.SYSTEM_MODULES_PATH+"")

#notepad.runMenuCommand('Recherche', "Rechercher...") #'Clone to Other View')

main()
