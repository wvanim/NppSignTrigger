# coding: utf-
"""
HotWord Debugger Module
------------------------
Ce module fournit une classe `DebugFormule` permettant de tester automatiquement le parser `HotWord` dans divers scénarios définis par des annotations simples dans une ligne de texte.

Chaque cas de test permet de valider :
- la détection de l'item
- la commande déclenchée (`key_command`)
- la commande d'édition (`key_command_edit`)
- la formule détectée complète

Les cas sont construits avec une sélection `{}` et des positions de curseur `|`. Des comparaisons avec les résultats attendus sont faites et affichées dans la console Notepad++.
"""

import re

import system as sys_
import string_ as str__
import hot_const as val_
import hot_commands as comm_
import hot_parser as parser_


ON_DEBUG_HOT_WORD = False

# TODO: vérifier que item n'est composé que de lettre chiffre ou '_'

# command.hot_parser(self):

DEBUG_FILE = val_.SYSTEM_MODULES_PATH+"test.py"

class DebugFormule(object):
    """
    Classe représentant un scénario de test pour le parser HotWord.

    Attributes:
        text (str): Le texte brut à analyser, contenant des balises `{}` pour les sélections et `|` pour les curseurs.
        expected_command (str): La `key_command` attendue.
        expected_item (str): L'item attendu.
        expected_edit (str): Le caractère de commande d'édition attendu.
        expected_formula (str): La formule complète attendue.
        label (str): Description du cas de test.
        area_select (list): Plage de sélection `[start, end]` si applicable.
        cursor_pos (list): Liste des positions de curseur à tester.
        error (bool): Indicateur d'erreur après test.
    """
    def __init__(self, text, expected_key_command, expected_item, expected_edit, expected_formula, label):
        self.text_org = self.text = text
        self.expected_command     = expected_key_command
        self.expected_item        = expected_item
        self.expected_edit        = expected_edit
        self.expected_formula     = expected_formula
        self.label                = label

        self.area_select  = [-1,-1]
        self.cursor_pos   = []
        self.error        = False

    def hotword_debug_batch(self, i):
        ''' 
        Lance les différents tests définis dans le texte brut.

        Analyse la sélection (s'il y en a une), puis chaque position de curseur.
        Affiche les résultats et indique les écarts éventuels avec les valeurs attendues.

        Args:
            i (int): Index du test dans la suite.

        Returns:
        '''
        print("__________________________________"+self.text_org+"________________________________________")
        self.text, self.pos = self.parse(self.text)
        ftext = self.text
        start = self.pos["sel_start"]
        end   = self.pos["sel_end"]
        if start: 
            script = "____"+ftext[0:start]+"{"+ftext[start:end]+"}"+ftext[end:]+"____"
            print("+++"+script)
            self._debug_parse_selection(start, end, script) 
                        
        for cursor in self.pos["cursors"]:
            script="____"+ftext[0:cursor]+"|"+ftext[cursor:]+"____"
            self._debug_parse_cursor(cursor, script)

        #----------------------------------------
        print("--------------------------------/"+self.expected_formula.strip()+"/--"+str(len(self.expected_formula.strip())))
        if len(self.expected_formula.strip())>0:
            fpos   = self.text.find(self.expected_formula)
            if fpos>=0:
                self.text = ftext  = self.text[fpos: fpos+len(self.expected_formula)] 
                if start:
                    start -= fpos
                    end   -= fpos
                    script = "____"+ftext[0:start]+"{"+ftext[start:end]+"}"+ftext[end:]+"____"
                    print("***"+script)
                    self._debug_parse_selection(start, end, script) 
                
                for cursor in self.pos["cursors"]:
                    cursor -= fpos
                    script="____"+ftext[0:cursor]+"|"+ftext[cursor:]+"____"
                    print("***"+script)
                    self._debug_parse_cursor(cursor, script)

            
        return self.error
        
    def _debug_parse_selection(self, start, end, script):
        """
        Applique une sélection sur le texte, déclenche le parsing, et vérifie les résultats.

        Args:
            start (int): Position de début de la sélection.
            end (int): Position de fin de la sélection.
            script (str): Représentation visuelle du test.
            
        Outuput:
            Résultat affiché dans la console 
        """
        global hot_command
        global DEBUG_TABS
        
        sys_.ui.setText(self.text)
        sys_.ui.setSelection(start, end)

        
        command = parser_.hot_command = parser_.HotWord()
        command.init_tabs(DEBUG_TABS[0], DEBUG_TABS[1], DEBUG_TABS[2], DEBUG_TABS[3], DEBUG_TABS[4], None)
        command.hot_parser()
        self.check_result(command,script)

    def _debug_parse_cursor(self, cursor, script):
        """
        Place le curseur à une position donnée, lance le parsing et vérifie les résultats.

        Args:
            cursor (int): Position du curseur.
            script (str): Représentation visuelle du test.
        """
        global hot_command
        global DEBUG_TABS

        sys.ui.setText(self.text)
        sys.ui.setSelectionStart(cursor, self.text)
        sys.ui.setSelectionEnd(cursor, self.text)
        sys.ui.setCurrentPos(cursor)
        
        command = parser_.hot_command = parser_.HotWord()
        command.init_tabs(DEBUG_TABS[0], DEBUG_TABS[1], DEBUG_TABS[2], DEBUG_TABS[3], DEBUG_TABS[4])
        command.hot_parser()
        self.check_result(command, script)
        
    def parse(self, text):
        """
        Nettoie le texte brut et enregistre les positions des sélections et curseurs.

        Args:
            text (str): Texte contenant `{}` pour la sélection et `|` pour les curseurs.

        Returns:
            tuple: (texte nettoyé, dictionnaire de positions {"sel_start", "sel_end", "cursors"})
        """
        positions = {
            "sel_start": None,
            "sel_end": None,
            "cursors": []  # pour gérer plusieurs '|'
        }

        result = []
        offset = 0  # nombre de caractères supprimés jusqu'à présent
    
        for i, char in enumerate(text):
            adjusted_index = i - offset  # position corrigée dans la chaîne nettoyée
            if char == '{':
                positions["sel_start"] = adjusted_index
                offset += 1  # on va supprimer ce caractère
            elif char == '}':
                positions["sel_end"] = adjusted_index
                offset += 1
            elif char == '|':
                positions["cursors"].append(adjusted_index)
                offset += 1
            else:
                result.append(char)
    
        cleaned_text = ''.join(result)
        return cleaned_text, positions
    
    def check_result(self, command, script):
        is_ok = True
        print("Résultat : {}  {}  {} {} *** {} ".format(lg_(20,command.key_command,"'"), lg_(10,command.item,"'"), lg_(10,command.key_command_edit,"'"), lg_(20, command.get_formula(),"|"), lg_(50,self.label,'*')))
        if command.key_command != self.expected_command:
            print("❌ {} key_command='{}', attendu: '{}'".format(lg_(40,script,""), command.key_command, self.expected_command))
            is_ok = False
        if command.item != self.expected_item:
            print("❌ {} item='{}' attendu: '{}'".format(lg_(40,script,""),command.item, self.expected_item))
            is_ok = False
        if command.key_command_edit != self.expected_edit:
            print("❌ {} edit='{}' attendu: '{}'".format(lg_(40,script,""),command.key_command_edit, self.expected_edit))
            is_ok = False
        if command.get_formula() != self.expected_formula:
            print("❌ {} formule='{}',  attendu: '{}'".format(lg_(40,script,""),command.get_formula(), self.expected_formula))
            is_ok = False
        if is_ok: 
            print("✅ OK "+script+"")
        else:
            self.error = True
DEBUG_TABS = None
def debug(cars_before, cars_after, cars_unic, items_command, COMMANDS_EDITION):
    """
    Lance la série de tests définis dans le tableau `DEBUGS`.

    Args:
        cars_before (list): Liste des signes valides avant l'item.
        cars_after (list): Liste des signes valides après l'item.
        cars_unic (list): Signes uniques déclencheurs.
        items_command (list): Liste des noms d’item à traiter comme commande.
        COMMANDS_EDITION (list): Liste des caractères de commande d'édition.
    """
    DEBUGS = (      # text                          key1               item    editor  formule      label
        DebugFormule(' 0 - aaa  { } bbb  '        , ' '              , '',     None  , " "        , "Sélectionner 1 espace"),
        DebugFormule(' 1 - 123  {   } 456'        , 'clean_key_word' , '',     None  , ""         , "Plusieurs espaces sélectionnés"),
        DebugFormule(' 2 - aaa  {|?|} bbb  '      , '?'              , '',     None  , "?"        , "Sélectionner 1 espace"),
        DebugFormule(' 3 - aaa  {|?|-|} bbb  '    , '?'              , '',     '-'   , "?-"       , "Sélectionner 1 espace"),
        DebugFormule(' 4 - aaa  {|?|}-| bbb  '    , '?'              , '',     '-'   , "?-"       , "Sélectionner 1 espace"),
        DebugFormule(' 5 - abc ,|,  item | def '  , None             , ''    , None  , ''         , "curseur isolé, sans hotword" ),
        DebugFormule(' 6 - abc  {|it|em|} def  '  , '>'              , 'item', None  , "item"     , "sans key-commande"),
        DebugFormule(' 7 - 123 .|{it|em} 456'     , '.x'             , 'item', None  , ".item"    , "key + select. item"),
        DebugFormule(' 8 - 123  {|it|em}*| 456'   , 'x*'             , 'item', None  , "item*"    , "key + select. item"),
        DebugFormule(' 9 - 123  {|it|em|}+| 456'  , '>'              , 'item', "+"   , "item+"    , "item_select+commande_editor+curseur_en_fin"),
        DebugFormule('10 - 123 .{|it|em|}+| 456'  , '.x'             , 'item', "+"   , ".item+"   , "key+item_select+commande_editor+curseur_en_fin"),
        DebugFormule('11 - 123  {|it|em|}*|+| 456', 'x*'             , 'item', "+"   , "item*+"   , "key+item_select+key.commande_editor+curseur_en_fin"),
        DebugFormule('12 - 123 .{|it|em}*+| 456'  , 'x*'             , 'item', "+"   , ".item*+"  , "key+item_select+key.commande_editor+curseur_en_fin"),
        DebugFormule('13 - 123 .|it|em*+| 456'    , 'x*'             , 'item', "+"   , ".item*+"  , "key+item_select+key.commande_editor+curseur_en_fin"),   
        DebugFormule('14 - {|*|} '                , None             , ''    , None  , ''         , "curseur isolé, sans hotword" ),
        # forcer error -> DebugFormule('13 - 123 .|it|em*+| 456'    , 'x*s'             , 'items', "+s"   , ".item*+s"  , "Errors"),   
    )
    global DEBUG_TABS
    DEBUG_TABS=(cars_before, cars_after, cars_unic, items_command, COMMANDS_EDITION)
    
    sys_.ui.notepad_open(DEBUG_FILE, 1)
    global hot_command

    print("           {}  {}  {} {}     {} ".format(lg_(20,"Key_command",""), lg_(10,"Item",""), lg_(10,"Key_edit",""), lg_(20, "Formula",""), lg_(50,"Description",'')))

    errors = []
    i = 0
    for line in DEBUGS:
        if line.hotword_debug_batch(i):
            errors.append(str(i)+" - "+line.text_org)
        i+=1
    if len(errors)>0:
        print("\n❌❌❌ ERROR ❌❌❌")
        for line in errors:
            print( line )
            
               
def lg_(n, s,separ):
    """
    Formate une chaîne avec une taille fixe et des séparateurs visuels.

    Args:
        n (int): Largeur de champ.
        s (Any): Chaîne ou nombre à formater.
        separ (str): Caractère de bord (ex. "'").

    Returns:
        str: La chaîne formatée avec padding.
    """
    if not s:
        s ='None'
    if isinstance(s, (int, float, long)):
        s = str(s)
    text = u""+separ+"{}"+separ
    s = convert_to_unicode(s)
    s = text.format(s).ljust(n)
    return convert_to_utf8(s)
