"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

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

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
