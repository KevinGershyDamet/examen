from flask import Flask, render_template, redirect, request, session, flash

from flask_app import app

from flask_app.models.usuario import Usuario
from flask_app.models.amistad import Amistad

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/main')
def register():
    return render_template('login.html')

@app.route('/save_user', methods=['post'])
def save_user():

    data_to_validate = {'name': request.form['name'],
            'alias': request.form['alias'],
            'email': request.form['email'],
            'password': request.form['password'],
            'password_2': request.form['password_2'],
            'birthday': request.form['birthday']}

    if not Usuario.validate(data_to_validate):
        return redirect('/main')
    
    data = {'name': request.form['name'],
            'alias': request.form['alias'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password']),
            'birthday': request.form['birthday']}
        
    Usuario.save(data)
    flash('You registered yourself successfully!')
    
    return redirect('/main')

@app.route('/login', methods=['post'])
def login():
    data = {'email': request.form['email']}
    found = Usuario.find(data)
    
    if len(found) > 0:
        if bcrypt.check_password_hash(found[0]['password'], request.form['password']):
            session['id'] = found[0]['id']
            session['name'] = found[0]['name']
            session['alias'] = found[0]['alias']
            session['email'] = found[0]['email']
            return redirect('/friends')
    
    flash('Either the email or the password is incorrect')
    return redirect('/main')

@app.route('/friends')
def friends():
    if not session:
        return redirect('/main')
    
    data = {'id': session['id']}
    fr = Usuario.friendships(data)
    not_fr = Usuario.not_friendships(data)
    return render_template('friends.html', fr = fr, not_fr = not_fr)

@app.route('/user/<int:id>')
def user_page(id):
    if not session:
        return redirect('/main')
    
    data = {'id': id}
    info = Usuario.find_id(data)
    return render_template('profile.html', info = info)

@app.route('/end_session')
def end_session():
    session.clear()
    return redirect('/main')

@app.route('/add/<int:friend_id>')
def add_friend(friend_id):
    data = {'user_id': session['id'],
            'friend_id': friend_id}
    Amistad.add_friend(data)
    return redirect('/friends')

@app.route('/remove/<int:friend_id>')
def remove_friend(friend_id):
    data = {'user_id': session['id'],
            'friend_id': friend_id}
    Amistad.remove_friend(data)
    return redirect('/friends')