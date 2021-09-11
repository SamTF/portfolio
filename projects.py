### Gets all the Project Categories and their respective Projects

### Imports     ##################
import os
import json

### Constants   ##################
ROOT = 'static/projects/'
CONTENT = f'{ROOT}/content.html'


### Classes     ##################
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

            print(self)
    
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
    

class Projects:
    def __init__(self):
        self.projects = get_projects()
    
    def reload_projects(self):
        self.projects = get_projects()
    
    def find_name(self, name:str, category:str):
        '''
        Checks if a project by the given name exists in the category. Returns the Project object if found, otherwise returns None.
        '''
        try:
            return [x for x in self.projects[category] if x.name == name][0]
        except:
            return None
    
    @property
    def list(self):
        return self.projects



### Functions   ##################
# Gets all the directories in a path (SUPER FAST)
def get_folders(root: str):
    current, dirs, files = next(os.walk(root))
    return dirs


def inst_proj(c:str, projects:list):
    '''
    Instantiates an instance of the Project class for each directory in the "projects" list.
    Returns a generator or list.

    projects: list of items for which to create Project class instances
    '''
    l = (Project(p, c) for p in projects)
    return list(l)



# Gets the categories and all of their subdirectories, and saves them into a dictionary
def get_projects_simple(root):
    categories = get_folders(root)
    projects = {x: get_folders(root + x) for x in categories}

    return projects

# Same as get_projects, but saves each project as a Project instance instead of just a string
def get_projects():
    categories = get_folders(ROOT)
    projects = {c: inst_proj(c, get_folders(ROOT+c)) for c in categories}
    return projects



### Running the script #########
if (__name__ == '__main__'):
    # projects = get_projects()
    # print(projects)
    # print('------')

    # for key, value in projects.items():
    #     for i in value:
    #         print(i)
    
    # print('############\n')

    p = Projects()
else:
    print('PROJECT_LIST IMPORTED')