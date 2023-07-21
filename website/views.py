from flask import Flask, Blueprint, render_template, request, flash, jsonify, send_file
from flask_login import login_required,current_user
from .models import Resume, ClientInfo
from . import db 
import json
from io import BytesIO
import sqlite3

views = Blueprint('views',__name__)

allowed = ['doc','docx','pdf']

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    return render_template('home.html',user=current_user)

@views.route('/resume-upload',methods=['GET','POST'])
@login_required
def upload():
    if request.method == 'POST':
        file1 = request.files['file1']
        if not file1:
            flash('Please upload a file to submit.',category='error')
        else:
            if file1.filename.rsplit('.',1)[1].lower() not in allowed:
                flash('Please upload a valid file type.',category='error')
            else:
                full = Resume(
                    resume_name=file1.filename,
                    resume_data=file1.read(),
                    user_id=current_user.id
                )

                yes = Resume.query.filter(Resume.user_id==current_user.id).first()
                if yes:
                    db.session.delete(yes)
                    db.session.commit()

                db.session.add(full)
                db.session.commit()

                flash('Information saved in database.',category='Success')

    connect = sqlite3.connect('instance/database.db')
    c = connect.cursor()
    sql1 = 'SELECT * FROM resume WHERE user_id=' + str(current_user.id)
    c.execute(sql1)
    output = c.fetchall()
    c.close()
    connect.close()

    return render_template('fileupload.html',user=current_user,data=output)

@views.route('/resume_download/<upload_id>')
def resume_download(upload_id):
    upload = Resume.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.resume_data), download_name=upload.resume_name,as_attachment=True)

@views.route('/delete-resume', methods=['POST'])
def delete_res():
    field = json.loads(request.data)
    profileid = field['profileid']
    field = Resume.query.get(profileid)
    if field:
        if field.user_id == current_user.id:
            db.session.delete(field)
            db.session.commit()
    return jsonify({})