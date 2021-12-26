from os import name

import datetime as dt


from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.admin import students

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('student', __name__, url_prefix='/student')

@bp.route('/about/<int:mark>')
@login_required
def about(mark):
    db = get_db()
    
    info = db.cursor().execute(
        'SELECT STUDENT.FIRST_NAME, STUDENT.SECOND_NAME, STUDENT.FATHER_NAME, CLASS.NUMBER, CLASS.LITERA, CLASS_GROUP.START_DATE from STUDENT '
        ' join CLASS_GROUP on STUDENT.GROUP_ID = CLASS_GROUP.ID '
        ' join CLASS on CLASS.ID = CLASS_GROUP.CLSS_ID '
        ' where STUDENT.ID = ?',
        
        (g.user['id'], )
    ).fetchall()

    stud = db.cursor().execute(
        'SELECT * from STUDENT'
        ' where STUDENT.ID = ?',
        
        (g.user['id'], )
    ).fetchonemap()

    subj = db.cursor().execute(
        'SELECT SUBJECT.NAME from "PLAN" '
        ' join CLASS on CLASS.ID = "PLAN".CLASS_ID '
        ' join SUBJECT on SUBJECT.ID = "PLAN".SUBJECT_ID '
        ' join CLASS_GROUP on CLASS_GROUP.CLSS_ID = CLASS.ID '
        ' join STUDENT on STUDENT.GROUP_ID = CLASS_GROUP.ID '
        ' where STUDENT.ID = ?',    
        (g.user['id'], )
    ).fetchall()


    marks = db.cursor().execute(
        'select MARK.MARK, SUBJECT.NAME, MARK.DATE_MARK, MARK.ID from MARK '
        ' join "PLAN" on "PLAN".ID = MARK.PLAN_ID '
        ' join STUDENT on STUDENT.ID = MARK.STUD_ID '
        ' join SUBJECT on SUBJECT.ID = "PLAN".SUBJECT_ID '
        ' where STUDENT.ID = ? and '
        ' extract(YEAR from MARK.DATE_MARK) = extract(YEAR from current_date) '
        ' order by MARK.DATE_MARK DESC',
        (g.user['id'], )
    ).fetchall()


    now = dt.datetime.now()

    datas = []

    if now.month in range (9,11):
        sdate = dt.date(now.year, 9, 1)
        edate = dt.date(now.year, 10, 28)

    if now.month in range (11,13):
        sdate = dt.date(now.year, 11, 4)
        edate = dt.date(now.year, 12, 23)

    if now.month in range (1,4):
        sdate = dt.date(now.year, 1, 7)
        edate = dt.date(now.year, 3, 21)



    if now.month in range (4,9):
        sdate = dt.date(now.year, 4, 4)
        edate = dt.date(now.year, 5, 31)


    delta = edate - sdate
    for i in range(delta.days + 1):
        tempdata = sdate + dt.timedelta(days=i)
        if tempdata.isoweekday() in range(1,6):
            datas.append(tempdata)


    mark_data = db.cursor().execute(
        'select * from MARK '
        ' join "PLAN" on "PLAN".ID = MARK.PLAN_ID '
        ' join STUDENT on STUDENT.ID = MARK.STUD_ID '
        ' join SUBJECT on SUBJECT.ID = "PLAN".SUBJECT_ID '
        ' where MARK.ID = ?',
        (mark, )
    ).fetchonemap()


    mark_data2 = db.cursor().execute(
    'select * from MARK' 
    ' where MARK.ID = ?',
        (mark, )
    ).fetchonemap()
    return render_template('student/about.html',
     info = info, datas = datas, subj = subj,
     marks = marks, mark = mark_data, stud = stud)