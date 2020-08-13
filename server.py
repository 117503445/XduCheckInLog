from flask import Flask, escape, request, render_template, jsonify
import flask_sqlalchemy
import time
import json
import file_util
app = Flask("XDU_Check_In")
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'

dir_data = 'data'
db = flask_sqlalchemy.SQLAlchemy(app)


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(64),name='studentid')
    message = db.Column(db.String(64))
    checktime = db.Column(db.Integer)

    def __init__(self, student_id, message):
        self.student_id = student_id
        self.message = message
        self.checktime = int(round(time.time()))


def init():
    file_util.create_dir_if_not_exist(dir_data)
    db.create_all()


@app.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html')


@app.route('/index.js', methods=['get'])
def get_js():
    return render_template('index.js')

@app.route('/api/log', methods=['post'])
def commit_data_with_log():
    js = request.get_json(force=True)

    log = Log(js['student_id'],js['message'])
    db.session.add(log)
    db.session.commit()

    return "success"


def main():
    init()
    app.run(host='0.0.0.0', port='80')


if __name__ == "__main__":
    main()
