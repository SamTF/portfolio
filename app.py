### The Main Flask app for my Portfolio website. I might completely redesign this in the future.
### Will loop through every project in the projects directory, and serve an HTML page for it based on pre-made HTML and CSS/SASS templates

### IMPORT
from flask import Flask, render_template        # The main thing - render_template is used to load HTML files     
from markupsafe import Markup                   # Used to pass variables as HTML markup instead of plain text - https://tedboy.github.io/flask/generated/generated/flask.Markup.html
import projects                                 # My script that lists all the projects and project categories in the ./static/projects folder
from flask import send_from_directory           # Sending a static file directly - TEMP

### CONSTANTS
PROJECTS = projects.Projects()

HOME = {
    'title'         : "Things I've Made",
    'footer'        : 'Sebastião Casaleiro',
    'creation_date' : '2023',
    'description'   : "A showcase of projects I've made across various fields.",
    'thumb'         : "/static/images/website_thumbnail.webp"
}

ABOUT = {
    'title'         : 'About Me :)',
    'footer'        : 'Sebastião Casaleiro',
    'creation_date' : '2023',
    'description'   : 'A short bio of who I am and what I like to do :)',
    'thumb'         : '/static/images/website_thumbnail.webp'
}

### WEBSITE PAGES #############################
# Initialises Flask
app = Flask(__name__)

### Homepage
@app.route('/')
@app.route('/home')
@app.route('/things-ive-made')
def home():
    # return 'Welcome home! 🐍'
    return render_template('home.html', title=HOME['title'], projects=PROJECTS.list, footer_title=HOME['footer'], creation_date=HOME['creation_date'], description=HOME['description'], thumb=HOME['thumb'])

### About Me Page
@app.route('/about')
@app.route('/me')
@app.route('/about-me')
def about():
    return render_template('about.html', title=ABOUT['title'], footer_title=ABOUT['footer'], creation_date=ABOUT['creation_date'], description=ABOUT['description'], thumb=ABOUT['thumb'])


### Project page
@app.route('/<category>/<project>')
def project_page(category, project):
    # Checks if the category exists - if not instantly throws a 404 error
    if not PROJECTS.category_exists(category):
        return f'<center><code><h1>Error 404: directory <em>{category}</em> not found</h1></code></center>'
    
    # Checks if a Project object exists with that name
    p = PROJECTS.get_project(project, category)

    # If the project doesn't exist
    if not p:
        return f'<center><code><h1>Error 404: Project <em>{project}</em> not found in directory <em>{category}</em></h1></code></center>'

    
    # Returing the Project Page
    return render_template('_project.html', title=p.title, banner=p.banner, content=Markup(p.HTML_content), footer_title=p.title, creation_date=p.creation_date, description=p.description, thumb=p.thumb)


### CV Direct Link
@app.route('/CV')
@app.route('/cv')
@app.route('/resume')
def cv():
    return send_from_directory('static', 'CV_2023_games.pdf')

### BA Thesis Direct Link
@app.route('/thesis')
def thesis():
    return send_from_directory('static/projects/video_games/thesis/', 'Sebastião Casaleiro - Letting Players Draw Their Own Character.pdf')