C:\Users\33684\AppData\Roaming\Notepad++\plugins\Config\PythonScript\scripts
    (ci-dessus : chemin vers le dossier de travail)

py <- pour reconstituer cette librairie, cliquez sur 'py!' + exécutez WvHotWord (Alt+W)

#\wvsystem_modules\column_inlaid.py
def __init__(self, list_source, ui_adapter):
def __init__(self, list_source, ui_adapter):
def _draw_frame(title, tabOrg):
def _list_insert_at_start_line(line_start, text, items ):
def _load_initial_state(self):
def add_column(self, script):
def close_process(self):
def colinlaid_erase(self, item_list):
def debug(self):
def draw(self, item_list):
def flush(self):
def flush(self):

def get_line_inlaid(self, pos):
def get_line_num(self):
def get_list(self):

def list_inlaid_add(line_start, title, tabOrg, script):
def list_inlaid_suppr(script):
def load(self):
def on_selection(self, car_position, action):
def open_page(self):
def save(self):
def update(self, s):

#\wvsystem_modules\column_list_handler.py
def __init__(self, io_adapter, ui_adapter):
def __init__(self, io_adapter, ui_adapter):
def __init__(self, io_adapter, ui_adapter):
def column_list_init(hot_parser, io_adapter, ui_adapter):
def column_selection_action( self, line ):
def debug(self):
def flush(self):
def get_command(self, item):

def get_line_num(self):

def load(self):

def parse(self, item):
def parser(self, hot_parser):
def save(self):
def serialize_to_file(self):
def set_items(self, tab, start):
def update(self, s):

#\wvsystem_modules\editor_.py
def __init__(self):
def __init__(self):
def _get_file_active(view=None):
def _get_nb_notepad_opens(view):
def _get_tabs_of(file_path, view=None):
def _move_to_view(tab_org):
def active_file_in_vue(file_path, vue_id):
def deleteRange(self, start, end) :
def delete_current_line():
def display_open_at_pos(self, cursor, column_file):
def display_open_page(self, path):
def forcer_vue_1_si_absente():
def from_notepad(self):
def getCurrentBufferID(self):
def getCurrentFilename(self):
def getCurrentPos(self):
def getCurrentView(self):
def getFiles(self):
def getFirstVisibleLine(self):
def getPosLine(self, line_num, text):
def getSelText(self):
def getSelectionEnd(self):
def getSelectionStart(self):
def getText(self):
def getTextInOtherFile(self, file_path, page_is_restored):
def getTextLength(self):
def get_file_of_alias(alias, text):
def get_line_of_cursor():
def get_script_of_projet(list_iter, inc):
def get_situation(self):
def get_text_of_alias(alias, text):
def get_text_of_file(file_name) :
def get_word_of_cursor():
def grabFocus(self):
def insert_line():
def insert_lines_above(lines):
def insert_lines_below(lines):
def line_num(self, pos=None):
def list_func_py(command):
def notepad_open(file_path, view=None):
def notepad_open_pos(pos, path, view=None, line=-1):
def open(self, file):
def positionFromLine(self, line_num, text):
def put_script_of_project(s):
def read(self, t, start):
def replace_text(pos, len_suppr, text_new):
def save_notepad_files_in_list(files):
def scroll_memo(self):
def scroll_memo(self):
def scroll_memo_pop():
def scroll_memo_push():
def scroll_restore(self, scroll):
def scroll_restore(self, scroll):
def select_file(start, end, path=None, view=None, line=-1):
def select_item(item, file):
def select_item_in_file(item, file_path):
def select_word_in_file(word, car_selector, file_path, view=None):
def select_word_in_user_files(word, car_selector, view=None):
def serializer(self):
def setCurrentPos(self, pos):
def setSelection(self, start, end):
def setText(self, text):
def setTextInOtherFile(self, text_new, file, page_is_restored):
def set_path_setting(unused):
def suppr_signwv(hot_command):
def unfold_all():

#\wvsystem_modules\file_.py
def SearchFolderFree(pathCurr, prefix):
def __init__(self):
def _get_path_of_folder(setting_name, file_name, path_org):
def backup_files_(file_pathes, base_directory, folder_name):
def backup_js(file_paths, sub_foldee):
def copy_file(file_path, destination_path):
def copy_files_to_subfolder(file_paths, subfolder_name):
def error_(name):
def files_equal(file_path1, file_path2):
def get_Path_of_filename(file_name) :
def get_scripts_of_project():
def get_setting(key):
def init_setting():
def is_in_file_list(value, file_path):
def load(self, file_path, exists_optionel=False):
def make_dirs(folder, message):
def message_(name):
def read(file_path, exists_optionel=False):
def read_citation(name, file):
def read_citation_langage(name, file_path):
def read_dictionary(file_path):
def read_error(nom):
def read_file_langage(file_path):
def read_item(param_name, file_path):
def read_langage():
def read_list(file_path):
def read_list_typed(file_path):
def read_message(nom):
def read_setting(key):
def save(self, datas, file_path):
def suppr_file(file_path):
def write(datas, file_path):
def write_dictionary(dico, file_path):
def write_item_dictionary(value, key, file_path):
def write_list(tab, file_path):
def write_list_typed(liste, file_path):
def write_setting(value, key):

#\wvsystem_modules\hot_commands.py
def _car_exec(expression):
def activate_command(unused):
def clean_clipboard(expression):
def colinlaid_suppr_all(context):
def copy_member(expression):
def dot_command_after( expression ):
def dot_command_before( expression ):
def goto(word):
def goto_body(aa):
def goto_hot_word0(unused):
def goto_hot_word1(unused):
def goto_hot_word2(unused):
def goto_hot_word3(unused):
def hotname_exec(expression):
def inhib_command(unused):
def init_copy_member(expression):
def list_func_py_(command):
def list_menu(expression):
def open_hotword_doc(unused):
def open_py_file(unused):
def print_help(unused):
def reinit_project(expression):
def select_error(line):
def select_menu(line):
def zzz_(): print("zzz_ :

#\wvsystem_modules\hot_goto.py
def __init__(self):
def _goto_glossary(command):
def _goto_if_function_py(command):
def _pos_goto(self, pos):
def display_next(unused=None):
def display_pos_rewind(message):
def functions_py_build_path(pos, script):
def goto_file_function_py(item):
def goto_function_def(cursor, s):
def goto_function_from_list_py():
def goto_glossary(command):
def init_search_by_step( item ):
def init_search_word_by_step( command ):
def list_attrs(name):
def list_function_names_sorted(text, ln):
def list_functions_py(unused=None):
def pos_add(self):
def pos_is_curr(self, pos):
def pos_next(self):
def pos_previous(self):
def pos_rewind_next(unused):
def pos_rewind_next_clip(unused):
def pos_rewind_previous(unused=None):
def pos_rewind_previous_clip(unused):
def pos_save(self):
def search_in_file(item, file, t):
def select_function_declaration_py_(item, start, text):
def select_item_in_system_file(item, file_name):
def to_script(self):

#\wvsystem_modules\hot_parser.py
def __init__(self):
def _parse_cursor_after_formula(self, pos_parser):
def _parse_from_end(self, pos_parser):
def _parser_selection(self, s):
def _print_debug(self):
def add_listener(self, listener):
def extern_parsers_exec(self):
def get_clipboard_hotword(self):
def get_formula(self):
def hot_parser(self):
def hotword_in_clipboard(self):
def init_tabs(self, cars_before, cars_after, cars_unic, items_command, COMMANDS_EDITION):
def item_absent(self):
def parse_signs(self):
def parser(self):
def selection_multi_spaces(self):
def suppr_formula(self):
def suppr_pointers(self, pos, nb):
def suppr_sign(self):

#\wvsystem_modules\hot_parser_debug.py
def __init__(self, text, expected_key_command, expected_item, expected_edit, expected_formula, label):
def _debug_parse_cursor(self, cursor, script):
def _debug_parse_selection(self, start, end, script):
def check_result(self, command, script):
def debug(cars_before, cars_after, cars_unic, items_command, COMMANDS_EDITION):
def hotword_debug_batch(self, i):
def lg_(n, s,separ):
def parse(self, text):

#\wvsystem_modules\project_.py
def _project_init():
def debug_invocation():
def play_invocation():
def project_close():
def project_init():

#\wvsystem_modules\string_.py
def _car_is_name(c):
def _convert_pos_unicode_to_utf8(pos_u, text_u):
def _convert_pos_utf8_to_unicode(pos_utf8, text_utf8):
def clean_clipboard():
def couper_au_deuxieme_saut_de_ligne(chaine):
def display_dictionary(tab):
def display_function_deep(margin, name, args, doc):
def errorwv(message):
def fc__():
def find_1st(word, text):
def find_all(item, text):
def find_newline_num( num, text):
def find_word(item, text):
def get_clipboard():
def get_functions_by_def(script_text):
def get_import_name(start, text):
def get_line_at(pos, text):
def get_ln(text):
def get_limits_of_line_at(pos, text):
def get_pos_start_name(text):
def get_pos_word_at(pos, text):
def get_row_at(pos, text):
def get_word_at(pos, text):

def join_two_arrays(tab0, tab1, separ1, separ2):
def lines_to_dict(text):
def list_words_in_line(pos, text):
def parse_function(texte, pos, len_max):
def parse_lines_to_dict(text, separ_key):
def parse_text_to_dict(text, separ_line, separ_key):
def print_class(elem, margin):
def print_dict(dico):
def print_stack():
def remove_accents(text):
def set_clipboard(text):
def split_columns_to_arrays(text, separ_item, separ_line):
def split_lines_to_arrays(text, separ=None):
def str_to_dict(text, separ_line):
def str_to_type( value ):
def to_list_str( tab ):
def to_type_str(value):
def wrapper(*args, **kwargs):
def wrapper(*args, **kwargs):
def wv_automat(fonction):
def wv_automat_(fonction):

#\wvsystem_modules\system.py
def display_open_at_pos(self, cursor, column_file):
def display_open_page(self, path):
def error(id_,message):
def getPosLine(self, line_num):
def getText(self):
def instance_expected(var, type, var_name, type_name):
def line_num(self, pos):
def load(self, datas, file_path):
def save(self, datas, file_path):
def scroll_memo(self):
def scroll_restore(self, scroll):
def setTextInOtherFile(self, script):
def warning(id_, message):