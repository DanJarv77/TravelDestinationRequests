from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.destination import Destination
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
        
    return render_template('dashboard.html', user=user, destinations=Destination.get_all())

@app.route('/destinations/new')
def create_destination():
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('destination_new.html')

@app.route('/destinations/new/process', methods=['POST'])
def process_destination():
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Destination.validate_destination(request.form):
        return redirect('/destinations/new')

    data = {
        'user_id': session['user_id'],
        'location': request.form['location'],
        'what_happened': request.form['what_happened'],
        'date_travel': request.form['date_travel'],
        'number_group': request.form['number_group']
    }
    Destination.save(data)
    return redirect('/dashboard')

@app.route('/destinations/<int:id>')
def view_destination(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('destination_view.html',destination=Destination.get_by_id({'id': id}))

@app.route('/destinations/edit/<int:id>')
def edit_sighting(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('destination_edit.html',destination=Destination.get_by_id({'id': id}))

@app.route('/destinations/edit/process/<int:id>', methods=['POST'])
def process_edit_destination(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Destination.validate_destination(request.form):
        return redirect(f'/destinations/edit/{id}')

    data = {
        'id': id,
        'location': request.form['location'],
        'what_happened': request.form['what_happened'],
        'date_travel': request.form['date_travel'],
        'number_group': request.form['number_group']
    }
    Destination.update(data)
    return redirect('/dashboard')

@app.route('/destinations/destroy/<int:id>')
def destroy_destination(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    Destination.destroy({'id':id})
    return redirect('/dashboard')