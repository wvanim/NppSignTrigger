io = None
ui = None

class GenericIo( object ):
    """ """
    def save(self, datas, file_path):
        raise NotImplementedError
    def load(self, datas, file_path):
        raise NotImplementedError
    def read_citation_langage(self, file_path ):    
        raise NotImplementedError
    def init_setting(self):
        raise NotImplementedError
    def get_setting(self):
        raise NotImplementedError
    def message_(self, name):
        raise NotImplementedError
    def write_item_dictionary(self, value, key, file_path):
        raise NotImplementedError
    def read_list(self, file_path):
        raise NotImplementedError
    def write_list(self, tab, file_path):
        raise NotImplementedError
    def write_dictionary(self, dico, file_path):
        raise NotImplementedError
    def get_scripts_of_project(self):
        raise NotImplementedError
    def read_item(self, param_name, file_path):
        raise NotImplementedError
        
class GenericUIRenderer( object ):
    """ """
    def getText(self):
        raise NotImplementedError
    def setText(self, text):
        raise NotImplementedError
    def getTextLength(self):
        raise NotImplementedError
    def getCurrentPos(self):
        raise NotImplementedError
    def setCurrentPos(self, pos):
        raise NotImplementedError
    def deleteRange(self, start, end) :   
        raise NotImplementedError
    def getTextInOtherFile(self, file_path, page_is_restored):
        raise NotImplementedError
    def setTextInOtherFile(self, text_new, file, page_is_restored):
        raise NotImplementedError        
    '''_______'''   
    ''' Ligne '''
    def line_num(self, pos=None):
        raise NotImplementedError
    def getPosLine(self, line_num, text):
        raise NotImplementedError
    '''___________'''   
    ''' Selection '''
    def setSelection(self, start, end):
        raise NotImplementedError
    def select_item(item, file_path):
        raise NotImplementedError
    def select_file(start, end, path=None, view=None, line=-1):
        raise NotImplementedError
    def select_item_in_file(item, file_path):
        raise NotImplementedError
    def select_word_in_file(word, car_selector, file_path, view=None):
        raise NotImplementedError
    def select_word_in_user_files(word, car_selector, view=None):
        raise NotImplementedError
    def getSelectionStart(self):
        raise NotImplementedError
    def getSelectionEnd(self):
        raise NotImplementedError
    def getSelText(self):    
        raise NotImplementedError
    '''______________________________________'''    
    ''' commande directe : sans modification '''        
    def getCurrentFilename(self):    
        raise NotImplementedError
    def getFiles(self):
        raise NotImplementedError
    def grabFocus(self):
        raise NotImplementedError
    def getCurrentView(self):    
        raise NotImplementedError
    def getCurrentBufferID(self):    
        raise NotImplementedError
    def getFirstVisibleLine(self):    
        raise NotImplementedError
    def open(self, file):
        raise NotImplementedError
    def set_path_setting():
        raise NotImplementedError
    def list_func_py(expression):
        raise NotImplementedError
    def get_script_of_projet(list_iter, inc):
        raise NotImplementedError
    '''_______'''    
    ''' Hotword Tools '''        
    def scroll_memo(self):
        raise NotImplementedError
    def scroll_restore(self, scroll):
        raise NotImplementedError
    def get_situation(self):
        raise NotImplementedError
    def notepad_open(file_path, view=None):
        raise NotImplementedError
    def display_open_at_pos(self, cursor, column_file):
        raise NotImplementedError
    def display_open_page(self, path):
        raise NotImplementedError
    
    def read_situation(tab, start):
        raise NotImplementedError
    def get_situation():
        raise NotImplementedError

def error(id_,message): 
    raise Exception("***ERROR*** "+message)
    
def warning(id_, message):    
    print("***ERROR*** "+message)

def instance_expected(var, type, var_name, type_name):
    if not isinstance(var, type):
        raise Exception(var_name+" : data_source is not "+type_name)
