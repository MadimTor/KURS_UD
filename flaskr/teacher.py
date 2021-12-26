from os import name

import datetime as dt


from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('teacher', __name__, url_prefix='/teacher')

@bp.route('/subs')
@login_required
def subs():
    db = get_db()
    
    info = db.cursor().execute(
        'select * from TEACHER ' 
        ' where TEACHER.ID = ?', 
        (g.user['id'], )
    ).fetchonemap()

    subs = db.cursor().execute(
        'select DISTINCT SUBJECT.NAME, SUBJECT.ID from TEACHER '
        ' join "PLAN" on TEACHER.ID = "PLAN".TEACHER_ID '
        ' join SUBJECT on SUBJECT.ID = "PLAN".SUBJECT_ID '
        ' where TEACHER.ID = ?',
        (g.user['id'], )
    ).fetchall()


    classes = db.cursor().execute(
        'select  SUBJECT.ID, CLASS.NUMBER, CLASS.LITERA, "PLAN".ID as P_ID from TEACHER'
        ' join "PLAN" on TEACHER.ID = "PLAN".TEACHER_ID'
        ' join SUBJECT on SUBJECT.ID = "PLAN".SUBJECT_ID'
        ' join CLASS on CLASS.ID = "PLAN".CLASS_ID'
        ' where TEACHER.ID = ?',
        (g.user['id'], )
    ).fetchallmap()

    sdate = dt.date(2009, 9, 1)
    edate = dt.date(2010, 5, 31)
    datas = []
    delta = edate - sdate
    for i in range(delta.days + 1):
        datas.append(sdate + dt.timedelta(days=i))

    return render_template('teacher/subs.html', info = info, subs = subs, datas = datas, classes = classes)





@bp.route('/subj/<int:id>/', methods=('GET', 'POST'))
@login_required
def subj(id):
    db = get_db()
    
    id = id
    sub = db.cursor().execute(
    'SELECT SUBJECT.NAME, "PLAN".ID FROM SUBJECT'
    ' join "PLAN" on "PLAN".SUBJECT_ID = SUBJECT.ID '
    ' WHERE "PLAN".ID = ?',
        (id, )
    ).fetchonemap()

    students = db.cursor().execute(
    'SELECT "PLAN".ID as P_ID, CLASS.ID as CL_ID, '
    ' CLASS_GROUP.ID as GR_ID, STUDENT.ID as ST_ID, '
    ' STUDENT.FIRST_NAME, STUDENT.SECOND_NAME, '
    ' STUDENT.FATHER_NAME FROM "PLAN" '
    ' join CLASS on CLASS.ID = "PLAN".CLASS_ID '
    ' join CLASS_GROUP on CLASS_GROUP.CLSS_ID = CLASS.ID '
    ' join STUDENT on CLASS_GROUP.ID = STUDENT.GROUP_ID '
    ' where "PLAN".ID = ? '
    ' order by STUDENT.SECOND_NAME ',
        (id, )
    ).fetchallmap()

    marks = db.cursor().execute(
    'SELECT MARK.ID, MARK.MARK, STUDENT.ID as ST_ID, MARK.DATE_MARK, MARK.TYPE_MARK FROM MARK '
    ' join "PLAN" on "PLAN".ID = MARK.PLAN_ID '
    ' join STUDENT on STUDENT.ID = MARK.STUD_ID '
    ' WHERE "PLAN".ID = ?',
        (id, )
    ).fetchallmap()

    now = dt.datetime.now()

    datas = []
    year = None
    if now.month in range (9,11):
        sdate = dt.date(now.year, 9, 1)
        edate = dt.date(now.year, 10, 27)
        quad = dt.date(now.year, 10, 28)

    if now.month in range (11,13):
        sdate = dt.date(now.year, 11, 4)
        edate = dt.date(now.year, 12, 22)
        quad = dt.date(now.year, 12, 23)

    if now.month in range (1,4):
        sdate = dt.date(now.year, 1, 7)
        edate = dt.date(now.year, 3, 20)
        quad = dt.date(now.year, 3, 21)

    if now.month in range (4,9):
        sdate = dt.date(now.year, 4, 4)
        edate = dt.date(now.year, 5, 29)
        quad = dt.date(now.year, 5, 30)
        year = dt.date(now.year, 5, 31)




    delta = edate - sdate
    for i in range(delta.days + 1):
        tempdata = sdate + dt.timedelta(days=i)
        if tempdata.isoweekday() in range(1,6):
            datas.append(tempdata)
    datas.append(quad)
    return render_template('teacher/subj.html', students = students, datas = datas, marks = marks, sub = sub, quad = quad, year = year)



@bp.route('/create/<date>/<plan_id>/<student_id>/<mark_type>', methods=('GET', 'POST'))
@login_required
def create(date, plan_id, student_id, mark_type):
    db = get_db()
    sub = db.cursor().execute(
    'SELECT SUBJECT.NAME, "PLAN".ID FROM SUBJECT'
    ' join "PLAN" on "PLAN".SUBJECT_ID = SUBJECT.ID '
    ' WHERE "PLAN".ID = ?',
        (plan_id, )
    ).fetchonemap()

    student = db.cursor().execute(
    'SELECT STUDENT.FIRST_NAME, STUDENT.SECOND_NAME FROM STUDENT'
    ' WHERE STUDENT.ID = ?',
        (student_id, )
    ).fetchonemap()

    mark = None
    if request.method == 'POST':
        mark = request.form.getlist('mark')


        comment = request.form['comment']
        
        db.cursor().execute(
                'INSERT into MARK (MARK.STUD_ID, MARK.PLAN_ID, MARK.DATE_MARK, MARK.MARK, MARK.TYPE_MARK, MARK.COMMENT_FOR_MARK) '
                ' values (?, ?, ?, ?, ?, ?) ',
                (student_id, plan_id, date, mark[0], mark_type, comment)
            )
        db.commit()
        return redirect(url_for('teacher.subj', id = plan_id))


    return render_template('teacher/create.html', sub = sub, date = date, student = student, mark = mark)



@bp.route('/edit/<plan_id>/<student_id>/<mark_id>/', methods=('GET', 'POST'))
@login_required
def edit(plan_id, student_id, mark_id):
    db = get_db()
    sub = db.cursor().execute(
    'SELECT SUBJECT.NAME, "PLAN".ID FROM SUBJECT'
    ' join "PLAN" on "PLAN".SUBJECT_ID = SUBJECT.ID '
    ' WHERE "PLAN".ID = ?',
        (plan_id, )
    ).fetchonemap()

    mark = db.cursor().execute(
    'SELECT * FROM MARK'
    ' WHERE MARK.ID = ?',
        (mark_id, )
    ).fetchonemap()

    student = db.cursor().execute(
    'SELECT STUDENT.FIRST_NAME, STUDENT.SECOND_NAME FROM STUDENT'
    ' WHERE STUDENT.ID = ?',
        (student_id, )
    ).fetchonemap()

    if request.method == 'POST':
        mark = request.form.getlist('mark')
        comment = request.form['comment']
        
        db.cursor().execute(
            'UPDATE MARK '
            ' SET MARK.MARK = ?, MARK.COMMENT_FOR_MARK = ? '
            ' WHERE MARK.ID = ? '
               ,
               (mark[0], comment, mark_id)
            )
        db.commit()
        return redirect(url_for('teacher.subj', id = plan_id))


    return render_template('teacher/edit.html', sub = sub, mark = mark, student = student)
