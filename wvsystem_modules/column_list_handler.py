# coding: utf-8

import ctypes
import re
import os
import inspect
import functools
import subprocess
from ctypes import wintypes

import system   as sys_
import hot_const as val_
import string_ as str__
import column_inlaid as inlaid_
import hot_parser as parser


    # Signature sur les cadres-intégrés
SEPAR_IN_FILE_INLAID        = "@wv@"
SEPAR_COMMAND_INLAID_LEN = len(SEPAR_IN_FILE_INLAID)

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

def column_list_init(hot_parser, io_adapter, ui_adapter):
    # initialise les colonnes incrustées
    list_source    = ColumnListSource(io_adapter, ui_adapter) #sys_.io, sys_.ui)
    inlaid_.columns_inlaid = inlaid_.ColumnsInLaid(list_source, ui_adapter)
    OnColumnSelectionEvent(inlaid_.columns_inlaid, hot_parser)
    
#************************************************************************************************************************
#************************************************************************************************************************
#
#                                            S E R V I C E   DE   C O L O N N E S - I N C R U S T E E S
#
#************************************************************************************************************************
#************************************************************************************************************************
class ColumnListSource(inlaid_.ListColumnSource, sys_.GenericUIRenderer):
    def __init__(self, io_adapter, ui_adapter): 
        """ """
        sys_.instance_expected( io_adapter, sys_.GenericIo, "io_adapter", "GenericIo")
        
        self.is_present = False
        self._io_adapter = io_adapter
        self._ui_adapter = ui_adapter
        self.hot_parser   = None
    def flush(self):
        if not self.is_present: 
            return
        self.is_present = False
        self._io_adapter.save("", val_.COLUMN_INLAID_FILE)
        
    def update(self, s):
        """
        Convertit les données reçues au format string
        """
        if self.is_present:
            sys_.error(val_.INLAID_UPDATE_PRESENT," update: Column_inlaid is already present")
        self.is_present = True
        situation = sys_.ui.get_situation()
        tab = s.split("\n")
        self.title           = tab[ID_STR_TITRE_INLAID]
        self.command_default = tab[ID_STR_COMMAND_INLAID]
        self.cursor          = situation.cursor_pos
        self.column_file     = situation.file
        self.set_items(tab, ID_STR_ITEM_INLAID)

        return self
        
    def load(self):
        """
        Leture des données depuis le stockage de mémorisation. exemple : 'COLUMN_INLAID_FILE'
        """
        if self.is_present:
            sys_.error(sys_.INLAID_LOAD_PRESENT, "load : Column_inlaid is already present")
        s = self._io_adapter.load(val_.COLUMN_INLAID_FILE, True)
        if s==None or len(s.strip())<1: 
            return False
        
        self.is_present = True
        
        # Récupérer les données
        tab = s.split("\n")
        self.title           = tab[ID_FILE_TITRE_INLAID  ]
        self.command_default = tab[ID_FILE_COMMAND_INLAID]
        self.cursor          = int(tab[ID_FILE_CURSOR_INLAID ])
        self.column_file     = tab[ID_FILE_FILE_INLAID   ]
        
        # Divise les libellés et les commandes en 2 tables distinctes et 1 dictionnaire 
        self.set_items(tab, ID_FILE_ITEM_INLAID)
        
        return True

    def set_items(self, tab, start):
        """
        Divise les libellés et les commandes en 2 tables distinctes*
        - et les réunis dans 1 dictionnaire         
        """
        self._dico     = {}
        self.libelle  = []
        self.commands = []
        isKey         = True
        lineI         = start
        lineNb        = len(tab)
        while lineI<lineNb:
            if isKey: 
                key = tab[lineI]
            else:   
                self.libelle.append(key)
                value = tab[lineI]
                self.commands.append(value)
                self._dico[key] = value
                
            isKey = not isKey
            lineI+=1
    
    def serialize_to_file(self):
        """
        Liste au format fichiers de mémorisation
        """
         
        s = '\n'.join([
            self.title,
            self.command_default,
            str(self.cursor),
            self.column_file
        ]) + '\n'  
        
        # Ajoute les items : libelle et command
        i = 0
        nb =  len(self.libelle)
        while i < nb:
            s += self.libelle[i]   + '\n'
            s += self.commands[i] + '\n'
            i += 1
        return s
        
    def save(self): 
        """ """
        self._io_adapter.save(self.serialize_to_file(), val_.COLUMN_INLAID_FILE)

    def open_page   (self): self._ui_adapter.display_open_at_pos(self.cursor, self.column_file)
    def get_line_num(self): return self._ui_adapter.line_num(self.cursor)
    def get_title   (self): return self.title
    def get_libelle (self): return self.libelle

class Parser(object):
    def __init__(self, _list, hot_parser):
        self._hot_parser = hot_parser
        self._list = _list
    def get_command(self, item):
        return self._list._dico[item]

    def column_selection_action( self, line ):
        """
        Parser de ligne sélectionnée dans la colonne_incrustée*
        Efface la colonne incrustée
        1 - lecture de la ligne
        2 - parse cette ligne associée aux commandes.
            priorité des commandes - Note: '{}' sera remplacé par la ligne
            - commande de ligne. 
            - commande de colonne
            - '>' ligne
            
        -> main() 
            [project_.py]-> play_invocation() 
                [hot_parser.py] -> HotWord.     hot_parser() 
                                -> HotWord.         extern_parsers_exec() 
                    [column_list_handler.py]-> OnColumnSelectionEvent.      parser() 
                        [column_inlaid.py]-> ColumnsInLaid.                     on_selection()
                            [column_list_handler.py] -> ColumnListSource.           column_selection_action()
        """
        #__________________________________________________
        command = self.get_command( line )
        
        # construit la formule_hotword
        if command.find("{}")<0:
            self._hot_parser.key_command = command
            self._hot_parser.item == None
            return True
            
        command = command.replace('{}',line)
            
        # Convertit la formulewv* et expression_hotword*        
        return self.parse(command)
     
    def parse(self, item):
        """
        Convertit la formulewv* et expression_hotword*
        => place la key_command et l'item dans le parser
        format de la formule (dans l'ordre de priorité) :
        - <command>;item
        - item<signe>
        - <signe>item
        - item = '>item"
        
        """
        hot_parser = self._hot_parser
        pos = item.find(';')

        # la commande est séparée par ';' de la valeur
        if pos>0:
            tab = item.split(";")
            hot_parser.key_command = tab[0]
            hot_parser.item        = tab[1]
            return True
            
        # Commande = signe de fin 
        if item[-1:] in hot_parser.cars_after:
            hot_parser.key_command = item[-1:]
            hot_parser.item = item[1:]
            return True
            
        # Commande = signe de début 
        if item[0]  in hot_parser.cars_before:
            hot_parser.key_command = item[0]
            hot_parser.item = item[0:-1]
            return True
                        
        # Commande = ligne dans la colonne 
        hot_parser.key_command = SIGN_COMMAND_DEFAULT
        hot_parser.item = item
        return True
        
    def debug(self):
        print("____COL_INLAID_LIST____")
        print(">title          ="+self.title)
        print(">command default="+self.command_default)
        print("self.libelle     ='{}'".format(self.libelle))
        print("self.commandes  ='{}'".format(self.commands))
        print("-----------------------")
        
class OnColumnSelectionEvent(parser.HotParserListener):
    def __init__(self, column_inlaid, hot_parser):
        
        self._column_inlaid = column_inlaid
        _list = column_inlaid.get_list()
        _list._hot_parser = hot_parser
        self.parser_select = Parser(_list, hot_parser)
        
        hot_parser.add_listener(self)

    """ TODO : déplacer le IU vers colum_inlaid.py - effacement"""    
    def parser(self, hot_parser):
        self._column_inlaid.on_selection(hot_parser.cursor_pos, self.parser_select)
        
