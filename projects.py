### Gets all the Project Categories and their respective Projects

### Imports     ##################
import os                                                                   # to get the directories, subdirectories, and files
import json                                                                 # to read JSON files from disk
import operator                                                             # to sort a list of classes by attribute

# test
from random import randrange

### Constants   ##################
ROOT = 'static/projects/'
CONTENT = f'{ROOT}/content.html'


### Classes     ##################
# PROJECT
class Project:
    def __init__(self, name, category):
        self.name           =   name                                        # the name of the project folder
        self.title          =   name.replace('_', ' ').title()              # the actual title of the project
        self.URL            =   f'/{category}/{name}'                       # the link to the project page on the website
        self.category       =   category                                    # the project's category (its parent folder)
        self.path           =   f'{ROOT}{category}/{name}/'                 # the path to the project on disk
    
        self.description    =   name                                        # description for the thumbnail tooltip on the home page
        self.thumb          =   f'/{self.path}thumb.webp'                   # path to the thumbnail image
        self.banner         =   f'/{self.path}banner.webp'                  # path to the banner image
        self.creation_date  =   '2000-02-24'                                # date when the project was created

        self.content        =   self.path + 'content.html'                  # path to the file with the HTML page content

        # Getting Metadata if .meta.json file exists
        if os.path.exists(f'{self.path}.meta.json'):
            with open(f'{self.path}.meta.json') as f:
                meta = json.load(f)
                self.title          = meta['title']
                self.description    = meta['description']
                self.creation_date  = meta['date_created']

    
    # A representation of the Object when printed
    def __repr__(self) -> str:
        return f'Project: {self.category} | {self.title} | {self.description} | {self.URL} | {self.path}'
    

    @property
    def HTML_content(self):
        '''
        Returns the HTML page content for the project.
        '''
        try:
            with open(self.content, 'r') as f:
                return f.read()
        except:
            with open(CONTENT, 'r') as f:
                return f.read()
    


# CATEGORY
class Category:
    # Initialises the class object
    def __init__(self, name: str) -> None:
        self.name = name
        self.title = name.replace('_', ' ')
        self.path = f'{ROOT}{name}/'
        self.order = randrange(10)

        # searching for subdirectories and creating Project instances
        self.projects = inst_proj(name, get_folders(self.path))

        # loads a meta.json file if it exists to get additional metadata
        meta_file = f'{self.path}.meta.json'
        if os.path.exists(meta_file):
            with open(meta_file) as f:
                meta = json.load(f)
                self.order = meta['order']
    

    def get_project(self, name:str) -> Project:
        '''
        Searches for a Project object m=by name, and returns it if it exists.

        name: Name of the project (its folder)
        '''
        try:    return [x for x in self.projects if x.name == name][0]
        except: return None
    

    # A representation of the Object when printed
    def __repr__(self) -> str:
        return f'\nCategory #{self.order}: {self.title} @ {self.path}\n>>> {self.projects}\n\n'
    

    # Returns the list of all projects in this category
    @property
    def list(self):
        return self.projects


# PROJECTS MAIN CLASS
class Projects:
    def __init__(self):
        # self.projects = get_projects()
        self.projects = inst_categories(get_folders(ROOT))
        
    
    def reload_projects(self):
        self.projects = inst_categories(get_folders(ROOT))
    
    
    def category_exists(self, category: str):
        return os.path.exists(f'{ROOT}{category}/')
    
    # Getting a Project by name
    def get_project(self, name:str, category:str) -> Project:
        '''
        Searches for a Project by its name and its Category name, and returns it if it exists

        name: Name of the project (same as the project folder)
        category: Name of the category (same the project's parent folder)
        '''
        category = [c for c in self.projects if c.name == category]          # Gets a list of Category objects that match that name (there should at most be 1)

        if category:
            return category[0].get_project(name)
        else:
            return None
    
    @property
    def list(self):
        return self.projects



### Functions   ##################
# Gets all the directories in a path (SUPER FAST)
def get_folders(root: str):
    '''
    Gets all the directories in a given path
    '''
    current, dirs, files = next(os.walk(root))
    return dirs


def inst_proj(c:str, projects:list):
    '''
    Instantiates an instance of the Project class for each directory in the "projects" list.
    Returns a generator or list.

    projects: list of items for which to create Project class instances
    '''
    l = (Project(p, c) for p in projects)
    sorted_list = sorted(l, key=operator.attrgetter('creation_date'), reverse=True)
    return sorted_list



# Instantiating Category objects for each subfolder in the projects/ folder
def inst_categories(dirs: list):
    '''
    Creates Category class instances for each directory in the list of dirs given.
    '''
    categories = [Category(dir) for dir in dirs]                                    # creates a Category object for each folder in the projects directory, and stores them all in a list
    categories = sorted(categories, key=operator.attrgetter('order'))               # sorts the list by Category order attribute
    return categories



### Running the script #########
if (__name__ == '__main__'):
    p = Projects()
else:
    print('PROJECTS IMPORTED')