from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/")
def index():
    return render_template('index.html')



@app.route("/tareas", methods=['POST', 'GET'])
def tareas():
    print("LLAME AQUI")
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


@app.route("/registro")
def register():
    return render_template("registro.html")


@app.route("/login")
def login():
    return "AQUI VA EL LOGIN"


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    db.session.delete(task_to_delete)
    #FALTA UN PEDAZO DE CÓDIGO IGUAL DE LA RUTA TAREAS
    #DEFINIR ADONDE SEREMOS REDIRIGIDOS


#@app.route("/update/<int:id>", methods=['GET', 'POST'])
#def update(id):


if __name__ == "__main__":
    app.run(debug=True)