# coding: utf-8

import os
import re
import errno
import codecs
import shutil
import subprocess
import glob

import system             as sys_
import hot_const          as val_
import string_            as str__


# os.sep
# os.path.basename(file_path)
# os.path.dirname(file_path)+os.sep     
# os.path.isfile(file_path)
# os.path.normcase(file_path1)
# os.remove(file_path)
# os.makedirs(folder)
# os.path.join(pathCurr, "{}{}".format(prefix,i))
# os.path.exists(folder_name)
# os.path.dirname(file_paths[0])


def convert_to_unicode(text):
    return str__.convert_to_unicode(text) if text else text
def convert_to_utf8(text):
    return str__.convert_to_utf8(text) if text else text


class FileIO(sys_.GenericIo):
    def __init__(self):
        """ """
    def save(self, datas, file_path):
        write(datas, file_path)
    def load(self, file_path, exists_optionel=False):
        return convert_to_unicode(read(file_path, exists_optionel))
    def read_citation_langage(self, name, file_path ):    
        return convert_to_unicode(read_citation_langage(name, file_path )  )
    def init_setting(self):
        return init_setting()
    def get_setting(self, name):
        return convert_to_unicode(get_setting(name))
    def message_(self, name):
        return message_(name)
    def write_item_dictionary(self, value, key, file_path):
        write_item_dictionary(str__.convert_to_utf8(value), str__.convert_to_utf8(key), file_path)
    def read_list(self, file_path):
        read_list(file_path)
    def write_list(self, tab, file_path):
        write_list([item for item in tab], file_path)
    def write_dictionary(self, dico, file_path):
        write_dictionary(str__.convert_dict_to_utf8(dico), file_path)
    def get_scripts_of_project(self):
        return get_scripts_of_project()
    def read_item(self, param_name, file_path):
        return read_item(param_name, file_path)
# DOC 
# TODO: à faire
# FIXME: bug ou correction à faire
# NOTE: information importante

# Valeurs initiales de setting
def init_setting():
    setting = {} 
    setting[val_.SET_PROJECT_NAME    ] = None
    setting[val_.SET_VERSION         ] = None
    setting[val_.SET_LANGAGE         ] = "fr"
    setting[val_.SET_PATH_SYSTEM     ] = val_.SYSTEM_MODULES_PATH
    setting[val_.SET_PATH_SYSTEM_DATA] = val_.SYSTEM_DATA_PATH
    setting[val_.SET_PATH_USER       ] = val_.SYSTEM_MODULES_PATH
    setting[val_.SET_PATH_USER_DATA  ] = val_.SYSTEM_DATA_PATH
    setting[val_.SET_ON              ] = True
    setting[val_.SET_DESCRIPTION     ] = None
    setting[val_.SET_GLOSSARY        ] = val_.SYSTEM_GLOSSARY
    setting[val_.SET_USER_GLOSSARY   ] = None
    setting[val_.SET_DOC_BATCH       ] = val_.SET_LEBEL_PYTHON # PYTHON or ALL_NOTEPAD
    setting[val_.SET_EXT_DOC_BATCH   ] = "py"
    setting[val_.LANGAGE_PROG        ] = val_.SET_LEBEL_PYTHON # Python ou Javscript
    return setting;


#************************************************************************************************************************
#************************************************************************************************************************
#                                       L E C T U R E   E C R I T U R E
#************************************************************************************************************************
#************************************************************************************************************************
def get_Path_of_filename(file_name) : 
    """
    Retourne le texte d'un fichier.
    Balaye tous les dossiers
    """
    file_path = sys_.ui.getCurrentFilename()
    path_org = os.path.dirname(file_path)+os.sep     
    file_path = path_org+file_name
    if os.path.isfile(file_path):
        return file_path
        
    file_path = _get_path_of_folder(val_.SET_PATH_USER, file_name, path_org)
    if file_path: return file_path
        
    file_path = _get_path_of_folder(val_.SET_PATH_SYSTEM,      file_name, path_org)
    if file_path: return file_path
         
    file_path = _get_path_of_folder(val_.SET_PATH_SYSTEM_DATA, file_name, path_org)
    if file_path: return file_path
         
    return _get_path_of_folder(val_.SET_PATH_USER_DATA,   file_name, path_org)
    
def _get_path_of_folder(setting_name, file_name, path_org):
    """
    Recherche un fichier dans un dossier indiqué dans le fichie setting : .system_path_data.txt
    Puis retourne le texte si le fichier est présnet dans ce dossier
    """
    path_user = read_setting(setting_name)
    if not path_user or path_user==path_org: return None

    file_path = path_user+file_name
    if not os.path.isfile(file_path): return None
    return file_path

#@str__.wv_automat
def files_equal(file_path1, file_path2): 
    # comparaison de 2 chemins de fichiers avec normalisation des caractères
    return os.path.normcase(file_path1) == os.path.normcase(file_path2)
    
#@str__.wv_automat
def read(file_path, exists_optionel=False):
    """
    Lit le contenu d'un fichier texte en gérant les exceptions (compatible Python 2).

    Parameters 
    ----------
    file_path : str
        Le chemin du fichier à lire.
    exists_optionel : bool
        Vérification préaliable de l'existence du fichier
        
    Returns 
    -------
    str
        Le contenu du fichier.
    None
        Si le fichier est absent
    Raises
    ------
    IOError
        - errno.ENOENT : Si le fichier n'existe pas.
        - errno.EACCES : Si l'accès est refusé.
        - errno.EISDIR : Si 'file_path' est un dossier au lieu d'un fichier.
    OSError
        - Si un problème système empêche la lecture.
    MemoryError
        - Si le fichier est trop volumineux pour être chargé en mémoire.

    Examples
    --------
    >>> read("mon_fichier.txt")
    'Contenu du fichier...'
    """
    
    if exists_optionel and not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r') as file:
            return file.read()  # Lit tout le contenu du fichier

    except IOError as e:
        if e.errno == errno.ENOENT:
            raise IOError(error_("FILE_NOT_FOUND {}".format(file_path)))
        elif e.errno == errno.EACCES:
            raise IOError(error_("PERMISSION_DENIED_READ"))
        elif e.errno == errno.EISDIR:
            raise IOError(error_("IS_FOLDER)"))
        else:
            raise IOError(error_("IO_ERROR"))

    except OSError as e:
        raise OSError(error_("IO_ERROR_SYS"))

    except MemoryError:
        raise MemoryError(error_("FILE_TO_BIG"))
        
#@str__.wv_automat
def write(datas, file_path):
    """
    Écrit des données dans un fichier texte en gérant les exceptions (compatible Python 2).

    Parameters
    ----------
    file_path : str
        Le chemin du fichier où écrire les données.
    datas : str
        Le contenu à écrire dans le fichier.

    Raises 
    ------
    IOError
        - errno.ENOENT : Le dossier contenant 'file_path' n'existe pas.
        - errno.EACCES : Permission refusée pour écrire dans le fichier.
        - errno.EROFS : Système de fichiers en lecture seule.
        - errno.ENOSPC : Pas assez d’espace disque.
        - errno.EISDIR : 'file_path' est un dossier, pas un fichier.
    TypeError
        - Si 'datas' n'est pas une chaîne de caractères.

    Examples
    --------
    >>> ecrire_fichier("mon_fichier.txt", "Bonjour, monde!")
    """
    if not isinstance(datas, str):
        try: 
            datas = datas.encode("utf-8")
        except:    
            raise TypeError("Les données à écrire doivent être une chaîne de caractères. {}".format(type(datas)))

    try:
        with open(file_path, 'w') as file:
            file.write(datas)
            return True
    except IOError as e:
        if e.errno == errno.ENOENT:
            IOError(error_("FOLDER_ABSENT {}".format(file_path)))
            raise
        elif e.errno == errno.EACCES:
            raise IOError(error_("PERMISSION_DENIED_WRITE").format(file_path))
        elif e.errno == errno.EROFS:
            raise IOError(error_("FILE_READ_ONLY").format(file_path))
        elif e.errno == errno.ENOSPC:
            raise IOError(error_("DISK_FULL").format(file_path))
        elif e.errno == errno.EISDIR:
            raise IOError(error_("IS_FOLDER").format(file_path))
        else:
            raise IOError("IO_ERROR_SYS").format(file_path, e)

#@str__.wv_automat
def suppr_file(file_path):
    """
    Supprime un fichier en gérant les exceptions (compatible Python 2).

    Parameters
    ----------
    file_path : str
        Le chemin du fichier à supprimer.

    Raises
    ------
    OSError
        - errno.ENOENT : Le fichier n'existe pas.
        - errno.EACCES : Permission refusée.
        - errno.EBUSY : Fichier en cours d'utilisation.
        - errno.EISDIR : 'file_path' est un dossier, pas un fichier.
        - Autres erreurs système.

    Examples
    --------
    >>> supprimer_fichier("mon_fichier.txt")
    """
    try:
        os.remove(file_path)

    except OSError as e:
        if e.errno == errno.ENOENT:
            print("***Error*** SuppressFile : error_(FILE_NOT_FOUND").format(file_path)
            return
        elif e.errno == errno.EACCES:
            raise OSError(error_("PERMISSION_DENIED_SUPPR").format(file_path))
        elif e.errno == errno.EBUSY:
            raise OSError(error_("FILE_IN_USE").format(file_path))
        elif e.errno == errno.EISDIR:
            raise OSError(error_("IS_FOLDER").format(file_path))
        else:
            raise OSError(error_("IO_ERROR_SYS").format(file_path, e)) 

#@str__.wv_automat
def copy_file(file_path, destination_path):
    """
    Copie un fichier de file_path vers destination_path avec gestion des exceptions.
    
    Parameters
    ----------
    file_path : str
        Chemin du fichier source.
    destination_path : str
        Chemin du fichier de destination.
    
    Returns py
    -------
    bool
        True si la copie réussit, False sinon.
    
    Raises
    ------
    IOError
        Si une erreur d'entrée/sortie se produit.
    shutil.Error
        Si une erreur spécifique à shutil survient.
    OSError
        Si une erreur liée au système d'exploitation se produit.
    Exception
        Pour toute autre exception non prévue.
    """
    try:
        shutil.copy(file_path, destination_path)
        print("***Error*** "+error_("FILE_COPIED").format(file_path, destination_path))
        return True
    except IOError as e:
        raise OSError(error_("IO_ERROR").format(e))
    except shutil.Error as e:
        raise OSError(error_("SHUTIL_ERROR").format(e))
    except OSError as e:
        raise OSError(error_("IO_ERROR_SYS").format(e))
    except Exception as e:
        raise OSError(error_("UNKNOWN_ERROR").format(e))
    raise

            
#________________________________________________________________________________________________________________________
#
#                                       D O S S I E R
#________________________________________________________________________________________________________________________
#@str__.wv_automat
def make_dirs(folder, message):
    """
    Crée un dossier avec 'os.makedirs()', en gérant les exceptions (compatible Python 2).

    Parameters
    ----------
    folder : str
        Le chemin du dossier à créer.

    Raises
    ------
    OSError
        - errno.EEXIST : Le dossier existe déjà.
        - errno.EACCES : Permission refusée.
        - errno.ENOSPC : Pas assez d’espace disque.
        - errno.EROFS : Système de fichiers en lecture seule.

    Examples
    --------
    >>> make_dirs("mon_dossier")
    """
    try:
        os.makedirs(folder)
    except OSError as e:
        if e.errno == errno.EACCES:
            if message != None: print("***Error*** "+message)
            raise OSError(error_("PERMISSION_DENIED").format(folder))
        elif e.errno == errno.ENOSPC:
            if message != None: print("***Error*** "+message)
            raise OSError(error_("DISK_FULL").format(folder))
        elif e.errno == errno.EROFS:
            if message != None: print("***Error*** "+message)
            raise OSError(error_("FILE_READ_ONLY").format(folder))
        else:
            if message != None: print("***Error*** "+message)
            raise OSError(error_("UNKNOWN_ERROR").format(e))
            
#@str__.wv_automat
def backup_files_(file_pathes, base_directory, folder_name):
    if len(file_pathes)==0: return
    # Extraire le répertoire du premier fichier dans la liste
    
    numFree = SearchFolderFree(base_directory, folder_name)
    copy_files_to_subfolder(file_pathes, folder_name+str(numFree))
    
#@str__.wv_automat
def SearchFolderFree(pathCurr, prefix):
    """
    Recherche le 1er sous dossier libre - qui n'existe pas
    """
    # Initialiser un compteur pour tester les sous-dossiers
    i = 0
    # Créer un nom de dossier à tester
    while True:
        # Construire le chemin du dossier à tester
        folder_name = os.path.join(pathCurr, "{}{}".format(prefix,i))
        
        # Vérifier si le dossier existe déjà
        if not os.path.exists(folder_name):
            # Si le dossier n'existe pas, retourner le numéro
            return i
        i += 1

#@str__.wv_automat 
def copy_files_to_subfolder(file_paths, subfolder_name):
    """
    Copie une liste de fichiers dans un sous-dossier du même répertoire que les fichiers d'origine.

    :param file_paths -> list[str]: Liste des chemins des fichiers à copier.
    :param subfolder_name -> str: Nom du sous-dossier dans lequel copier les fichiers.
    
    :return -> None: Aucune valeur de retour, effectue uniquement la copie des fichiers.

    :note:
        - La fonction extrait le répertoire du premier fichier de `file_paths` pour définir l'emplacement du sous-dossier.
        - Si le sous-dossier n'existe pas, il est créé.
        - Chaque fichier de `file_paths` est copié dans le sous-dossier.

    :dependencies:
        - `os`: Manipulation des chemins et vérification/création de répertoires.
        - `shutil`: Copie de fichiers d'un emplacement à un autre.

    :example:
        >>> file_paths = ["/home/user/scripts/script1.js", "/home/user/scripts/script2.js"]
        >>> copy_files_to_subfolder(file_paths, "backup_js")
        # Les fichiers seront copiés dans `/home/user/scripts/backup_js/`
    """
    # Extraire le répertoire du premier fichier dans la liste
    base_directory = os.path.dirname(file_paths[0])
    
    # Créer le chemin complet du sous-dossier à partir du répertoire des fichiers
    subfolder_path = os.path.join(base_directory, subfolder_name)

    # Créer le sous-dossier s'il n'existe pas
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    # Copier chaque fichier dans le sous-dossier
    for file_path in file_paths:
        # Extraire le nom du fichier à partir du chemin complet
        file_name = os.path.basename(file_path)
        
        # Créer le chemin complet du fichier dans le sous-dossier
        destination_path = os.path.join(subfolder_path, file_name)
        
        # Copier le fichier dans le sous-dossier
        shutil.copy(file_path, destination_path)
        #rint("Fichier {} copied in {}".format(file_name, subfolder_path))

#@str__.wv_automat
def backup_js(file_paths, sub_foldee):
    """
    Effectue une sauvegarde des fichiers en les copiant dans un sous-dossier de sauvegarde.

    :param file_paths: Liste des chemins des fichiers à sauvegarder.
    :type file_paths: list[str]
    :param sub_folder: préfixe du sous-dossier de sauvegarde.
    
    :return: Rien (effectue uniquement la copie des fichiers).
    :rtype: None

    :note:
        - Si la liste `file_paths` est vide, la fonction retourne immédiatement sans exécuter d'actions.
        - La fonction extrait le répertoire du premier fichier de la liste pour déterminer l'emplacement de la sauvegarde.
        - Un sous-dossier de sauvegarde est créé en utilisant `val_.BACKUP_JS_FOLDER` suivi d'un numéro unique trouvé via `SearchFolderFree`.
        - Tous les fichiers de `file_paths` sont copiés dans ce sous-dossier.

    :dependencies:
        - `os` : Utilisé pour obtenir le répertoire du premier fichier.
        - `SearchFolderFree(base_directory, val_.BACKUP_JS_FOLDER)` : Fonction permettant de trouver un numéro unique pour éviter les conflits de noms de dossier.
        - `copy_files_to_subfolder(file_paths, val_.BACKUP_JS_FOLDER+str(numFree))` : Fonction effectuant la copie effective des fichiers.

    """
    if len(file_paths) == 0:
        return
    # Extraire le répertoire du premier fichier dans la liste
    base_directory = os.path.dirname(file_paths[0])

    # Trouver un numéro de dossier disponible
    numFree = SearchFolderFree(base_directory, sub_folder)

    # Copier les fichiers dans le sous-dossier de sauvegarde
    copy_files_to_subfolder(file_paths, sub_folder + str(numFree))

#************************************************************************************************************************
#************************************************************************************************************************
#                                       L I S T  /  D I C T I O N N A I R E 
#************************************************************************************************************************
#************************************************************************************************************************
#@str__.wv_automat        
def write_dictionary(dico, file_path):
    """
    Incrit un dictionnaire dans un fichier avec un indicateur de type
    """
    with open(file_path, "w") as f:
        for key, value in dico.iteritems():
            try:
                value = str__.to_type_str(value)
            except Exception as e:
                continue
            print("WRITE DICO {}:{}".format(key, value))
            f.write(key +": "+value+"\n")

#@str__.wv_automat
def read_dictionary(file_path):
    dico = {}
    with open(file_path, "r") as f:
        lines = f.readlines()
    for l in lines:
        pos = l.find(':')
        if pos<0: continue
        value = str__.convert_to_unicode( l[pos+1:].strip() )
        dico[convert_to_unicode(l[0:pos].strip())]=value
    return dico
def write_item_dictionary(value, key, file_path):
    """
    Ecrire un item dans un fichier-dictionnaire
    Note: le fichier doit exister avant la modification
    """
    # Lecture du fichier-dictionnaire
    dico = read_dictionary(file_path)
    if dico==None:
        str__.errorwv("unknown dictionary "+file_path)
        return False
 
    # Ecriture de l'item dans le dictionnaire
    try:
        dico[key] = value
    except Exception as e:
        str__.errorwv("unknown '"+name+"' in dictionary "+file_path)
        return False
        
    # Ecriture du fichier
    write_dictionary(dico, file_path)
    return True

def write_list_typed(liste, file_path):
    with open(file_path, "w") as f:
        for value in liste:
            try:
                v = str__.to_type_str(value)
                f.write(v[0] + "\n")
                f.write(v[1] + "\n")
            except Exception as e:
                """ nothing """

def read_list_typed(file_path):
    liste = []
    with open(file_path, "r") as f:
        lignes = f.readlines()

    # Chaque élément occupe 2 lignes : type, value
    for i in range(0, len(lignes), 2):
        type_val = lignes[i].rstrip('\n')
        value = lignes[i + 1].rstrip('\n')

        try:
            liste.append( str_to_type( type_val, value ) )
        except Exception as e:
            """ ignore """
    return liste 
def is_in_file_list(value, file_path):
    """ Inique si le chemin_complet_de_fichier est dans la liste inscrite dans le fichier 'file_path' """
    tab = read_list(file_path) 
    if not tab: return False
    for t in tab: print(value+" '"+str(t)+"'")
    return value in tab
def write_list(tab, file_path):
    if str__.to_list_str(tab)==None: 
        return False
    s = '\n'.join(tab)
    return write( s, file_path )
def read_list(file_path):
    s = read( file_path )
    if s==None: return None
    return convert_to_unicode(s).splitlines()
    
#************************************************************************************************************************
#************************************************************************************************************************
#                                       P R O P R I E T E   :   S E T T I N G   S Y S T E M E
#************************************************************************************************************************
#************************************************************************************************************************
#@str__.wv_automat
def read_item(param_name, file_path):
    """
    Lecture d'une variable dans un fichiers-de-variable
    Un fichier de variables associe un nom à des valeurs
    C'est en fait un tableau[nom] de Python, sauvegardé au format J son 
    """
    variables = read_dictionary(file_path)
    if variables==None:
        str__.errorwv("unknown item "+param_name+" in file "+file_path)
        return None
    # Lecture du paramètre
    try: 
        return variables[param_name]
    except KeyError:
        return None
#@str__.wv_automat 
def read_citation(name, file): 
    """
    Lit un texte au format propriétaire-WV multilignes dans un fichier.
    Le nom pourra comporter une désignation du langage
    - désignation de langage est _fr. : nom_fr.ext
    - fr sera remplacé par le langage indiqué dans le fichier setting à la désignation "langage"
    - le chemin du fichier setting est affecté à ce module lors de l'initialisation du projet

    Parameters
    ----------
    name : str
        Nom de l'item à rechercher dans le fichier.
    file_path : str
        Chemin du fichier contenant les messages.

    Returns
    -------
    str
        Le message correspondant à 'name' sous forme de chaîne de caractères multilignes.
    """
    try:
        try:
            with open(file, "r") as fichier:
                contains = fichier.read()
        except IOError:
            # Lancer une exception si une erreur de lecture du fichier survient
            error_="Error : information file not read : '{}'".format(file)
            raise Exception(error_)
        contains = re.sub(r'=\s+`', '=`', contains)
        contains = re.sub(r'`\s+;', '`;', contains)
        contains = re.sub(r'#\s*([^\s#=]+)\s*([^\s#=]+)\s*=`', r'#\1\2=`', contains)


        #rint(contains)
        # Construire le motif de recherche
        pattern = r"\#" + re.escape(name) + r"=`([^;]*)`;"
        match = re.search(pattern, contains)
        #rint(match)

        if match:
            texte = match.group(1).strip()
            texte = re.sub(r"^¤", " ", texte)  # Remplace ¤ en début
            texte = re.sub(r"¤$", " ", texte)  # Remplace ¤ en fin
            return texte  # Retourne la valeur trouvée
        else:
            return None  # Retourne None si le motif n'est pas trouvé

    except IOError:
        print("***Erreur*** : Impossible de lire le fichier.")
        return None  # Retourne None en cas d'erreur de lecture

#@str__.wv_automat
def read_message(nom):
    langage = read_item(val_.SET_LANGAGE, val_.SYSTEM_SETTING_FILE)
    file = val_.SYSTEM_MESSAGES+langage+".txt"

    return read_citation(nom, file)
#@str__.wv_automat
def read_error(nom):
    langage = read_item(val_.SET_LANGAGE, val_.SYSTEM_SETTING_FILE)
    file = val_.SYSTEM_ERROR_MESSAGES+langage+".txt"

    return read_citation(nom, file)
    #c:\Users\33684\AppData\Roaming\Notepad++\plugins\config\PythonScript\scripts\npp_js_datas\errors_fr.txt

def read_setting(key):
    return read_item(key ,val_.SYSTEM_SETTING_FILE) 
    
def write_setting(value, key):
    path = val_.SYSTEM_SETTING_FILE
    if path==None:
        raise IOError( "System error_. Error not init.")  
    return write_item_dictionary(value, key, path)
#@str__.wv_automat
def read_langage():
    return read_item(val_.SET_LANGAGE,val_.SYSTEM_SETTING_FILE) 
    
#@str__.wv_automat
def error_(name):
    path = val_.SYSTEM_ERROR_MESSAGES+read_langage()+".txt"
    print("error_"+path);
    if path==None:
        raise IOError( "System error_. Error not init.")
    return read_citation(name, path)

#@str__.wv_automat
def message_(name):
    path = val_.SYSTEM_MESSAGES+read_langage()+".txt"
    if path==None:
        raise IOError( "System error_. Error not init.")
    return read_citation(name, path)

def read_file_langage(file_path):
    if file_path.find("_fr.")<0:
        error_(FILE_LANGAGE)
        return None
    return read( file_path.replace("_fr.", "_" + read_langage() + "."))
    

def read_citation_langage(name, file_path):
    """
    Lit une citation* dans un fichier de texte pour la langue délectionnée dans '.system_setting.txt' 
    Syntaxe du fichier :
        #citation1=`texte de la citation1`;
        #citation2=`texte de la citation2`;
        ...
    """
    if file_path.find("_fr.")<0:
        error_(FILE_LANGAGE)
        return None
    return read_citation( name, file_path.replace("_fr.", "_" + read_langage() + "."))
    
#************************************************************************************************************************
#************************************************************************************************************************
#                                       B A T C H - T R A I T E M A N T   P A R   L O T 
#************************************************************************************************************************
#************************************************************************************************************************
def get_scripts_of_project():
    if val_.doc_batch=="ALL_NOTEPAD" :
        """ Retourne la liste des fichiers ouverts dans Notepad 
        Appelé par : hot_goto.py/list_functions_py()
        return [0, [file_path,...]] 
        """
        files_notepad=notepad.getFiles()
        files_ok=[]
        files = []
        for file_edit in files_notepad:
            file = str_.convert_to_unicode(file_edit[0])
            
            file_name = os.path.basename(file)
            if file_name in files_ok: continue

            files_ok.append(file_name)
            files.append(file)
    elif val_.doc_batch=="PYTHON" :
        """ """
        get_setting(val_.SET_PATH_USER)
        files = glob.glob(val_.SYSTEM_MODULES_PATH + "/*.py")
    files = sorted(files)
    return [0, files]
    
#@str__.wv_automat
def get_setting(key):
    """ 
    Récupère l'option de batch de documents
    Liste des documents à traiter par lot
    - Les document dans Notepad ou les fichiers Python d'un dossier
    Exemple d'usage: lister les fonctions Python dans 'functions.py'
    """
    path = val_.SYSTEM_SETTING_FILE
    if path==None:
        raise IOError( "System error_. Error not init.")  
    setting =  read_dictionary(path)
    if setting==None     : return None
    try                  : return setting[key]
    except Exception as e: return None
    
        
   