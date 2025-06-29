# coding: utf-8

import ctypes
import re
import os
import inspect
import functools
import subprocess
from ctypes import wintypes
from ctypes import wintypes
from Npp import notepad, editor, console
import hot_const as val_
import string_ as str__
import file_
import editor_ as edit_
    # Signature sur les cadres-intégrés
SIGNATURE_INLAID            = "wv"
SEPAR_IN_FILE_INLAID        = "@wv@"
SEPAR_COMMAND_INLAID_LEN = len(SEPAR_IN_FILE_INLAID)
SEPAR_ITEM                  = "@wvitem@"
SEPAR_LINE                  = "@wvline@"

ID_FILE_TITRE_INLAID             = 0
ID_FILE_COMMAND_INLAID           = 1
ID_FILE_CURSOR_INLAID            = 2
ID_FILE_FILE_INLAID              = 3
ID_FILE_ITEM_INLAID              = 4

ID_STR_TITRE_INLAID              = 0
ID_STR_COMMAND_INLAID            = 1
ID_STR_ITEM_INLAID               = 2

# signe 'key_command' ajouté par les parser si aucune commande n'est mentionné pour la colonne_incrustee*  
SIGN_COMMAND_DEFAULT        = '>'

#************************************************************************************************************************
#                                       C O D E S   C A D R E
#************************************************************************************************************************
CADRE_U = [u"─",u"│",u"┌",u"┐",u"└",u"┘"]
CADRE = []
for c in CADRE_U:
    CADRE.append(c.encode("utf-8"))
MARK_LIST_INSIDE_START = "\n"+CADRE[1] 
COL_INLAID_VERTICAL = CADRE_U[1]

...

""" Service d'incrustation de colones de texte dans une page de notepad """
columns_inlaid= ColumnsInLaid(val_.COLUMN_INLAID_FILE)
