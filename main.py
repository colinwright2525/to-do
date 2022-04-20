from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.String(250), nullable=False)
    date_completed = db.Column(db.String(250), nullable=False)

# db.create_all()

class TaskForm(FlaskForm):
    body = StringField("Task", validators=[DataRequired()])
    date_one = StringField("Date of task creation", validators=[DataRequired()])
    date_two = StringField("Date task is to be completed", validators=[DataRequired()])
    submit = SubmitField("Add Task")

@app.route('/', methods=['GET', 'POST'])
def home():
    form = TaskForm()
    tasks = Task.query.all()
    if request.method == 'POST':
        new_task = Task(
            description=request.form.get("body"),
            date_created=request.form.get("date_one"),
            date_completed=request.form.get("date_two"),
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('index.html', form=form, tasks=tasks)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task_to_delete = Task.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/complete/<int:task_id>')
def mark_complete(task_id):
    task = Task.query.get(task_id)
    task.description = f'{task.description} | Completed'
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)