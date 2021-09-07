### The Main Flask app for my Portfolio website. I might completely redesign this in the future.
### Will loop through every project in the projects directory, and serve an HTML page for it based on pre-made HTML and CSS/SASS templates

### IMPORT
from flask import Flask, render_template
from flask.scaffold import F        # The main thing - render_template is used to load HTML files
from markupsafe import Markup                   # Used to pass variables as HTML markup instead of plain text - https://tedboy.github.io/flask/generated/generated/flask.Markup.html
import projects                                 # My script that lists all the projects and project categories in the ./static/projects folder
from flask import send_from_directory           # Sending a static file directly - TEMP

### CONSTANTS
PROJECTS = projects.Projects()

### WEBSITE PAGES #############################
# Initialises Flask
app = Flask(__name__)

### Homepage
@app.route('/')
@app.route('/home')
@app.route('/things-ive-made')
def home():
    # return 'Welcome home! 🐍'
    return render_template('home.html', title="Things I've Made", projects=PROJECTS.list)


### Project page
@app.route('/<category>/<project>')
def micro_mike(category, project):
    # Checks if the category exists - if not instantly throws a 404 error
    if category not in PROJECTS.list.keys():
        return f'<center><code><h1>Error 404: directory <em>{category}</em> not found</h1></code></center>'
    
    # Checks if a Project object exists with that name
    p = PROJECTS.find_name(project, category)

    # If the project doesn't exist
    if not p:
        return f'<center><code><h1>Error 404: Project <em>{project}</em> not found in directory <em>{category}</em></h1></code></center>'

    
    # Returing the Project Page
    return render_template('_project.html', title=p.title, banner=p.banner, content=Markup(p.HTML_content))


### PDF Files - temp!! NGINX will take care of it later -> https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
@app.route('/documents/<category>/<project>/<filename>')
def serve_pdf(category, project, filename):
    return send_from_directory(f'./static/projects/{category}/{project}/', filename)


    


### RUNNING APP #############################
if (__name__ == '__main__'):
    app.run(debug=True)
    # app.run(debug=False, port=4999, host='localhost')