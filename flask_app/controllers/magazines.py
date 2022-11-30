from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.magazine import Magazine
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/addMagazine')
def createForm():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id']
    }
    return render_template('createMag.html', loginUser= User.get_user_by_id(data),)


@app.route('/createmagazine', methods = ['POST'])
def createMagazine():

    if 'user_id' not in session:
        return redirect('/logout')
    if not Magazine.validate_magazine(request.form):
        return redirect(request.referrer)

    Magazine.create_magazine(request.form)
    
    return redirect('/')

@app.route('/subcribe/<int:id>')
def addsubcribe(id):
    data = {
        'magazine_id': id,
        'user_id': session['user_id']
    }
    Magazine.add_subcribe(data)
    return redirect(request.referrer)

@app.route('/unsubcribe/<int:id>')
def removesubcribe(id):
    data = {
        'magazine_id': id,
        'user_id': session['user_id']
    }
    Magazine.remove_subcribes(data)
    return redirect(request.referrer)

@app.route('/showmagazine/<int:id>')
def showOne(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'magazine_id': id,
        'user_id': session['user_id']
    }
    magazine=Magazine.get_magazine_by_id(data)
    get_user_magazine=Magazine.get_user_Magazine(data)
    
    return render_template('showMag.html', magazine=magazine,get_user_magazine=get_user_magazine)


@app.route('/delete/<int:id>')
def delete(id):

    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        'magazine_id': id,
        'user_id': session['user_id']
    }
    currectMagazine = Magazine.get_magazine_by_id(data)

    if not session['user_id'] == currectMagazine['user_id']:
        return redirect('/')

    Magazine.deleteAllsubcribes(data)
    Magazine.delete(data)

    return redirect(request.referrer)