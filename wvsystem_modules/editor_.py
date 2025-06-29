# coding: utf-8
import time
import sys
import os 
import shutil
import subprocess
import re
import codecs
import glob 
from Npp import notepad, editor
# notepad.getFiles()  path, buffer_id, num-onglet[0-n], view[0-1]
# notepad.getCurrentBufferID()    
# notepad.getCurrentFilename()
#     os.path.dirname(chemin_complet)          # Chemin uniquement
# notepad.activateBufferID(int(file_info[1]))  # Activer temporairement la page
# notepad.activateFile(chemin_fichier) 

# editor.getText() 
# editor.getCurrentPos() 
# editor.setCurrentPos(position)
# 
# editor.gotoPos(min(cursor_pos, len(text_new)))
#    line = editor.lineFromPosition(result[0])
# editor.setFirstVisibleLine(line-5)
# editor.setSelection(debut, fin)
#   flags = 0  # 0 pour une recherche sensible à la casse; utilisez 4 pour insensible (SCFIND_MATCHCASE = 1, SCFIND_WHOLEWORD = 2, etc. si besoin)
#result = editor.findText(flags, startPos, endPos, word)
#   La méthode findText retourne un tuple (start, end) si trouvé, sinon None
import system             as sys_
import hot_const as val_
import string_ as str__
import column_inlaid as uni_
import file_ 
# TODO :getLineEndPosition
class NppAdaptater(sys_.GenericUIRenderer):
    def __init__(self):
        """  """
    '''__________________________'''
    ''' Texte '''    
    def getText(self):
        return editor.getText().decode("utf-8").replace(u'\r', u'')
    def setText(self, text):
        editor.setText(text.replace(u'\n', u'\r\n').encode("utf-8"))
    def getTextLength(self):
        return len(self.getText())
    def getCurrentPos(self):
        pos8  = editor.getCurrentPos()
        text8 = editor.getText()
        return str__._convert_pos_utf8_to_unicode(pos8, text8)
    def setCurrentPos(self, pos):
        editor.setEmptySelection(str__._convert_pos_unicode_to_utf8(pos, self.getText()))    
    def deleteRange(self, start, end) :   
        text = self.getText()
        text = text[0:start]+text[end:]
        self.setText(text)
    def getTextInOtherFile(self, file_path, page_is_restored):
        if page_is_restored:
            scroll = scroll_memo()   
        notepad_open(file_path)
        text = self.getText()
        if page_is_restored:
            scroll_restore(scroll)  
        return text 
    def setTextInOtherFile(self, text_new, file, page_is_restored):
        if page_is_restored:
            scroll = scroll_memo()   
        notepad_open(file_path)
        self.setText(text_new)
        if page_is_restored:
            scroll_restore(scroll)  
        
    '''_______'''   
    ''' Ligne '''
    def line_num(self, pos=None):
        if pos:
            return self.getText()[0:pos].count('\n')
            
        pos8  = editor.getCurrentPos()
        text8 = editor.getText()
        text  = text[0:pos8].decode("utf-8")
        
        return text.count('\n')
    def getPosLine(self, line_num, text):
        # retourne [position du 1er char de la ligne, le saut de ligne ("\n" ou "\r\n"), la longueur du saut de ligne (1 ou2 )]
        pos     = str__.find_newline_num( line_num, text)
        pos_end = text.find('\n', pos)
        print("z31 getPosline "+str(pos)+"  "+str(pos_end))
        if(pos_end<1): pos_end = len(text)
        return text[pos:pos_end]
        
    '''___________'''   
    ''' Selection '''
    def setSelection(self, start, end):
        text = self.getText()
        editor.setSelectionStart(str__._convert_pos_unicode_to_utf8(start, text))
        editor.setSelectionEnd  (str__._convert_pos_unicode_to_utf8(end,   text))
    def select_item(self, item, file_path):
        select_item(item, file_path)
    def select_file(self, start, end, path=None, view=None, line=-1):
        select_file(start, end, path, view, line)
    def select_item_in_file(self, item, file_path):
        select_item_in_file(item, file_path)
    def select_word_in_file(self, word, car_selector, file_path, view=None):
        select_word_in_file(word, car_selector, file_path, view)
    def select_word_in_user_files(self, word, car_selector, view=None):
        return select_word_in_user_files(word, car_selector, view)
    def getSelectionStart(self):
        text8 = editor.getText()
        pos8  = editor.getSelectionStart()
        return str__._convert_pos_utf8_to_unicode(pos8, text8)
    def getSelectionEnd(self):
        text8 = editor.getText()
        pos8  = editor.getSelectionEnd()
        return str__._convert_pos_utf8_to_unicode(pos8, text8)
    def getSelText(self):    
        text = editor.getSelText()
        if text == None or len(text) < 1: 
            return None
        else: 
            return str__.convert_to_unicode(text)
        
    '''______________________________________'''    
    ''' commande directe : sans modification '''        
    def getCurrentFilename(self):    
        return notepad.getCurrentFilename()
    def getFiles(self):
        return notepad.getFiles( )
    def grabFocus(self):
        editor.grabFocus()
    def getCurrentView(self):    
        return notepad.getCurrentView()
    def getCurrentBufferID(self):    
        return notepad.getCurrentBufferID()
    def getFirstVisibleLine(self):    
        return editor.getFirstVisibleLine()
    def open(self, file):
        notepad.open( file )
    def set_path_setting(self):
        set_path_setting()
    def list_func_py(self, expression):
        list_func_py(expression)
    def get_script_of_projet(self, list_iter, inc):
        get_script_of_projet(list_iter, inc)
    '''_______'''    
    ''' Hotword Tools '''        
    def scroll_memo(self):
        return scroll_memo()
    def scroll_restore(self, scroll):
        scroll_restore(scroll)
    def get_situation(self):
        return situation
    def read_situation(self,tab, start):
        """ mémorise la situation actuelle de Notepad++ """
        return situation.read(tab, start)

    def notepad_open(self, file_path, view=None):
        notepad_open(file_path, view)
    def display_open_at_pos(self, cursor, column_file):
        notepad_open_pos(cursor, column_file)
    def notepad_open_pos(self, pos, path, view=None, line=-1):
        notepad_open_pos(pos, path, view, line)
    def display_open_page(self, path):
        notepad_open(path)
    

ui = NppAdaptater()

if editor.getCodePage() != 65001:  # UTF-8
    console.write("Avertissement : encodage non UTF-8 !\n")

class NotepadSituation(object):
    #@str__.wv_automat
    def __init__(self):
        """ """
    def from_notepad(self):    
        """ command(*) """
        self.text           = ui.getText()
        self.cursor_pos     = ui.getCurrentPos()
        self.scroll_line    = ui.getFirstVisibleLine()
        self.view           = notepad.getCurrentView()
        self.file           = notepad.getCurrentFilename()
        self.item           = ui.getSelText()
        self.select_area    = [editor.getSelectionStart(), editor.getSelectionEnd()]
        return self
        
    def serializer(self):
        return "{}\n{}\n{}\n{}".format(\
            self.cursor_pos  ,\
            self.scroll_line ,\
            self.view        ,\
            self.file        );
            
    def read(self, tab, start):
        """ """        
        self.cursor_pos  = int(tab[start])
        self.scroll_line = int(tab[start+1])
        self.view        = int(tab[start+2])
        self.file        = tab[start+3]
        return self
            
situation = NotepadSituation().from_notepad()   

COLUMN_INSIDE_TEST = ["AAA","BBBB","CCCCC","DDDDDD"]
#************************************************************************************************************************
#************************************************************************************************************************
#                                       S T R I N G
#************************************************************************************************************************
#************************************************************************************************************************
#@str__.wv_automat
def get_word_of_cursor(): 
    """
    Extrait le mot sur lequel est placé le curseur
    """
    s = ui.getText()
    if s==None: return False
    cursor = ui.getCurrentPos()
    pos = str__.get_pos_word_at(cursor, s)
    if pos==None: return None
    #f str__.ON_DEBUG:#rint("editor_.py.get_word_of_cursor() : pos cursor="+str(cursor)+"  start="+str(pos[0])+"  end="+str(pos[1]))
    return s[pos[0]:pos[1]]

#@str__.wv_automat
def get_line_of_cursor():
    """
    Retourne la ligne comportant le curseur
    """
    s = ui.getText()
    if s==None: return None
    cursor = ui.getCurrentPos()
    return str__.get_line_at(cursor, s)
    
#@str__.wv_automat
def replace_text(pos, len_suppr, text_new):
   
    """
    Remplace une portion de texte dans l'éditeur Notepad++ à une position donnée.

    Args:
        pos (int): La position de début où la modification doit être effectuée.
        len_suppr (int): Le nombre de caractères à supprimer à partir de cette position.
        text_new (str): Le texte qui sera inséré à la place du texte supprimé.

    Returns:
        None

    Example:
        Supposons que l'éditeur contienne le texte suivant :
        
        "Bonjour le monde"
        
        Si `string_replace_in_vue(8, 2, "tout le")` est appelé, la phrase deviendra :
        
        "Bonjour tout le monde"

    Notes:
        - `editor.deleteRange(pos, len_suppr)` supprime `longueur` caractères à partir de `position`.
        - `editor.insertText(pos, text_new)` insère `text_new` à `position`, après suppression.
        - Si `pos` dépasse la longueur du texte dans l'éditeur, cela peut générer une erreur.
        - Si `len_suppr` est plus grand que le texte restant après `pos`, toute la partie sera supprimée.
    """
    pos = str__._convert_pos_unicode_to_utf8(pos)
    text_new8 = str__.convert_to_utf8(text_new)

    # Supprimer la portion de texte spécifiée
    editor.deleteRange(pos, len_suppr)

    # Insérer le nouveau texte à la position spécifiée
    if isinstance(text_new8, str) and len(text_new8)>0: editor.insertText(pos, text_new8)
        
def insert_line8():
    """
    Insère une ligne à la place de la ligne du curseur de Notepad++
    Position le curseur text au début de cette ligne
    """
    # Get the current cursor position
    current_pos = ui.getCurrentPos()
    text        = ui.getText()
    limits = str__.get_limits_of_line_at(current_pos, text)

    # Get the position at the start of the current line
    line_start_pos = limits[0]
    
    # Insert a newline character at the start of the current line
    editor.insertText(line_start_pos, '\n')
    
    # Optionally, move the cursor to the newly inserted blank line
    ui.setCurrentPos(line_start_pos)

def delete_current_line8():
    """
    Supprime une ligne du curseur de Notepad++
    Note : traitement pur 'editor' = Notepad++, donc en utf-8
    """
    # Get the current cursor position
    current_pos = editor.getCurrentPos()
   
    # Determine the current line number
    current_line = editor.lineFromPosition(current_pos)
    
    # Select the entire line
    line_start_pos = editor.positionFromLine(current_line)
    line_end_pos   = editor.getLineEndPosition(current_line)

    editor.setSelection(line_start_pos, line_end_pos)
    
    # Delete the selected line
    editor.deleteBack()

def get_script_of_projet(list_iter, inc):
    line = list_iter[0]
    if val_.doc_batch=="ALL_NOTEPAD" :
        """ Extrait le script de Notepad """
        notepad_open(list_iter[1][line])
        
        s = ui.getText()
        s1 = s.replace("\n","\\n")
    elif val_.doc_batch=="PYTHON" :
        """ Lecture du fichier """
        s = sys.io.read(list_iter[1][line])
    if inc: list_iter[0]+=1
    return s

def put_script_of_project(s):
    line = list_iter[0]
    if val_.doc_batch=="ALL_NOTEPAD" :
        """ Ecrit le script dans Notepad """
        notepad_open(list_iter[1][line])
        ui.setText(s) 
    elif val_.doc_batch=="PYTHON" :
        """ Ecriture du fichier """
        return write(s, list_iter[2][line])
        
#************************************************************************************************************************
#************************************************************************************************************************
#   #suppr:aaee                                    MODIFICATION DU CONTENU DE NOTEPAD
#************************************************************************************************************************
#************************************************************************************************************************
situation_stack = []
#@str__.wv_automat
def scroll_memo():
    return NotepadSituation().from_notepad()

def scroll_memo_push():
    s = NotepadSituation().from_notepad()
    situation_stack.append(s)
    return s

def scroll_memo_pop():
    if(len(situation_stack)<1):
        sys_.erreur("editor.py : pile de changement de page vide")
        return
    scroll_restore(situation_stack.pop())
    
#@str__.wv_automat
def scroll_restore(scroll):
    unfold_all()

    #suppr:
    print("//////////////////////////////")
    str__.print_dict(scroll)
    if(notepad.getCurrentFilename()!=scroll.file or (scroll.view and scroll.view!=notepad.getCurrentView())):
        notepad_open(scroll.file, scroll.view)
        editor.setCurrentPos(min(scroll.cursor_pos, editor.getTextLength()))
        editor.setFirstVisibleLine(scroll.scroll_line)
    else:
        if editor.getCurrentPos() != scroll.cursor_pos: 
            ui.setCurrentPos(min(scroll.cursor_pos, editor.getTextLength()))
        if editor.getFirstVisibleLine() != scroll.scroll_line:
            editor.setFirstVisibleLine(scroll.scroll_line)
    

# Index des datas retournés par "notepad.getFiles()"
ID_FILE_PATH = 0
ID_BUFFER_ID = 1
ID_TAB_NUM   = 2
ID_VIEW_NUM  = 3

# Situation d'un fichier et de la vue désiée
VIEW_ACTIVE   = 0   # fichier affiché dans la vue active
OTHER_VIEW    = 1   # fichier affiché uniquement dans l'autre vue, celle qui n'est pas active
TAB_ACTIVE    = 2   # fichier actid, en cours dédition
"""
def forcer_vue_1_si_absente():
    if vue_1_est_vide():
        console.write("🔧 Vue 1 vide, création d’un onglet...\n")
        # Créer un onglet vide dans la vue 1
        # Astuce : switch dans la vue 1 puis créer un fichier
        notepad.new()
        notepad.activateIndex(1, 0)  # Donne le focus à la vue 1
        console.write("✅ Vue 1 créée avec un onglet vide.\n")
    else:
        console.write("✅ Vue 1 déjà active avec %d onglet(s).\n" % notepad._get_nb_notepad_opens(1))
"""
#@str__.wv_automat
def notepad_open(file_path, view=None):
    """
    Ouvre le fichier spécifié dans Notepad++ pour l'éditer.
    Si le fichier n'est pas déjà ouvert, il sera chargé.
    
    :param file_path: Chemin complet du fichier.
    :param view: (optionnel) Numéro de vue.
    
    return:
        list: description d'onglet [fichier, id-buffer, num-onglet, num_view]
    """
    print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
    if isinstance(file_path, unicode):  # Vérifie si c'est une chaîne Unicode
        file_path = file_path.encode("utf-8") 
    
    # Récupère les onglet correspondants au fichier.
    # VIEW_ACTIVE = 0 - onglet non actif + view active, 
    # OTHER_VIEW  = 1 - onglet non actif + view non active, 
    # TAB_ACTIVE  = 2 - onglet actif 
    file_tabs = _get_tabs_of( file_path, view ) 
    #________________________________________ 
    # Onglet actif
    if file_tabs[TAB_ACTIVE]:
        return file_tabs[TAB_ACTIVE]
    #________________________________________
    # view active
    file_active_view = file_tabs[VIEW_ACTIVE]
    if file_active_view:
        notepad.activateIndex(file_active_view[ID_VIEW_NUM], file_active_view[ID_TAB_NUM])        
        return file_active_view
    #________________________________________
    # view non active
    file_other_view = file_tabs[OTHER_VIEW ]
    if file_other_view:
        print("kkkkkmmmm")
        if view==None: 
            notepad.activateIndex(file_other_view[ID_VIEW_NUM], file_other_view[ID_TAB_NUM])
            return file_other_view
        if notepad.getCurrentView()!=view:
             # Se placer dans l'autre vue et ouvrir le fichier
            notepad.activateIndex(notepad.getCurrentView(), file_other_view[ID_TAB_NUM])
        _move_to_view(file_other_view)
        
        #notepad.activateIndex(file_other_view[ID_VIEW_NUM], file_other_view[ID_TAB_NUM])
        return [file_path,notepad.getCurrentBufferID(),-1, view]
    
    #________________________________________    
    # Vérifier que le fichier existe sur le disque
    if not os.path.exists(file_path):
        print("File do not exists :\n" + file_path, "Erreur")
        return None

    # Activer la vue souhaitée
    if view:
        current_view = notepad.getCurrentView()
        if current_view != view:
            #notepad.switchView()  # Se positionner dans la bonne vue
            notepad.activateIndex(view, 0)        
        # Charge et ouvre le fichier
        if view==1 and _get_nb_notepad_opens(1) == 0:
            notepad.new()
            notepad.activateIndex(1, 0)
        notepad.activateIndex(1, 0)
    notepad.open(file_path)    # Ouvre le fichier dans la vue active
    return _get_file_active()[VIEW_ACTIVE]

def select_item_in_file(item, file_path):
    """
    Recherche un item dans un fichier
    L'affiche, puis sélectionne l'item
    Args:
        item (str): string à rechercher.
        file_path (str): Chemin complet du fichier.
        view (int): nom du fichier, 
    Returns:
        bool: True si la sélection est effectuée
              False si absent
    
    """ 
    #suppr:
    print("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")
    print(item)
    notepad_open(file_path)
    
    result = editor.findText(0, 0, editor.getTextLength(), item)
    if not result:
        return False
    select_file(result[0], result[1])
    return True
    
def select_word_in_user_files(word, car_selector, view=None):
    # Recherche dans les scripts_utilisateurs*   
    script_iter = file_.get_scripts_of_project()
    for f in script_iter[1] :
        if select_word_in_file(word, car_selector, f):
            return True
        
    return False

def select_word_in_file(word, car_selector, file_path, view=None):
    """
    Dans le fichier, selectionne le mots-suivi-de-carselector
    Si absent, return False
    Args:
        word (str): Le mot à chercher, qui doit être suivi de "(*)".
        car_target (str): caratère pour distinguer le mot parmis les autres présents dans les fichiers. Ex "(*)".
                    si car_target = vide (""), le mot sera recherché 
        file_path (str): Chemin complet du fichier.
        view (int): numéro de vue qui affichera le fichier
                    si absent, le fichier s'affichera dans sa vue actuelle
    Returns:
        bool: True si la sélection est effectuée
              False si absent
    """
    notepad_open(file_path, view)
    text = ui.getText()

    # Rechercher la position du premier mot exact suivi de "(*)" dans le texte.
    motif = r'\b' + re.escape(word) + re.escape(car_selector)
    match = re.search(motif, text)
    #suppr
    print("___________select_word_in_file()_____________")
    print(file_path)
    print("match car_selector '"+car_selector+"'")
    print("motif : '"+motif+"'")
    print("---------------------------------------------")
    if not match : return False    

    # Sélectionner le texte du lexique 
    editor.setSel(match.start(), match.end())
    
    # Positionne l'ascenseur
    select_file(match.start(), match.end()) 
    return True

#________________________________________________________________________________________________________________________
#
#                                       T O O L S
#________________________________________________________________________________________________________________________    
def _move_to_view(tab_org):
    try:
        view_org = tab_org[ID_VIEW_NUM]
        view_dest = 1 - view_org
        
        # Vérifier qu'on est dans la vue_org
        if notepad.getCurrentView() != view_org:
            notepad.activateIndex(view_org, tab_org[ID_TAB_NUM])

        # Sauvegarder l'état actuel
        scroll=scroll_memo()
        scroll.view = view_dest;
        
        # 1. Fermer le fichier dans la vue org
        notepad.close()

        # 2. Basculer en vue dest
        notepad.activateIndex(view_dest, 0)

        # 3. Rouvrir le fichier
        notepad.open(tab_org[ID_FILE_PATH])
        scroll_restore(scroll)
        print("Fichier déplacé vers la vue "+str(view_dest), "Succès")

    except Exception as e:
        print("Erreur : {}".format(str(e)))
        return False
    

def _get_nb_notepad_opens(view):
    tabs = notepad.getFiles()
    nb = 0;
    for t in tabs:
        if t[ID_VIEW_NUM]==view: nb+=1
    return nb

#@str__.wv_automat
def _get_file_active(view=None):
    """
    Fournit le fichier actif dans Notepad++
    Ainsi que le même fichier dans l'autre vue si il est présent
    returns: 
        list: 2 descriptions d'onglets
            [onglet-actif/None, onglet de l'autre-vue/None]
            Pour chaque onglet paramètre du contenu 
            - onglet[][0] (str): chemin complet du fichier
            - onglet[][1] (int): identifiant du buffer
            - onglet[][2] (int): numéro d'onglet [0-n]
            - onglet[][3] (int): numéro de vue [0-1]
    """
    tabs          = notepad.getFiles()
    buffer_active = notepad.getCurrentBufferID()
    if not view: view = notepad.getCurrentView()
    
    files_active   = [None,None]
    for t in tabs:
        if t[ID_BUFFER_ID] == buffer_active:
            if t[ID_VIEW_NUM]==view: files_active[VIEW_ACTIVE]=t
            else:                     files_active[OTHER_VIEW ]=t
            
    return files_active 
    
def _get_tabs_of(file_path, view=None):
    """
    Fournit les onglets correspondants à ce fichier dans un tableau à 3 cases
    [onglet_actif, onglet_view_active, onglet_view_inactive]
    Si un des onglet est actif, il ets 
    returns: 
        list: 2 descriptions d'onglets
            [onglet-actif/None, onglet de l'autre-vue/None]
            Pour chaque onglet paramètre du contenu 
            - onglet[][0] (str): chemin complet du fichier
            - onglet[][1] (int): identifiant du buffer
            - onglet[][2] (int): numéro d'onglet [0-n]
            - onglet[][3] (int): numéro de vue [0-1]
    """
    file_path = os.path.normcase(file_path)
    tabs          = notepad.getFiles()
    buffer_active = notepad.getCurrentBufferID()
    if view==None: view   = notepad.getCurrentView()

    file_tabs   = [None,None,None]
    for t in tabs:
        if os.path.normcase(t[ID_FILE_PATH]) == file_path:
            if t[ID_BUFFER_ID] == buffer_active:
                if t[ID_VIEW_NUM]==view: file_tabs[TAB_ACTIVE ]=t
                else                    : file_tabs[OTHER_VIEW ]=t
            else:                                
                if t[ID_VIEW_NUM]==view: file_tabs[VIEW_ACTIVE]=t
                else:                     file_tabs[OTHER_VIEW ]=t
    return file_tabs

#************************************************************************************************************************
#************************************************************************************************************************
#                                       MODIFICATION DE PRESENTATION DE NOTEPAD
#************************************************************************************************************************
#************************************************************************************************************************

# Mémoire globale (valable tant que la session PythonScript est active)
saved_position = {}

#@str__.wv_automat
def select_item(item, file):
    ''' Recherche un item dans notepad, puis le sélectionne '''
    # Recherche la position de l'item
    notepad.activateFile(file)
    s = ui.getText()
    pos = str__.find_1st(item, s)
    print(" z2 ")
    if pos<0: return False

    print(" z3 ")
    # selectionne le texte pour positionne l'ascenseur
    select_file(pos, pos+len(item))
    return True

def notepad_open_pos(pos, path, view=None, line=-1):
    """
    Ouvre un fichier dans Notepad++
    puis positionne le curseur. 
    Note: si les fichier est déjà présent dans Notepad++, il n'est pas rechargé
    """
    # Si le fichier est indiqué. Sinon, nous travaillons sur le fichier en cours d'édition
    if path:
        #suppr:
        print("########")
        print(path)
        notepad_open( path, view )
    #Déplace le curseur
    text = ui.getText()
    if pos < len(text):
        pos8 = str__._convert_pos_unicode_to_utf8(pos, text)  
    else: 
        pos8 = len(editor.getText())-1
    editor.setEmptySelection(pos8)

    # Positionner l'ascenseur
    # Déplier tous les paragraphs. Sinon Notepad retourne un mauvais numéro de ligne
    unfold_all()
    if line < 0:
        line = editor.lineFromPosition(pos8)-5        
    editor.setFirstVisibleLine(line)
    
def select_file(start, end, path=None, view=None, line=-1):
    """
    Sélectionne un zone de texte dans Notepad++
    """
    if path:
        notepad_open( path, view )
    #suppr:
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@editor.py\nstart = {}, end = {}".format(start, end))
    sys_.ui.setSelection(start, end) 
    ui.setCurrentPos(end)
    unfold_all()
    if line < 0:
        line = editor.lineFromPosition(end)-5        
    editor.setFirstVisibleLine(line)

        
def insert_lines_below(lines):
    """
    Insère une ou plusieurs lignes juste en dessous de la ligne du curseur,
    sans toucher au contenu de la ligne actuelle.
    Note : traitement pur 'editor' = Notepad++, donc en utf-8
    """
    lines8 = '\r\n' + str__.convert_to_utf8(lines)
    # Récupère le numéro de la ligne actuelle
    current_line = editor.lineFromPosition(editor.getCurrentPos())
    
    # Récupère la fin de cette ligne (début de la ligne suivante)
    position_insertion = editor.getLineEndPosition(current_line)
    sys_.error("editor.py/insert_lines_below() TODO editor.getLineEndPosition()")
    
    # Ajoute un saut de ligne, puis insère les lignes
    editor.insertText(position_insertion, lines8)
    
def insert_lines_above(lines):
    """
    Insère une ou plusieurs lignes juste au-dessus de la ligne du curseur,
    sans modifier son contenu.
    """
    current_line = editor.lineFromPosition(editor.getCurrentPos())
    insert_pos = editor.positionFromLine(current_line)
    
    #text = '\r\n'.join(lines) + '\r\n'
    text = str__.convert_to_utf8(lines) + '\r\n'
    editor.insertText(insert_pos, text)
    
'''________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________'''
#@str__.wv_automat
def active_file_in_vue(file_path, vue_id):
    """
    Active un fichier dans une vue de notepad++
    Note: Traitement pur 'notepad', donc en utf-8
    Note : si absent, le fichier n'est pas chargé dans notepad++
    :param file_path: chemin complet du fichier à activer
    :param vue_id: vue de notepad++ qui recevra le fichier
    :return: non 
    """
                    # Vérifier si la vue numéro passée est valide (0 ou 1)
    if vue_id not in [0, 1]:
        print("***Error*** Numéro de vue invalide. Utilisez 0 pour Vue 1 ou 1 pour Vue 2.")
        return
                    # Obtenir la vue actuelle
    current_view = notepad.getCurrentView()
                    # Liste des files dans les deux vues
    view1_files = notepad.getFiles(0)  # Liste des fichiers dans la vue 1
    view2_files = notepad.getFiles(1)  # Liste des fichiers dans la vue 2
                    # Déterminer dans quelle vue se trouve le fichier
    if vue_id == 0:
                    # Vue 1
        files_in_target_view = view1_files
    else:           # Vue 2
        files_in_target_view = view2_files
                    # Vérifier si le fichier est ouvert dans la vue cible
    is_file_in_target_view = any(file[0] == file_path for file in files_in_target_view)

    if not is_file_in_target_view:
        print("***Error*** Le fichier '{}' n'est pas ouvert dans la vue {}.").format(file_path,vue_id + 1)
        return
                    # Si le fichier est déjà dans la vue spécifiée, ne rien faire
    if current_view == vue_id:
        print("***Error*** Le fichier '{}' est déjà actif dans la vue {}.").format(file_path,vue_id + 1)
        return
                    # Basculer vers la vue spécifiée
    notepad.setCurrentView(vue_id)
                    # Activer la page du fichier dans la vue spécifiée
    for file in files_in_target_view:
        if file[0] == file_path:
            notepad.activateFile(file_path)
            #rint("Le fichier '{}' est maintenant actif dans la vue {}.").format(file_path,vue_id + 1)
            break
            
#************************************************************************************************************************
#************************************************************************************************************************
#                                       F I C H I E R
#************************************************************************************************************************
#************************************************************************************************************************
#@str__.wv_automat
def save_notepad_files_in_list(files):
    """
    Sauvegarde tous les fichiers spécifiés dans le tableau 'fichiers'.
    Si le fichier est ouvert dans Notepad++, il sera sauvegardé.
    
    Paramètre:
    fichiers (list) : Liste de chemins de fichiers à sauvegarder.
    """
    try:
        for file_path in files:
            # Vérifie si le fichier est déjà ouvert dans une page
            for i in range(notepad.getNbFiles()):
                # Récupère le chemin du fichier ouvert dans chaque page
                filename = notepad.getFileName(i)
                
                if filename == file_path:
                    # Si le fichier est ouvert, on l'active et on le sauvegarde
                    notepad.activateFile(i)  # Active la page
                    notepad.menuCommand("File", "Save")  # Sauvegarde le fichier
                    #rint("Le fichier {} a été sauvegardé.").format(file_path)
                    break
            else:
                print("***Error*** Le fichier {} n'est pas ouvert.").format(file_path)
    finally:
        # Restaure le buffer original quoi qu'il arrive
        notepad.activateBuffer(original_buffer)
    
def get_text_of_file(file_name) : 
    """
    Retourne le texte d'un fichier.
    Balaye tous les dossiers
    """
    file_path=file_.get_Path_of_filename(file_name)
    if not file_path: return None

    notepad_open(file_path)
    return ui.getText()

def get_file_of_alias(alias, text):
    """
    Retourne le texte du fichier de alias indiqué en paramètre 
    """
    # Rechercher le nom de ficher
    pos_def = text.find( alias )
    words = str__.list_words_in_line(pos_def, text)
    if words[0]!="import": return None
    
    # Construit le chemin complet du fichier
    # Qui est dans le même dossier que le fichier 'appelant'
    file_path = notepad.getCurrentFilename()
    path = os.path.dirname(file_path)          
    return path+os.sep+words[1]+".py"
#@str__.wv_automat    
def list_func_py(command): 
    """ Place les fonctions d'un fichier .py dans un tableau """
    # Si le point n'est pas précédé de mot => rechercher la fonction 'py' dans le ttexte édité dans Notepad
    # + supprimer le '.'
    
    # Recherche le fichier destination, puis retourne le texte
    text = command.text
    if command.item=="self":
        scroll = None
    else:
        scroll = scroll_memo() 
        
        # Rechercher le ficher
        pos_def = text.find( command.item )
        words = str__.list_words_in_line(pos_def, text)
        if words[0]!="import": return None
        file = val_.SYSTEM_MODULES_PATH+words[1]+".py"
        
        # Recupère le texte du fichier recherché
        notepad.open(file)
        text = ui.getText()
        
    #lister les fonction du script destination
    funcs_py = str__.get_functions_by_def(text)
    if scroll: scroll_restore(  scroll  )
    
    if len(funcs_py)<1: return None
    return sorted([py[py.find("def"):] for py in funcs_py])   

def get_text_of_alias(alias, text):
    """
    Retourne le texte du fichier de alias indiqué en paramètre
    En entré : le 
    """
    # Rechercher le ficher
    pos_def = text.find( alias )
    words = str__.list_words_in_line(pos_def, text)
    print(" z20 "+words[0]+"  "+words[0])
    if words[0]!="import": return None
    return get_text_of_file(words[1]+".py")

def walk_path_var( path_var ):
    """ Avance d'une étape dans le chemmin d'une variable
    En entrée : le fichier en-cours est édité
        Note: aucune position n'est en-cours
    """
    
    ''' Recherche l'import ou la variable calée à gauche'''
    scroll_memo_push()
    path = str__.reverse_list()
    
    flag_start = True
    for name in path:
        if flag_start:
            flag_start = False
            file_name = str__.get_import(name, text)
            if file_name:
                io.open_file(file_name+".py")
                text = ui.getText()
                continue
        walk_step_var(name, text, "")    
    scroll_memo_pop()

def walk_step_var(pos, name, text):
    # Rechercher la position du nom dans le texte 
    pos = str__.get_pos_of_item_started_line(name,text)
    
    # L'item le chemin est erroné
    if pos == None: 
        sys_.erreur("Mauvais départ pour le chemin de variable ")
        return None
        
    # recherche '='
    pos_egal = text.find('=', pos[0], pos[2])
    limit_line = get_limits_of_line_at(pos, text)
    formule = text[pos_egal+1: limit_line[1]].strip()
    
    # lire le path : ui=sys_.var / ui=var
    
#************************************************************************************************************************
#************************************************************************************************************************
#                                       C O M M A N D E S    W V - H O T - W O R D
#************************************************************************************************************************
#************************************************************************************************************************
#@str__.wv_automat
def set_path_setting(unused): #pth
    chemin = os.path.dirname(notepad.getCurrentFilename())
    file_.write_item_dictionary(chemin,val_.SET_PATH_USER,val_.SYSTEM_SETTING_FILE)


def unfold_all():
    total_lines = editor.getLineCount()
    for i in range(total_lines):
        if not editor.getLineVisible(i + 1):
            editor.foldLine(i, 1)  # 1 = déplier


