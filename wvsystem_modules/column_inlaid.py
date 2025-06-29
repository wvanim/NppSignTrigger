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

"""
Module de gestion de colonne_incrustée* dans l'interface utilisateur.

Fournit :
- Création visuelle de colonnes encadrées avec des cadres Unicode
- Insertion/suppression dynamique de contenu
- Gestion du cycle de vie complet des colonnes

Classes Principales:
    ColumnsInLaid : Contrôleur principal
    _ColumnInlaidUI : Gestionnaire d'interface (usage interne)
"""

class ListColumnSource( object ):
    ''' '''
    def flush(self):
        raise NotImplementedError
    def load(self):
        raise NotImplementedError
    def save(self):    
        raise NotImplementedError
    def update(self, s):    
        raise NotImplementedError
    def open_page(self):    
        raise NotImplementedError
    def get_line_num(self): 
        raise NotImplementedError
    def get_title   (self): 
        raise NotImplementedError
    def get_libelle (self): 
        raise NotImplementedError
    def debug(self):
         raise NotImplementedError

    # Signature sur les cadres-intégrés
SIGNATURE_INLAID            = u"wv"
#columns_inlaid= ColumnsInLaid() 

#************************************************************************************************************************
#************************************************************************************************************************
#                                       C O D E S   C A D R E
#************************************************************************************************************************
#************************************************************************************************************************
CADRE_U = [u"─",u"│",u"┌",u"┐",u"└",u"┘"]
CADRE = []
for c in CADRE_U:
    CADRE.append(c.encode("utf-8"))
MARK_LIST_INSIDE_START = "\n"+CADRE[1] 
COL_INLAID_VERTICAL = CADRE_U[1]
    
# Service de colonne_incrustée
columns_inlaid = None
    
#************************************************************************************************************************
#************************************************************************************************************************
#                                       T E X T E S   E N   C O L O N N E S
#************************************************************************************************************************
#************************************************************************************************************************

#@wv_automat 
def list_inlaid_add(line_start, title, tabOrg, script): 
    """Ajoute une colonne_incrustee* dans le texte.
    
    Args:
        line_start (int): Ligne de départ (0-based)
        title (str): Titre de la colonne
        tabOrg (list): Items à afficher
        script (str): Texte original
        
    Returns:
        str: Texte modifié ou None en cas d'erreur
    """
    # Vérification des paramètres
    if(line_start==None or line_start<0 ): return None 
    if(script==None)                     : return None
    if(not tabOrg or len(tabOrg)==0):
        sys_.warning(sys_.INLAID_SOURCE_EMPTY, "List of words is empty") 
        return None
    if (line_start>0): line_start -= 1
    
    # Dessiner le cadre
    items = _draw_frame(title, tabOrg)
    # Incruste un tableau de texte en début de ligne     
    return _list_insert_at_start_line(line_start, script, items )


   
#************************************************************************************************************************
#************************************************************************************************************************
#                                       T E X T E S   E N   C O L O N N E S
#************************************************************************************************************************
#************************************************************************************************************************

#@wv_automat
def _draw_frame(title, tabOrg):
    """Génère les lignes du cadre UTF-8.
    
    Returns:
        list: Lignes du cadre formatées
    """
    if title==None: 
        title = ''
        
    ''' Dessine le cadre de la liste, place chaque ligne dans une case d'un tableau '''
    # Largeur du tableau pour s'adapter à l'item le plus long
    column_lg = len(max(tabOrg, key=len))
    #max_length = max(map(len, py_line))

    # Construction de la colonne, de largeur fixe, incrustée* dans des balises        
    items = []
    #     ┌wv─title──────┐
    items.append(CADRE_U[2]+SIGNATURE_INLAID+CADRE_U[0]+title+CADRE_U[0]*(column_lg-len(SIGNATURE_INLAID)- 1 -len(title))+CADRE_U[3])

    for w in tabOrg:
        # │ text         |        w = w.decode("utf-8")
        items.append(CADRE_U[1]+w.ljust(column_lg)+CADRE_U[1])
    #     └──────────────┘
    items.append(CADRE_U[4]+CADRE_U[0]*(column_lg)+CADRE_U[5])
    return items

#@wv_automat
def _list_insert_at_start_line(line_start, text, items ):
    """
    Insère chaque case du tableau 'items' au début de chaque ligne à partir de `line_start`.
    Ajoute des lignes si le nombre de items dépasse les lignes existantes.
    
    Args:
    line_start (int): Numéro de la première ligne où incruster les items (indexé à 0).
    text (str): Texte contenant plusieurs lignes.
    items(str): Liste de items à incruster.
    
    Returns: 
        str: Texte modifié.
    """
    item_nb = len(items)
    lines = text.split("\n")  # Découper le text en lines
    # Assurer qu'on a assez de lines pour commencer l'insertion
    while len(lines) < line_start:
        lines.append("")  # Ajoute des lines vides jusqu'à la ligne de départ
    
    # Ajouter des lines vides si nécessaire pour contenir tous les items
    while len(lines) < line_start + item_nb:
        lines.append("")

    # Incruster chaque mot au début de la ligne correspondante
    i=0 # 
    index=line_start
    while i<item_nb:
        line = lines[index]
        item = items[i]
        print("z18 unicode True" if isinstance(item,unicode) else "z18 unicode False")
        print("z19 unicode True" if isinstance(line,unicode) else "z19 unicode False")
        lines[index] = item + line # Incruster au début
        index += 1
        i     += 1
        
    return "\n".join(lines)
    
#@wv_automat
def list_inlaid_suppr(script):
    """
    Supprime la colonne_incrustée* dans une string
    
    Args:
        script8 (str): sccript complet au format utf-8
    
    Return:
        str: script8 sans la colonne au format utf-8
    """
    
    line_start = script.find(CADRE_U[2]+SIGNATURE_INLAID)
    if line_start<0:
        return None
    line_end   = script.find(CADRE_U[3])
    line_lg=line_end-line_start+1
        
    if line_start==0: area1=""
    else:             area1 = script[0:line_start]
    line_end = script.find(CADRE_U[4])
    line_end = script.find("\n", line_end)
    if(line_end<0):
        area2 = script[line_start:]
        area3 = ""
    else:     
        area2 = script[line_start:line_end]
        area3 = script[line_end:]
    line_nb = area2.count('\n')
    
    # Expression régulière pour supprimer les N premiers caractères de chaque ligne
    pattern = ur"^.{%d}" % line_lg  # ^ = début de ligne, .{%d} = N caractères quelconques
    
    # Remplacement par une chaîne vide
    area2 = re.sub(pattern, "", area2, flags=re.MULTILINE)
    return (area1+area2+area3)

#________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________
#
#                                            S E R V I C E   D E  C O L O N N E _ I N C R U S T E E 
#________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________
class ColumnsInLaid(object):
    """Contrôleur principal pour colonne_incrustée*.
    Pilote le cycle de vie complet de la colonne
    Coordonne l'interaction entre :
    - La source de données (ColumnListSource)
    - L'interface utilisateur (_ColumnInlaidUI)
    
    Attributes:
        _ui (_ColumnInlaidUI): Gestionnaire d'interface
        _item_list (ColumnListSource): Source des données
        is_column_added (bool): État d'ajout de colonne
    """
    #________________________________________________________________________________________________________________________
    #
    #                                        C O N S T R U C T O R  - D E S T R U C T O R
    #________________________________________________________________________________________________________________________
    #@str__.wv_automat
    def __init__(self, list_source, ui_adapter):
        """Initialise le contrôleur avec ses dépendances.
        
        Args:
            list_source (ListColumnSource): Source des données à afficher
            ui_adapter (GenericUIRenderer): Adaptateur pour l'interface
        """
        sys_.instance_expected(list_source, ListColumnSource, "list_source", "ListColumnSource")
        sys_.instance_expected(ui_adapter, sys_.GenericUIRenderer, "ui_adapter", "GenericUIRenderer")
            
        self._ui   = _ColumnInlaidUI(ui_adapter)
        self._item_list = list_source
        self._load_initial_state()
        self.is_column_added = False
        
    def get_list(self):
        return self._item_list

   #------------------------------------------------------------------------------------------------------------------------
    #@str__.wv_automat
    def close_process(self):
        """Traitement de clotûre de l'invocation de Python
        Si une colonne_incrustée est présente :
        - soit est arrivée durent cette invocation : 
            elle reste, et les données -item, position - sont mémorisés
        - sinon elle est effacée, la mémorisation des données est vidée
        """
        # Referme les colonnes-incrustée*s (cadres incrustée*s)
        if self._ui.is_visible:
            if self.is_column_added:
                self._item_list.save()
            else:
                self.flush()
        
    def flush(self):
        """ Refermer la colonne
        1 - effacée du texte
        2 - liste-des-items supprimée
        """
        if not self._ui.is_visible: return
        
        self._ui.colinlaid_erase(self._item_list) 
        self._item_list.flush()      
    #________________________________________________________________________________________________________________________
    #
    #                                        A D D / S U P P R   C O L O N N E 
    #________________________________________________________________________________________________________________________
    def _load_initial_state(self):
        """1. Chargement initial si colonne existante"""
        #if self._item_list.has_saved_column():
        if not self._item_list.load(): 
            return
        self._ui.is_visible = True
     
    #@str__.wv_automat 
    def add_column(self, script):   
        """2.1 Ajout/suppression colonne"""
        self.flush()
 
        self._item_list.update(script)
        self._ui.draw(self._item_list)
        self.is_column_added = True
        
    def on_selection(self, car_position, action):  # TODO vérifier le type de context Il doit comporter get_car_position()
        """2.2 Gestion sélection item
        Gère la sélection d'un item dans la colonne.
        
        Args:
            car_position (int): Position du curseur
            action (Parser): Gestionnaire d'actions
            
        Returns:
            bool: True si l'action a été exécutée
        """
        line = self._ui.get_line_inlaid(car_position)
        if not line:
            return False
            
        # Efface la colonne_incrustée* dans Notepad 
        self.flush( )

        return action.column_selection_action(line.strip())


#________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________
#
#                                            D E S S I N A T E U R   D E   C O L O N N E _ I N C R U S T E E
#________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________
class _ColumnInlaidUI(object):
    """
    Gestionnaire privé des opérations d'interface utilisateur. Exemple : Notepad 
    
    Responsabilités:
    - Dessin des cadres
    - Gestion du positionnement
    - Interaction avec l'éditeur
    
    Attributes:
        is_visible (bool): État de visibilité
        _ui_adapter (GenericUIRenderer): Adapteur concret
    """
    #________________________________________________________________________________________________________________________
    #
    #                                        C O N S T R U C T O R  - D E S T R U C T O R
    #________________________________________________________________________________________________________________________
    #@str__.wv_automat
    def __init__(self, ui_adapter):
        """
        """
        self.is_visible = False
        self._ui_adapter = ui_adapter
    #________________________________________________________________________________________________________________________
    #
    #                                        A D D / S U P P R   C O L O N N E 
    #________________________________________________________________________________________________________________________
    @str__.wv_automat   
    def draw(self, item_list):
        """ 
        Ajoute une colonne-incrustée* dans une page de la view (ex : Notepad++ 
        """
        self.is_visible = True
        ui = self._ui_adapter
        scroll = ui.scroll_memo()
        
        # Affiche le fichier concerné dans Notepad
        item_list.open_page()
        
        # Récupère les infos de la page courrante de Notepad
        script  = ui.getText()
   
        line    = item_list.get_line_num() 
        
        ''' insère la colonne dans le texte. Note : dans string, la colonne se nomme 'liste' '''
        script = list_inlaid_add(line, item_list.get_title(), item_list.get_libelle(), script)

        # Inscrit le nouveau texte dans la page
        ui.setText(script)
        ui.scroll_restore(scroll)

        return self
    #------------------------------------------------------------------------------------------------------------------------
    #@str__.wv_automat
    def colinlaid_erase(self, item_list):
        ''' 
        Supprime une colonne-incrustée* dans une page
        '''
        self.is_visible = False
        ui = self._ui_adapter
        scroll = ui.scroll_memo() 
                
        ui.display_open_page(item_list.column_file)

        script = ui.getText()
        print("z31 '{}'".format(isinstance(script, unicode)))
        
        script = list_inlaid_suppr(script)
        print("z32 '{}'".format(isinstance(script, unicode)))
        ui.setText(script)
        
        ui.scroll_restore(scroll)

    def get_line_inlaid(self, pos):
        """
        Récupère la ligne pointé par le curseur-texte à l'interieur d'une colonne-incrustée, 
        retourne la ligne située entre les 2 traits verticaux du cadre
        Args:
            pos (int): Position de la recherche.
        Returns:
            str or None: La ligne de texte entre les marqueurs, ou None si les conditions ne sont pas remplies.
        Exemple:
    
        Notes:
            - Utilise la fonction 'list_inlaid_get_mark(script)' pour récupérer les marqueurs.
            - Vérifie que la position est bien entre les marqueurs avant d'extraire le texte.
        """ 
        if not self.is_visible:
            return None

        ui = self._ui_adapter
        
        #________________________________________
        # Récupère le numéro de la ligne (0-based)
        text = ui.getText()
        line_num = ui.line_num(pos)
        # Récupère le texte de cette ligne
        line_u = ui.getPosLine(line_num, text).strip()
        print(u"z33 '"+line_u+u"'")
        #________________________________________
        # Extrait la ligne à l'intérieur de la colonne reconverie en utf-8
        start = line_u.find(COL_INLAID_VERTICAL)
        if start<0: return None
        end   = line_u.find(COL_INLAID_VERTICAL, start+1)
        if end<0: return None
        # Vérifie que le curseur est dans le cadre
        col = str__.get_row_at(pos, text)
        if col<start or col>=end: return None 
        
        # Retourne la portion de ligne située dans le cadre
        return line_u[start+1:end]
