from datetime import datetime as dt

from web_app import app
from web_app import db
from flask import render_template, redirect, url_for, flash, get_flashed_messages
import datetime as dt
import uuid
import sys

import forms
from models import Task, CrewMember, Crew


def console_out(msg):
    """ output to console """
    print(msg, file=sys.stderr)
    return


@app.route('/')
@app.route('/index')
def index():
    # return 'Hello Bernard'
    tasks = Task.query.all()
    return render_template('index.html', list_name='Ze_List', tasks=tasks)


@app.route('/watch')
def watch():
    watch_list = [
            {'number': 1, 'crew_1': 'B', 'crew_2': 'D'},
            {'number': 2, 'crew_1': 'S', 'crew_2': 'E'}
    ]
    return render_template('watch_list.html', list_name="Watches", watch_list=watch_list)


@app.route('/param')
def save_param():
    crew_id = str(uuid.uuid1())  # shared by all crew members
    crew_list = [{'name': 'B', 'is_skipper': False}, {'name': 'D', 'is_skipper': False},
                 {'name': 'E', 'is_skipper': False}, {'name': 'S', 'is_skipper': True}]
    for crw in crew_list:
        console_out(f'crw: {crw}')
        cm = CrewMember(name=crw['name'], is_skipper=crw['is_skipper'], crew_id=crew_id)
        db.session.add(cm)
    # db.session.commit()
    param = dict(start_date=dt.datetime(2022, 5, 15), end_date=dt.datetime(2022, 6, 30), watch_duration=4,
                 crew_id=crew_id)
    cr = Crew(**param)
    db.session.add(cr)
    db.session.commit()

    # Read the data back from the DB
    out_param = Crew.query.filter_by(crew_id=crew_id).first()
    console_out(f'DB Result: {out_param}')
    console_out(f'DB Result crew_ID: {out_param.crew_id}')
    crew_list = CrewMember.query.filter_by(crew_id=crew_id).all()
    console_out(f'Crew_List: {crew_list}')
    return render_template('crew_list.html', crew_id=crew_id, param=out_param, crew_list=crew_list)



@app.route('/add', methods=['GET', 'POST'])
def add():
    form = forms.AddTaskForm()
    if form.validate_on_submit():
        t = Task(title=form.title.data, date=dt.utcnow())
        db.session.add(t)
        db.session.commit()
        # print(f'Submitted title: {form.title.data}')
        flash(f"Task {form.title.data} added to Database")
        # return render_template('about.html', form=form, title=form.title.data)
        return (redirect(url_for('index')))
    return render_template('add.html', form=form)


# @app.route('/edit/<int: task_id>')
@app.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get(task_id)
    # print(task)
    if task:
        form = forms.AddTaskForm()
        if form.validate_on_submit():
            task.title = form.title.data
            task.date = dt.utcnow()
            db.session.commit()
            flash('Task has been updated')
            return redirect(url_for('index'))
        else:
            form.title.data = task.title
            return render_template('edit.html', form=form, task_id=task_id)
    else:
        flash('Task not found')
    return redirect(url_for('index'))


@app.route('/delete/<task_id>', methods=['GET', 'POST'])
def delete(task_id):
    task = Task.query.get(task_id)
    # print(task)
    if task:
        form = forms.DeleteTaskForm()
        if form.validate_on_submit():
            db.session.delete(task)
            db.session.commit()
            flash('Task has been deleted')
            return redirect(url_for('index'))
        else:
            return render_template('delete.html', form=form, task_id=task_id, title=task.title)
    else:
        flash('Task not found')
    return redirect(url_for('index'))

#
# @app.route('/basic')
# def basic():
#     print('basic')
#     return render_template('basic.html')
