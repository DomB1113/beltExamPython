from flask_app.models.login import Login
from flask_app.models.sighting import Sighting
from flask_app import app
from flask import redirect, request, session, render_template, flash


@app.route('/new/sighting')
def new_sighting():
    if 'login_id' not in session:
        return redirect('/logout')
    data={
        'id':session['login_id']
    }
    login = Login.get_by_id(data) 
    
    return render_template('new_report.html' , login = login)

@app.route('/create/sighting', methods = ['POST'])
def create_sighting():
    if 'login_id' not in session:
        return redirect('/logout')
    if not Sighting.validate_report(request.form):
        return redirect('/new/sighting')
    
    Sighting.insert_sas(request.form)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def show_sighting(id):
    if 'login_id' not in session:
        return redirect('/logout')
    data = {
        'id':session['login_id']
    }
    login = Login.get_by_id(data) 
    report_data = {
        'id':id
    }
    reported = Sighting.get_by_sas_id_plus_login(report_data)
    skeptics = Sighting.show_skeptics(report_data)
    
    return render_template('show_report.html', login=login , reported = reported, skeptics = skeptics)

@app.route('/add/skeptic', methods = ['POST'])
def add_skeptics():
    data ={
        'login_id': session['login_id'],
        'sighting_id':request.form['sighting_id']
    }
    Sighting.add_skeptic(data)
    return redirect(f"/show/{request.form['sighting_id']}")

@app.route('/delete/skeptic', methods = ['POST'])
def delete_skeptic():
    data = {
        'login_id' : session['login_id'],
        'sighting_id' : request.form['sighting_id']
    }
    Sighting.delete_skeptic(data)
    return redirect(f"/show/{request.form['sighting_id']}")


@app.route('/edit/<int:id>')
def edit_sighting(id):
    if 'login_id' not in session:
        return redirect('/logout')
    data={
        'id':session['login_id']
    }
    login = Login.get_by_id(data) 
    
    report_data ={
        'id':id
    }

    report = Sighting.get_by_sas_id(report_data)
    print(report)

    return render_template('edit_report.html', login=login , report= report)

@app.route('/update/sighting' , methods = ['POST'] )
def update_sighting():
    if 'login_id' not in session:
        return redirect('/logout')
    if not Sighting.validate_report(request.form):
        return redirect(f"/edit/{request.form['id']}")
    Sighting.update_sas(request.form)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete_sighting(id):
    data = {
        'id':id
    }
    Sighting.delete_sas(data)
    return redirect('/dashboard')