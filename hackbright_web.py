"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github1 = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github1)

    title_grade_pairs = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html", first=first, last=last,
                           github=github, pairs=title_grade_pairs)

    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student_add")
def display_form():
    """Render form to add student to database"""
    return render_template("student_add.html")

@app.route("/add_student", methods=['POST'])
def add_a_student():
    """Add a student to database."""

    first = request.form.get('first')
    last = request.form.get('last')
    github = request.form.get('github')
    hackbright.make_new_student(first, last, github)

    return render_template("success.html", github=github)

@app.route("/which_proj")
def display_projform():
    """Render form for project info"""
    return render_template("which_proj.html")

@app.route("/project")
def display_proj_info():
    """shows requested information about a project."""

    title = request.args.get('project')
    proj_info = hackbright.get_project_by_title(title)
    proj_grades = hackbright.get_grades_by_title(title)

    print proj_grades
    print proj_info
    return render_template("proj_info_display.html", proj=proj_info, grades=proj_grades)

@app.route("/")
def homepage():
    """Render homepage"""
    all_students = hackbright.get_all_students()
    all_projects = hackbright.get_all_projects()

    return render_template("home.html", students=all_students, projects=all_projects)

@app.route("/project_form")
def show_project_form():
    """Display form to add a new project."""
    return render_template("create_project_form.html")

@app.route("/add_project", methods=["POST"])
def add_project():
    """Add a project to database."""
    name = request.form.get('project_name')
    description = request.form.get('project_description')
    grade = request.form.get('project_max_grade')
    hackbright.add_project(name, description, grade)
    return redirect('/')

@app.route("/grade_form")
def show_grade_form():
    """Display form to add a grade."""
    all_students = hackbright.get_all_students()
    all_projects = hackbright.get_all_projects()

    return render_template("add_grade_form.html", students=all_students, projects=all_projects)

@app.route("/add_grade", methods=["POST"])
def add_grade():
    """Add or update a grade"""

    github = request.form.get('student')
    title = request.form.get('project')
    grade = request.form.get('grade')

    if hackbright.get_grade_by_github_title(github, title):
        hackbright.assign_grade(github, title, grade)
    else:
        hackbright.update_grade(github, title, grade)

    return redirect("/")
        



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
