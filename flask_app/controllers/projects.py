from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.project import Project
from flask_app.models.user import User


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = User.get_user_by_id({"id": session['user_id']})
        projects = Project.get_all_projects()
        return render_template('dashboard.html',
                               user=user,
                               projects=projects)
    return redirect('/')


@app.route('/new/project')
def new_project():
    if 'user_id' in session:
        user = User.get_user_by_id({"id": session['user_id']})
        return render_template('create.html',
                               user=user)
    return redirect('/')


@app.route('/create/project', methods=['POST'])
def create_project():
    if 'user_id' in session:
        if Project.validate_project(request.form):
            data = {
                'project_name': request.form['project_name'],
                'client_name': request.form['client_name'],
                'word_count': request.form['word_count'],
                'word_rate': request.form['word_rate'],
                'amount_total': request.form['amount_total'],
                'start_date': request.form['start_date'],
                'due_date': request.form['due_date'],
                'user_id': session['user_id']
            }
            print(data)
            Project.save(data)
            return redirect('/dashboard')
        return redirect('/new/project')
    return redirect('/')


@app.route('/edit/project/<int:id>')
def edit_project(id):
    if 'user_id' in session:
        user = User.get_user_by_id({"id": session['user_id']})
        project = Project.get_project_by_id({'id': id})
        return render_template('edit.html',
                               project=project,
                               user=user)
    return redirect('/')


@app.route('/update/project/<int:id>', methods=['POST'])
def update_projects(id):
    if 'user_id' in session:
        if Project.validate_project(request.form):
            data = {
                'project_name': request.form['project_name'],
                'client_name': request.form['client_name'],
                'word_count': request.form['word_count'],
                'word_rate': request.form['word_rate'],
                'amount_total': request.form['amount_total'],
                'start_date': request.form['start_date'],
                'due_date': request.form['due_date'],
                'id': id
            }
            Project.update_project(data)
            print(data)
            return redirect('/dashboard')
        return redirect(f'/edit/project/{id}')
    return redirect('/')


@app.route('/delete/project/<int:id>')
def delete_project(id):
    if 'user_id' in session:
        Project.delete({'id': id})
        return redirect('/dashboard')
    return redirect('/')


@app.route('/projects/all')
def allprojects():
    if 'user_id' in session:
        user = User.get_user_by_id({"id": session['user_id']})
        projects = Project.get_all_projects()
        return render_template('allprojects.html',
                               user=user,
                               projects=projects)
    return redirect('/')
