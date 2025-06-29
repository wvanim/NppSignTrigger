# coding: utf-8

"""
HotWord Parser
--------------
Analyse l’environnement de l’éditeur Notepad++ pour détecter et extraire une expression hotword.
Voir `docs/hotword_parser.md` pour la documentation complète (syntaxe, priorités, exemples).
"""
import re
import string_ as str__
import hot_const as val_
import system as sys_

ON_DEBUG_HOT_WORD = val_.ON_DEBUG_HOT_WORD

hot_command = None

class HotParserListener(object):
    def parser(self):
        raise NotImplementedError 

DEBUG_FILE = val_.SYSTEM_MODULES_PATH+"test.py"
class HotWord(object): 
    """
     Classe de parsing des expressions hotword dans Notepad++.
    - Extrait les composants de la commande dans le texte d'origine
      ils sont placé dans les paramètres de lecture dans __init__(), 
        informations extraites du texte origine :
        - fichier édité, position du curseur, mot-cible*, sélection... 
    - reconstinue un format d'appel de commandwv*
      - key_command(*) caractère ou nom pour déclencher l'action wv
    Propriétés : item, file, text, cursor_pos, scroll_line, 
        pos_start pos_end, key_command pos_command aaaiii
    """
    def __init__(self):
        """Initialise le contexte de l'éditeur (texte, curseur, sélection)."""
        self.listeners = []        
        self.file          = sys_.ui.getCurrentFilename()

        self.view          = sys_.ui.getCurrentView()
        self.scroll_line   = sys_.ui.getFirstVisibleLine()
        self.cursor_pos    = sys_.ui.getCurrentPos() 
        # position utilisée pour ce parser. Elle pourra être modifiée selon les besoins 
        self.pos_parser    = self.cursor_pos 
        text = self.text_org = self.text   = sys_.ui.getText()
        
        # Récupérer l'item
        if self.cursor_pos >= len(text):
            self.cursor_pos = len(text)-1
        limits = str__.get_pos_word_at(self.cursor_pos, text)
        if limits:
            self.item_area = limits
            self.item      = text[limits[val_.ID_START]:limits[val_.ID_END]]
        else:
            self.item_area = None
            self.item      = ''

        # Récupérer la sélection   
        sel = sys_.ui.getSelText()
        if sel:
            self.selection    = sel
            self.select_area  = [sys_.ui.getSelectionStart(),sys_.ui.getSelectionEnd()]
        else:
            self.selection    = None
            self.select_area  = None

        # Zone complète de la formule_hotword
        # Initialement à la dim de l'items
        # Elle s'agrandira au fur et à mesure de l'apparitions des signes
        if self.item_area:
            self.formula_area = [self.item_area[val_.ID_START], self.item_area[val_.ID_END]]
        else:
            self.formula_area = [-1,-1]
            
        self.car_prev         = None
        self.car_prev_pos     = -1
        self.car_next         = None
        self.car_next_pos     = -1
        self.key_command      = None
        self.key_command_edit = None
        self.key_command_edit_pos = -1
        self.pos_command      = None
        self.type_suppr       = None
        
        # Définit l'etape effectuée dans l'invocation
        
        self.cars_before      = None
        self.cars_after       = None
        self.cars_unic        = None
        self.items_command    = None 
        
    def add_listener(self, listener):
        if not isinstance(listener, HotParserListener):
            raise "***ERROR*** hot_parser.py : listener is not 'HotParserListener' "

        self.listeners.append(listener)

    # @reference hot_word.py.hot_word_exec()
    def init_tabs(self, cars_before, cars_after, cars_unic, items_command, COMMANDS_EDITION):
        """
        Chaque paramètre agit comme un filtre servant à identifier les composants syntaxiques d’une formule hotword.
        Sauf le dernier. Il liste les parser externes.
            Ces parser offre l'entrée : parser(this_parser)
            puis returne True/False si le traitement est réalisé ou non
            Ex : les colonnes incrustées
            
        Args:
            cars_before (list of str): 
                Liste des signes ou opérateurs situés avant l’*item_cible*, déclenchant une action.
            
            cars_after (list of str): 
                Liste des signes ou opérateurs situés après l’*item_cible*, déclenchant une action.
                Remarque : le caractère « après » est prioritaire sur le caractère « avant » si les deux sont présents.
            
            items_command (list of str): 
                Liste des noms de fonctions reconnues. Elle permet d’identifier les *item_cible* qui doivent être interprétés comme des appels de fonction.
            
            cars_commands_editor (list of str): 
                Liste des caractères terminaux de la formule qui déclenchent une action d’édition dans l’éditeur.
                Exemple : '+' empêche l’effacement ; '-' force l’effacement de la formule dans le document Notepad++.
            
            extern_parser (list of object): 
                Liste des outils externes à utiliser pour le traitement complémentaire des formules.
        """        
        self.cars_before      = cars_before
        self.cars_after       = cars_after
        self.cars_unic        = list(cars_unic)
        self.items_command    = items_command 
        self.COMMANDS_EDITION = COMMANDS_EDITION
    #________________________________________________________________________________________________________________________
    #
    #                                       E X T R A C T I O N   D U   H O T - W O R D
    #________________________________________________________________________________________________________________________
    #@reference hot_word.py.hot_word_exec()
    def hot_parser(self):
        """
        Exécute le parsing selon la priorité des cas reconnus.
        """
        #________________________________________
        # PRIORITE 1 - Sélections de plusieurs espaces
        if self.selection_multi_spaces():
            return True
    
        #________________________________________
        # PRIORITE 2 - Contenu du presse-papier se terminant pas la signature 'CLIPBOARD_SIGNATURE'
        if self.hotword_in_clipboard():
            return True
        #________________________________________
        # PRIORITE 3 - Les parsers externes. Ex : selection dans une colonne_incrustee*
        if self.extern_parsers_exec():
            return True;
        #________________________________________
        # PRIORITE 4 - Script python
        if self.python_script():
            return True
        #________________________________________
        # PRIORITE 5 - Récupération de la sélection
        if self.selection and self._parser_selection(self.selection):
            return True            
        #________________________________________
        # PRIORITE 6 - Pointage avec curseur : Sans item
        if not self.item: 
            return self.item_absent()
        #________________________________________________________________________________
        # PRIORITE 7 - Avec item, récupération des caractère avant, après et commande éditeur
        return self.parse_signs()
        
        
    #************************************************************************************************************************
    #                                       S E L E C T I O N   M U L T I _ S P A C E S
    #************************************************************************************************************************
    def selection_multi_spaces(self):    
        """Vérifie si la sélection ne contient que des espaces."""
        if self.selection and len(self.selection)>1 and len(self.selection.strip())==0:
            self.key_command = val_.CMD_EDIT_CLEAN_KEYWORD
            return True
        return False
        
    #************************************************************************************************************************
    #                                       H O T W O R D   D A N S   C L I P B O A R D
    #************************************************************************************************************************
    def hotword_in_clipboard(self):
        """Vérifie si le presse-papier contient une commande hotword valide."""
        item_clip = self.get_clipboard_hotword()
        if not item_clip:
            return False
            
        if self.selection:
            str__.clean_clipboard()
            return False
            
        # Supprimer la signature
        self.item = item_clip[0:-str__.CLIPBOARD_SIGNATURE_LEN]
        self.key_command = val_.CAR_COMMAND_IS_FUNCTION
        return True

    #************************************************************************************************************************
    #                                       E X T E R N   P A R S E R
    #************************************************************************************************************************
    def extern_parsers_exec(self):
        if not self.listeners: return False
        ok = False
        ok = False
        for parse in self.listeners:
            str__.print_stack()
            if parse.parser(self):
                ok = True
        return ok
        
    #************************************************************************************************************************
    #                                       S C R I P T   P Y T H O N
    #************************************************************************************************************************
    def python_script(self):
        text = self.text
        pos_parser = self.pos_parser
        # recherche de """{
        pos_unic = (pos_parser 
            if text[pos_parser] == '{'
            else pos_parser - 1
                if pos_parser > 0 and text[pos_parser - 1] == "{"
                else -1)
        if pos_unic <0: return False
        pos_end = text.find('}"""')
        if pos_end<0: return False
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(text[pos_unic+1:pos_end] )
        print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")

        self.key_command = '"""{'
        self.item = text[pos_unic+1:pos_end] 
        return True
        # extraitraire """{ script python }"""
    #************************************************************************************************************************
    #                                       I T E M   A B S E N T
    #************************************************************************************************************************
    def item_absent(self):
        print(112)
        text  = self.text
        if ON_DEBUG_HOT_WORD: print(">>hot_parser.py : Aucun item -  key={}, item={}".format(self.key_command,self.item))    

        #------------------------------------------------------------
        # Signe unique présent, ex : '?'
        #------------------------------------------------------------
        pos_parser = self.pos_parser
        text_lg = len(text)
        
        # Recherche du sign unique, avant ou après le curseur
        if text_lg==0:
            self.key_command = None
            self.item = None
            return True
            
        if pos_parser >= text_lg: pos_parser=text_lg-1;
        print(pos_parser)
        pos_unic = (pos_parser 
            if text[pos_parser] in self.cars_unic
            else pos_parser - 1
                if pos_parser > 0 and text[pos_parser - 1] in self.cars_unic
                else -1)
              
        # Le signe unique est présent
        if pos_unic>=0:
            if ON_DEBUG_HOT_WORD: print(">>hot_parser.py : Aucun item + signe-unique "+str(pos_unic)+" -  key={}, item={}".format(self.key_command,self.item))    
            self.car_prev = self.key_command  = text[pos_unic]
            self.car_prev_pos = pos_unic
            self.formula_area = [pos_unic, pos_unic+1]
            # un car_command_editeur présent ?
            pos_unic += 1
            if pos_unic< len(text):
                car = text[pos_unic:pos_unic+1]
                if car in self.COMMANDS_EDITION:
                    self.key_command_edit          = car
                    self.key_command_edit_pos      = pos_unic
                    self.formula_area[val_.ID_END] = pos_unic + 1
            return True
            
        #------------------------------------------------------------
        # Sans signe précédant ni item, on verifier si le curseur ne pointe pas l'item précédant  
        #------------------------------------------------------------
        return self._parse_from_end( pos_parser )
        
    #************************************************************************************************************************
    #                                       P R E L E V E   L E S   S I G N E S
    #************************************************************************************************************************
  
    def parse_signs(self):
        """Détecte les signes autour de l'item (avant et après)."""
        text = self.text
        #------------------------------------------------------------
        # Signe avant l'item : key command - ex : '*'item
        #------------------------------------------------------------
        start = self.item_area[val_.ID_START]-1         # Se positionner sur le caractère précédant l'item
        if start>=0 and text[start] in self.cars_before : 
            self.car_prev = text[start]                 # Mémoriser le signe précédant
            self.car_prev_pos = start                   
            self.formula_area[val_.ID_START] = start    # Ajuster la longueur de la zone formule
            self.key_command = self.car_prev+'x'        # Mémorise la key_commandwv*. Note: sera écrasé par la key suivante l'item si présente
            if ON_DEBUG_HOT_WORD:print(">>hot_parser.py : "+str(start)+" CAR_PREV "+self.car_prev)

        #------------------------------------------------------------
        # Signe après l'item : key command
        #------------------------------------------------------------
        end = self.item_area[val_.ID_END  ]
        if end<len(text) and text[end] in self.cars_after: 
            self.car_next     = text[end]               # Mémoriser le signe suivant
            self.car_next_pos = end
            self.formula_area[val_.ID_END] = end + 1    # Ajuster la longueur de la zone formule
            self.key_command = 'x'+self.car_next        # Mémoriser la commande
            if ON_DEBUG_HOT_WORD: print(">>hot_parser.py : "+str(end)+" CAR NEXT "+self.car_next)
                
        #------------------------------------------------------------
        # Signe final = key_command_editeur*
        #------------------------------------------------------------
        # Caractère de commande d'édition '+' ou '-'
        area_end = self.formula_area[val_.ID_END]
        if area_end and area_end<len(text) and text[area_end] in self.COMMANDS_EDITION:
            self.key_command_edit = text[area_end]
            self.key_command_edit_pos = area_end
            self.formula_area[val_.ID_END] = area_end + 1
                
        #------------------------------------------------------------
        # Sans signe
        #------------------------------------------------------------
        print("__{}___".format(self.key_command))
        if not self.key_command:
            print(114)
            if self.item in self.items_command:  
                # Ajouter la key_command de fonction
                self.key_command = val_.CAR_COMMAND_IS_FUNCTION
            else:
                # Ajouter la key_command de recherche
                self.key_command = val_.CAR_COMMAND_SEARCH         
        return True
        
    #************************************************************************************************************************
    #                                        S E L E C T I O N
    #************************************************************************************************************************
    #@str__.wv_automat    
    def _parser_selection(self, s):
        """
        Analyse une sélection pour extraire un hotword ou basculer en mode curseur.
        - traite les sélections uniquement composées d'un ou plusieurs espaces
          return True pour interrompre l'analyse: l'expression_hotword* est constituée
        - si l'item-cible* est absent, la formule est absente
          return True pour interrompre l'analyse: l'expression_hotword* est constituée       
        - sinon positionne le curseur au début de l'item puis
          return False pour continuer le traitement 'curseur'
          
        Args:
            s (str): Texte sélectionné

        Returns:
            bool: True si formule détectée, False sinon (poursuite).
          
        """
        #--------------------------------------------
        # Vide : ne rien faire
        #--------------------------------------------
        selection_len = len(s) 
        if selection_len==0: return False
        self.formula_area = self.select_area
        #--------------------------------------------
        # Car unic, dans la table 'self.cars_unic'. Ex : '?' ou ' '
        #--------------------------------------------
        if s == ' ':
            self.key_command = ' '
            self.item = ''
            
            # Lire la key_commande_editor
            
            if ON_DEBUG_HOT_WORD: print(">>hot_parser.py : _parser_selection() - '?' ou ' '")
            return True
        #--------------------------------------------
        # Espaces sélectionnés => vider le presse papier si avec suffixe
        #--------------------------------------------
        s = s.strip()
        if len(s) == 0:
            self.item     = val_.CMD_EDIT_CLEAN_KEYWORD
            self.car_prev = val_.CAR_COMMAND_IS_FUNCTION
            self.formula_area = [0,0]

            if ON_DEBUG_HOT_WORD: print(">>hot_parser.py : _parser_selection() - '    ' plusieurs espaces")
            return True
           
        #--------------------------------------------
        # Recherche la position du début de l'item
        #--------------------------------------------
        self.pos_parser = str__.get_pos_start_name(s)
        if self.pos_parser >= 0:
            return False
        #--------------------------------------------        
        # La sélection ne comporte pas d'item
        self.item        = ''
        self.key_command = None
        self.key_command_edit = None
        self.formula_area = [0,0]
        return True
        
    #________________________________________________________________________________________________________________________
    #
    # Construit l'expression-hotword en partant de la fin (Ctrl-f+33)
    #________________________________________________________________________________________________________________________
    #
    #@str__.wv_automat     
    def _parse_from_end(self, pos_parser):
        """Détecte une formule hotword si le curseur est situé juste après. """
        text = self.text
        if self.key_command: return True
        
        #________________________________________
        # Les signes précédant le curseur définissent une formule : key-command-edit [+=] ou key-command [*.(]        
        pos_parser = self._parse_cursor_after_formula(pos_parser)
        if pos_parser == -1: return False
       
        #________________________________________
        # Caractère précédant est une commande unique
        if text[pos_parser] in self.cars_unic:
            self.formula_area[val_.ID_START] = pos_parser
            self.key_command = text[pos_parser]
            return True
        # Reconstituer l'item précédant
        # L'item précédant est présent
        limits = str__.get_pos_word_at(pos_parser, text) if pos_parser > 0 else None
        if not limits:
            self.key_command = None
            self.key_command_edit = None
            self.formula_area = [0,0]
            return False
        
        start = limits[val_.ID_START]
        self.item_area = limits
        self.item      = text[start:limits[val_.ID_END]]
        self.formula_area[val_.ID_START] = start        
        if not self.key_command: self.key_command = val_.CAR_COMMAND_SEARCH
        #________________________________________
        # Reconstituer la key_command_précédante
        if start>0 and text[start-1] in self.cars_before:
            start            -= 1
            car               = text[start]
            self.car_prev     = car
            self.car_prev_pos = start
            if not self.key_command or self.key_command==val_.CAR_COMMAND_SEARCH :
                self.key_command = car+'x'
            self.formula_area[val_.ID_START] = start
        return True
        
    def _parse_cursor_after_formula(self, pos_parser):
        """
        Si aucune formule_hot_word* n'a été détectée
        le parser analyse ici les signes placés juste avant le curseur
        """
        pos_parser -= 1        
        #________________________________________
        # Le curseur est placé après le signe-command-d'edition [+-]
        # Puis vérifie la présence d'un key_command after
        # cas : item*-  le curseur est placé sur le - 
        if self.text[pos_parser+1] in self.COMMANDS_EDITION:
            pos_parser += 1
        if self.text[pos_parser] in self.COMMANDS_EDITION:
            #________________________________________
            # Présence de commande-éditeur [+-] sous le curseur-text 
            self.formula_area         = [pos_parser,pos_parser + 1]
            self.key_command_edit     = self.text[pos_parser]
            self.key_command_edit_pos = pos_parser
            
            # Pas de key-command-after [*.(]  
            pos_parser -= 1              
            if not self.text[pos_parser] in self.cars_after: return pos_parser
            #________________________________________
            # Présence du key-command-after [*.(]
            # Ex : item*+ ici nous traitons '*' après avoir traité '+'        
                  
            self.formula_area         = [pos_parser,pos_parser + 2]
            self.car_next             = self.text[pos_parser]
            self.car_next_pos         = pos_parser
            self.key_command          = 'x'+self.text[pos_parser]
            return pos_parser-1  
            
        # Le curseur n'est pas placé après le key-command-after [*.(]        
        if not (self.text[pos_parser] in self.cars_after): return -1       

        #________________________________________
        # Le curseur est placé après le key-command-after [*.(]
        self.formula_area             = [pos_parser,pos_parser + 1]
        self.car_next                 = self.text[pos_parser]
        self.car_next_pos             = pos_parser
        self.key_command              = 'x'+self.text[pos_parser]
        return pos_parser
        
    #________________________________________________________________________________________________________________________
    #
    # Effacement de tout ou partie de la formule                                      
    #________________________________________________________________________________________________________________________
    def suppr_sign(self):
        """
        Efface  les caractères dans Notepad
        Soit toute la zone formulewv*
        Soit le caractère précédant ou suivant uniquement
        """
        if sys_.ui.get_situation().text != self.text :
            print("hot_parser#suppr_formula() le texte est modifié depuis le lancement de la macro")
            ERROR.ERROR
        
        flag_dec = False
        if self.car_prev:
            sys_.ui.deleteRange(self.car_prev_pos, 1)
            self.suppr_pointers(self.car_prev_pos, 1)
            flag_dec = True

        if self.car_next:
            sys_.ui.deleteRange(self.car_next_pos, 1)
            self.suppr_pointers(self.car_next_pos, 1)
            flag_dec = True            
             
        if self.key_command_edit:
            sys_.ui.deleteRange( self.key_command_edit_pos, 1)
            self.suppr_pointers( self.key_command_edit_pos, 1)
            flag_dec = True
            
        if flag_dec: 
            sys_.ui.get_situation().text = self.text       = sys_.ui.getText(  ) 
            sys_.ui.get_situation().cursor_pos = self.cursor_pos = sys_.ui.getCurrentPos() 
                    
    def suppr_formula(self):
        if self.formula_area:
            if sys_.ui.get_situation().text != self.text :
                sys_.error("hot_parser#suppr_formula() le texte est modifié depuis le lancement de la macro")
            nb =  self.formula_area[1]-self.formula_area[0]
            sys_.ui.deleteRange(self.formula_area[0], self.formula_area[1])
            self.suppr_pointers( self.formula_area[0], nb)
            sys_.ui.get_situation().text = self.text       = sys_.ui.getText(  ) 
            sys_.ui.get_situation().cursor_pos = self.cursor_pos = sys_.ui.getCurrentPos() 
    
    def suppr_pointers(self, pos, nb):
        """ mise à jour des pointeurs après la suppression d'un caractère """
        if self.cursor_pos           and self.cursor_pos                   > pos: self.cursor_pos                   -= nb
        if self.item_area            and self.item_area   [val_.ID_START]  > pos: self.item_area   [val_.ID_START]  -= nb
        if self.item_area            and self.item_area   [ val_.ID_END ]  > pos: self.item_area   [ val_.ID_END ]  -= nb
        if self.select_area          and self.select_area [val_.ID_START]  > pos: self.select_area [val_.ID_START]  -= nb
        if self.select_area          and self.select_area [ val_.ID_END ]  > pos: self.select_area [ val_.ID_END ]  -= nb
        if self.formula_area[0]>=0   and self.formula_area[val_.ID_START]  > pos: self.formula_area[val_.ID_START]  -= nb
        if self.formula_area[0]>=0   and self.formula_area[ val_.ID_END ]  > pos: self.formula_area[ val_.ID_END ]  -= nb

        if self.car_prev_pos         and self.car_prev_pos         > pos: self.car_prev_pos         -= nb
        if self.car_prev_pos         and self.car_prev_pos         > pos: self.car_prev_pos         -= nb
        if self.key_command_edit_pos and self.key_command_edit_pos > pos: self.key_command_edit_pos -= nb
            
            
    #________________________________________________________________________________________________________________________
    #
    # Service clipboard                                      
    #________________________________________________________________________________________________________________________
    def get_clipboard_hotword(self):
        """ Récupère le contenu du presse-papier si c'est une formule_hotword* """
        item_clip = str__.get_clipboard()
        return (item_clip 
                if item_clip and item_clip>str__.CLIPBOARD_SIGNATURE_LEN and item_clip[-str__.CLIPBOARD_SIGNATURE_LEN:]==str__.CLIPBOARD_SIGNATURE
                else None)
    def _print_debug(self):
        """ """
        print("Résultat : {}  {}  {} {} *** {} ".format(lg_(20,self.key_command,"'"), lg_(10,self.item,"'"), lg_(10,self.key_command_edit,"'"), lg_(20, self.get_formula(),"|"), lg_(50,self.label,'*')))
    
    def get_formula(self):
        if self.formula_area[val_.ID_START]==-1:
            return ""
        return self.text[self.formula_area[val_.ID_START]: self.formula_area[val_.ID_END]]
        

