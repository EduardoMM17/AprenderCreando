from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'aprendo-creando-y-esta-es-la-llave'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
notLogged = True

#DEFINICIÓN DE LAS TABLAS MENCIONADAS EN CLASE
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    password= db.Column(db.String(200))

    def __repr__(self):
        return '<User %r>' % self.id


#IMPLEMENTAR ESTA RUTA COMO QUIERAN
@app.route("/")
def index():
    temp = notLogged
    return render_template('index.html', notLogged=temp)


@app.route("/registro", methods=['POST', 'GET']) #MÉTODOS A USAR
def register():
    notLogged = True
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            email = form.email.data #COLOCO LOS DETALLES DEL FORM EN UNA VARIABLE
            password = form.password.data
            user = User(email=email, password=password) #CREO EL OBJETO USER
            db.session.add(user) #LO AGREGO A LA BASE DE DATOS
            db.session.commit() #LO SUBO A LA BASE DE DATOS
            notLogged = False
            return redirect('/tareas')
        else:
            flash("EL USUARIO YA ESTÁ REGISTRADO", 'error') #RENDEREA UN MENSAJE EN LA PAG. WEB SI HAY UN ERROR
            return redirect('/registro')
    return render_template('registro.html', form=form, notLogged=notLogged)


#POR HACER:
#IMPLEMENTAR EL LOGIN
#@app.route("/login")
#def login():


@app.route("/tareas", methods=['POST', 'GET'])
def tareas():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        db.session.add(new_task)
        db.session.commit()
        return redirect("/tareas")

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        # Todo.query.order_by ordena según el parametro que le pases, en este caso la fecha. Y como colocamos .all(),
        # Ordenerá toda la info
        return render_template('tareas.html', tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    db.session.delete(task_to_delete)
    #FALTA UN PEDAZO DE CÓDIGO IGUAL DE LA RUTA TAREAS
    #DEFINIR ADONDE SEREMOS REDIRIGIDOS


if __name__ == "__main__":
    app.run(debug=True)