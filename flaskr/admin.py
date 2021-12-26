from os import error, name

import datetime as dt
import re
import transliterate
import random
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.auth import login_required, admin_required
from flaskr.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/main')
@login_required
@admin_required
def main():
    db = get_db()


    return render_template('admin/main.html')



@bp.route('/teachers')
@login_required
@admin_required
def teachers():
    db = get_db()
    teacher = db.cursor().execute(
    'select *'
    ' FROM TEACHER',
        ( )
    ).fetchallmap()


    return render_template('admin/teachers.html', teacher = teacher)

@bp.route('/teachers/delete/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def delete_teacher(id):
    db = get_db()
    
    db.cursor().execute('DELETE FROM TEACHER WHERE id = ?', (id,))
    
    db.commit()
    return redirect(url_for('admin.teachers'))


@bp.route('/teachers/create/', methods=('POST','GET'))
@login_required
@admin_required
def create_teacher():
    db = get_db()
    if request.method == 'POST':
        f_name = request.form['first_name']
        s_name = request.form['second_name']
        fa_name = request.form['father_name']
        db.cursor().execute(
                'INSERT into TEACHER (FIRST_NAME, SECOND_NAME, FATHER_NAME) '
                ' values (?,?,?)',
                (f_name, s_name, fa_name)
            ) 

        db.commit()
        return redirect(url_for('admin.teachers'))
    return render_template('admin/teachers_add.html')

@bp.route('/teachers/update/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def update_teacher(id):
    db = get_db()
    teacher = db.cursor().execute(
    'SELECT * FROM TEACHER where id = ?',
        (id, )
    ).fetchonemap()
    if request.method == 'POST':
        f_name = request.form['first_name']
        s_name = request.form['second_name']
        fa_name = request.form['father_name']
        
        db.cursor().execute(
            'UPDATE TEACHER '
            ' SET TEACHER.FIRST_NAME = ?,  TEACHER.SECOND_NAME = ?, TEACHER.FATHER_NAME = ?'
            ' WHERE TEACHER.ID = ? ',
                (f_name, s_name, fa_name, id)
            )

        db.commit()
        return redirect(url_for('admin.teachers'))
    return render_template('admin/teachers_update.html', teacher = teacher)


@bp.route('/subjects')
@login_required
@admin_required
def subjects():
    db = get_db()
    sub = db.cursor().execute(
    'SELECT * FROM SUBJECT',
        ( )
    ).fetchallmap()
    return render_template('admin/subjects.html', subs = sub )

@bp.route('/subjects/delete/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def delete_sub(id):
    db = get_db()
    db.cursor().execute('DELETE FROM SUBJECT WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('admin.subjects'))

@bp.route('/subjects/create/', methods=('POST','GET'))
@login_required
@admin_required
def create_sub():
    db = get_db()
    if request.method == 'POST':
        name_sub = request.form['name_sub']
        
        db.cursor().execute(
                'INSERT into SUBJECT (NAME) '
                ' values (?)',
                (name_sub,)
            )

        db.commit()
        return redirect(url_for('admin.subjects'))
    return render_template('admin/subjects_add.html')

@bp.route('/subjects/update/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def update_sub(id):
    db = get_db()
    sub = db.cursor().execute(
    'SELECT * FROM SUBJECT where id = ?',
        (id, )
    ).fetchonemap()
    if request.method == 'POST':
        name_sub = request.form['name_sub']
        
        db.cursor().execute(
            'UPDATE SUBJECT '
            ' SET SUBJECT.NAME = ? '
            ' WHERE SUBJECT.ID = ? ',
                (name_sub, id)
            )

        db.commit()
        return redirect(url_for('admin.subjects'))
    return render_template('admin/subjects_update.html', sub = sub)

@bp.route('/classes')
@login_required
@admin_required
def classes():
    db = get_db()
    clas = db.cursor().execute(
    'SELECT * FROM CLASS',
        ( )
    ).fetchallmap()

    return render_template('admin/classes.html', classes = clas)



@bp.route('/classes/delete/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def delete_classes(id):
    db = get_db()
    db.cursor().execute('DELETE FROM CLASS WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('admin.classes'))

@bp.route('/classes/create/', methods=('POST','GET'))
@login_required
@admin_required
def create_classes():
    db = get_db()
    if request.method == 'POST':
        lit = request.form['lit']
        num = request.form['num']
        if type(lit) is int:
            error = "oh"
        db.cursor().execute(
                'INSERT into CLASS (NUMBER, LITERA) '
                ' values (?, ?)',
                (num, lit)
            )

        db.commit()
        return redirect(url_for('admin.classes'))
    return render_template('admin/classes_add.html')

@bp.route('/classes/update/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def update_classes(id):
    db = get_db()
    clas = db.cursor().execute(
    'SELECT * FROM CLASS where id = ?',
        (id, )
    ).fetchonemap()
    if request.method == 'POST':
        lit = request.form['lit']
        num = request.form['num']
        
        db.cursor().execute(
            'UPDATE CLASS '
            ' SET CLASS.LITERA = ?, CLASS.NUMBER = ?'
            ' WHERE CLASS.ID = ? ',
                (lit, num, id)
            )

        db.commit()
        return redirect(url_for('admin.classes'))
    return render_template('admin/classes_update.html', clas = clas)


@bp.route('/groups')
@login_required
@admin_required
def groups():
    db = get_db()
    groups = db.cursor().execute(
    'SELECT * FROM CLASS_GROUP',
        ( )
    ).fetchallmap()
    cls = db.cursor().execute(
    'SELECT * FROM CLASS',
        ( )
    ).fetchallmap()

    return render_template('admin/groups.html', groups = groups, cls = cls)


@bp.route('/groups/delete/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def delete_groups(id):
    db = get_db()
    db.cursor().execute('DELETE FROM CLASS_GROUP WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('admin.groups'))

@bp.route('/groups/create/', methods=('POST','GET'))
@login_required
@admin_required
def create_groups():
    db = get_db()
    cls = db.cursor().execute(
    'SELECT * FROM CLASS ',
        ( )
    ).fetchallmap()
    if request.method == 'POST':
        date = request.form['date']
        clid = request.form['clid']
        if clid == "":
            db.cursor().execute(
                'INSERT into CLASS_GROUP (START_DATE, CLSS_ID) '
                ' values (?, ?)',
                (date, None)
            )
        else:
            try:
                db.cursor().execute(
                'INSERT into CLASS_GROUP (START_DATE, CLSS_ID) '
                ' values (?, ?)',
                (date, clid)
                )
            except:
                error = 'Этот класс уже занят другой группой' 
                flash(error)   
        db.commit()
        return redirect(url_for('admin.groups'))
    return render_template('admin/groups_add.html', cls = cls)

@bp.route('/groups/update/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def update_groups(id):
    db = get_db()
    group = db.cursor().execute(
    'SELECT * FROM CLASS_GROUP where id = ?',
        (id, )
    ).fetchonemap()

    cls = db.cursor().execute(
    'SELECT * FROM CLASS ',
        ( )
    ).fetchallmap()

    if request.method == 'POST':
        date = request.form['date']
        clid = request.form['clid']
        if clid == "":
            db.cursor().execute(
            'UPDATE CLASS_GROUP '
            ' SET CLASS_GROUP.START_DATE = ?, CLASS_GROUP.CLSS_ID = ?'
            ' WHERE CLASS_GROUP.ID = ? ',
                (date, None, id)
            )
        else:
            try:
                db.cursor().execute(
                'UPDATE CLASS_GROUP '
                ' SET CLASS_GROUP.START_DATE = ?, CLASS_GROUP.CLSS_ID = ?'
                ' WHERE CLASS_GROUP.ID = ? ',
                    (date, clid, id)
                )
            except:
                error = 'Этот класс уже занят другой группой'
                flash(error)

        db.commit()
        return redirect(url_for('admin.groups'))
    return render_template('admin/groups_update.html', cls = cls, group = group)


@bp.route('/students')
@login_required
@admin_required
def students():
    db = get_db()
    groups = db.cursor().execute(
    'SELECT CG.ID as ID, C.ID as CID, C.LITERA, C.NUMBER  FROM CLASS_GROUP CG join CLASS C on CG.CLSS_ID = C.ID',
        ( )
    ).fetchallmap()
    students = db.cursor().execute(
    'SELECT * FROM STUDENT',
        ( )
    ).fetchallmap()


    return render_template('admin/students.html', group = groups, students = students)

@bp.route('/students/delete/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def delete_students(id):
    db = get_db()
    db.cursor().execute('DELETE FROM STUDENT WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('admin.students'))

@bp.route('/students/create/', methods=('POST','GET'))
@login_required
@admin_required
def create_students():
    db = get_db()
    cls = db.cursor().execute(
    'SELECT C.LITERA, C.NUMBER, CG.ID FROM CLASS C join CLASS_GROUP CG on C.ID = CG.CLSS_ID '
    ' WHERE EXISTS(SELECT * FROM CLASS_GROUP WHERE CG.CLSS_ID = C.ID) ',
        ( )
    ).fetchallmap()
    if request.method == 'POST':
        clid = request.form['clid']
        f_name = request.form['first_name']
        s_name = request.form['second_name']
        fa_name = request.form['father_name']
        if clid == "":
            db.cursor().execute(
                'INSERT into STUDENT (FIRST_NAME, SECOND_NAME, FATHER_NAME, GROUP_ID) '
                ' values (?, ?, ?, ?)',
                (f_name, s_name, fa_name, None)
            )
        else:
            db.cursor().execute(
                'INSERT into STUDENT (FIRST_NAME, SECOND_NAME, FATHER_NAME, GROUP_ID) '
                ' values (?, ?, ?, ?)',
                (f_name, s_name, fa_name, clid)
            )

        db.commit()
        return redirect(url_for('admin.students'))
    return render_template('admin/students_add.html', cls = cls)

@bp.route('/students/update/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def update_students(id):
    db = get_db()
    cls = db.cursor().execute(
    'SELECT C.LITERA, C.NUMBER, CG.ID FROM CLASS C join CLASS_GROUP CG on C.ID = CG.CLSS_ID '
    ' WHERE EXISTS(SELECT * FROM CLASS_GROUP WHERE CG.CLSS_ID = C.ID) ',
        ( )
    ).fetchallmap()
    student = db.cursor().execute(
    'SELECT * FROM student where id = ?',
        (id, )
    ).fetchonemap()

    if request.method == 'POST':
        clid = request.form['clid']
        f_name = request.form['first_name']
        s_name = request.form['second_name']
        fa_name = request.form['father_name']
        if clid == "":
            db.cursor().execute(
                'UPDATE  STUDENT ' 
                ' SET FIRST_NAME = ?, SECOND_NAME = ?, FATHER_NAME = ?, GROUP_ID = ?',
                'where STUDENT.ID = ?',
                (f_name, s_name, fa_name, clid, id)
            )
        else:
            db.cursor().execute(
                'UPDATE  STUDENT ' 
                ' SET FIRST_NAME = ?, SECOND_NAME = ?, FATHER_NAME = ?, GROUP_ID = ? '
                'where STUDENT.ID = ?',
                (f_name, s_name, fa_name, clid, id)
            )



        db.commit()
        return redirect(url_for('admin.students'))
    return render_template('admin/students_update.html', student = student, cls = cls)


@bp.route('/plan')
@login_required
@admin_required
def plan():
    db = get_db()
    plan = db.cursor().execute(
    ' SELECT P.ID, C.ID as C_ID, C.LITERA, C.NUMBER, '
    ' T.ID as T_ID, T.FIRST_NAME, T.SECOND_NAME, T.FATHER_NAME, ' 
    ' S.ID as S_ID, S.NAME '
    ' FROM "PLAN" P '
    ' join CLASS C on C.ID = P.CLASS_ID '
    ' join TEACHER T on T.ID = P.TEACHER_ID '
    ' join SUBJECT S on S.ID = P.SUBJECT_ID '
    ).fetchallmap()

    return render_template('admin/plan.html', plan = plan)


@bp.route('/plan/delete/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def delete_plan(id):
    db = get_db()
    db.cursor().execute('DELETE FROM "PLAN" WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('admin.plan'))

@bp.route('/plan/create/', methods=('POST','GET'))
@login_required
@admin_required
def create_plan():
    db = get_db()
    cls = db.cursor().execute(
    'SELECT * FROM CLASS',
        ( )
    ).fetchallmap()
    subj = db.cursor().execute(
    'SELECT * FROM SUBJECT',
        ( )
    ).fetchallmap()
    teachers = db.cursor().execute(
    'SELECT * FROM TEACHER',
        ( )
    ).fetchallmap()
    if request.method == 'POST':
        teacher = request.form['teacher']
        subject = request.form['subject']
        cls = request.form['cls']
        
        db.cursor().execute(
            'INSERT into "PLAN" (CLASS_ID, SUBJECT_ID, TEACHER_ID) '
            ' values (?, ?, ?)',
            (cls, subject, teacher)
        )

        db.commit()
        return redirect(url_for('admin.plan'))
    return render_template('admin/plan_add.html', cls = cls, teachers = teachers, subj = subj)

@bp.route('/plan/update/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def update_plan(id):
    db = get_db()
    cls = db.cursor().execute(
    'SELECT * FROM CLASS',
        ( )
    ).fetchallmap()
    subj = db.cursor().execute(
    'SELECT * FROM SUBJECT',
        ( )
    ).fetchallmap()
    teachers = db.cursor().execute(
    'SELECT * FROM TEACHER',
        ( )
    ).fetchallmap()
    plan = db.cursor().execute(
    'SELECT * FROM "PLAN" where id = ?',
        (id, )
    ).fetchonemap()

    if request.method == 'POST':
        teacher = request.form['teacher']
        subject = request.form['subject']
        cls = request.form['cls']

        db.cursor().execute(
            'UPDATE  "PLAN" ' 
            ' SET CLASS_ID = ?, SUBJECT_ID = ?, TEACHER_ID = ?'
            'where "PLAN".ID = ?',
            (cls, subject, teacher, id)
            )

        db.commit()
        return redirect(url_for('admin.plan'))
    return render_template('admin/plan_update.html', cls = cls, teachers = teachers, subj = subj, plan = plan)























@bp.route('/users')
@login_required
@admin_required
def users():
    db = get_db()
    users_st = db.cursor().execute(
    ' SELECT * FROM USERS join STUDENT on STUDENT.ID = USERS.USER_ID where USERS.ROLE = 1 ',
    ).fetchallmap()

    users_te = db.cursor().execute(
    ' SELECT * FROM USERS join TEACHER on TEACHER.ID = USERS.USER_ID where USERS.ROLE = 2 ',
    ).fetchallmap()

    return render_template('admin/users.html', users_st = users_st, users_te = users_te)



@bp.route('/users/delete/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def delete_users(id):
    db = get_db()
    db.cursor().execute('DELETE FROM USERS WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('admin.users'))


def test_username(username, usernames_test):
    for i in usernames_test:
        if username == i['USERNAME']:
            username = username + 'NEW'
            username = test_username(username, usernames_test)
    return username



@bp.route('/users/create/<int:role>', methods=('POST','GET'))
@login_required
@admin_required
def create_users(role):
    db = get_db()
    if role == 1:
        not_usr = db.cursor().execute(
        'SELECT * FROM STUDENT WHERE '
        ' NOT EXISTS(SELECT * FROM USERS WHERE USERS.USER_ID = STUDENT.ID)',
            ( )
        ).fetchallmap()

        if request.method == 'POST':
            usr_id = request.form['usr_id']
            temp_info = db.cursor().execute(
                'SELECT * FROM STUDENT WHERE ID = ?',
                (usr_id, )
            ).fetchonemap()

            username = transliterate.translit(str(temp_info['FIRST_NAME'])
             + str(temp_info['SECOND_NAME'])[0]
             + str(temp_info['FATHER_NAME'])[0] + str(temp_info['ID']) + str(temp_info['GROUP_ID']), reversed=True)
            usernames_test = db.cursor().execute(
                'SELECT * FROM users',
                ( )
            ).fetchallmap()
            username = test_username(username, usernames_test)

            password = ''            
            for x in range(6): #Количество символов (16)
                password = password + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ')) #Символы, из которых будет составлен пароль
            new_user = [[temp_info['FIRST_NAME'], temp_info['SECOND_NAME'], temp_info['FATHER_NAME'], username, password, 'Ученик'],]
            print(new_user)
            db.cursor().execute(
               'INSERT into users (USER_ID, USERNAME, PASSWORD, ROLE) '
               ' values (?, ?, ?, ?)',
               (usr_id, username, generate_password_hash(password), 1)
            )

            db.commit()

            return render_template('admin/users_list_new.html', new_user = new_user)
    
    
    if role == 2:
        not_usr = db.cursor().execute(
        'SELECT * FROM TEACHER WHERE '
        ' NOT EXISTS(SELECT * FROM USERS WHERE USERS.USER_ID = TEACHER.ID)',
            ( )
        ).fetchallmap()

        if request.method == 'POST':
            usr_id = request.form['usr_id']
            temp_info = db.cursor().execute(
                'SELECT * FROM TEACHER WHERE ID = ?',
                (usr_id, )
            ).fetchonemap()

            username = transliterate.translit(str(temp_info['FIRST_NAME'])
             + str(temp_info['SECOND_NAME'])[0]
             + str(temp_info['FATHER_NAME'])[0] + str(temp_info['ID']), reversed=True)
            usernames_test = db.cursor().execute(
                'SELECT * FROM users',
                ( )
            ).fetchallmap()
            username = test_username(username, usernames_test)

            password = ''            
            for x in range(6): #Количество символов (16)
                password = password + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ')) #Символы, из которых будет составлен пароль
            new_user = [[temp_info['FIRST_NAME'], temp_info['SECOND_NAME'], temp_info['FATHER_NAME'], username, password, 'Учитель'],]
            print(new_user)
            db.cursor().execute(
               'INSERT into users (USER_ID, USERNAME, PASSWORD, ROLE) '
               ' values (?, ?, ?, ?)',
               (usr_id, username, generate_password_hash(password), 2)
            )

            db.commit()       
            return render_template('admin/users_list_new.html', new_user = new_user)
    return render_template('admin/users_add.html', not_usr = not_usr)


@bp.route('/users/update/<int:id>', methods=('POST','GET'))
@login_required
@admin_required
def update_users(id):
    db = get_db()
    
    user = db.cursor().execute(
    'SELECT * FROM users where id = ?',
        (id, )
    ).fetchonemap()


    if user['ROLE'] == 1:

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            db.cursor().execute(
                'UPDATE  users ' 
                ' SET username = ?, password = ?, role = ?'
                'where USERS.ID = ?',
               (username, generate_password_hash(password), 1, id)
               )

            db.commit()
            return redirect(url_for('admin.users'))
    if user['ROLE'] == 2:

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']


            db.cursor().execute(
                'UPDATE  users ' 
                ' SET username = ?, password = ?, role = ?'
                'where USERS.ID = ?',
               (username, generate_password_hash(password), 2, id)
               )

            db.commit()
            return redirect(url_for('admin.users'))
    return render_template('admin/users_update.html', user = user)

