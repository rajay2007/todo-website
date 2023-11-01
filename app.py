from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'todo.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACk_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sl_no = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sl_no} - {self.title}"
    
def create_db():
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
def Bootstrap():
    if request.method == 'POST':
        user_title = request.form['title']
        user_desc = request.form['description']
        todo = Todo(title=user_title, desc=user_desc)
        db.session.add(todo)
        db.session.commit()
    
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route('/update/<int:sl_no>', methods=['GET', 'POST'])
def Update(sl_no):
    if request.method == 'POST':
        update_title = request.form['title']
        update_desc = request.form['description']
        todo = Todo.query.filter_by(sl_no=sl_no).first()
        todo.title = update_title
        todo.desc = update_desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sl_no=sl_no).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sl_no>')
def Delete(sl_no):
    todo = Todo.query.filter_by(sl_no=sl_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    create_db()
    app.run(debug=False, host="0.0.0.0", port="5000")