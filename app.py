from flask import Flask, make_response, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
from group_by_level import group_by_level
load_dotenv()


app = Flask(__name__)
CORS(app)
# app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(12), nullable=False)
    xp = db.Column(db.String(5), nullable=False)
    lang1 = db.Column(db.String(50), nullable=False)
    lang2 = db.Column(db.String(50), nullable=False)
    lang3 = db.Column(db.String(50), nullable=False)
    lang_other = db.Column(db.String(50))
    can_pair = db.Column(db.Boolean, nullable=False, default=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def to_dict(self):
        return {
            'name': self.name,
            'level': self.level,
            'xp': self.xp,
            'lang1': self.lang1,
            'lang2': self.lang2,
            'lang3': self.lang3,
            'lang_other': self.lang_other,
        }

    def __repr__(self):
        return f'<Participant> {self.name}, {self.date_time}'


@app.route("/api/ping", methods=['GET'])
def ping():
    return make_response('Success!', 200)


@app.route("/api/cleanup")
def cleanup():
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    today_dt = datetime(year, month, day)
    Participant.query.filter(Participant.date_time < today_dt).delete()
    db.session.commit()
    return make_response('Success!', 200)


@app.route("/api/participants", methods=['GET'])
def getParticipants():
    if request.method != 'GET':
        return make_response('Malformed request', 400)
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    today_dt = datetime(year, month, day)
    participants = Participant.query.filter(
        Participant.date_time >= today_dt).all()
    headers = {"Content-Type": "application/json"}
    return make_response(jsonify([participant.to_dict for participant in participants]), 200, headers)


@app.route("/api/groups", methods=['GET'])
def getGroups():
    if request.method != 'GET':
        return make_response('Malformed request', 400)
    participants = Participant.query.all()
    # ##############################################################################
    # SORTING ALGORITHM
    # ##############################################################################
    # INITIAL GROUPING BY LANGUAGE AND LEVEL
    beginners = []
    nonbeginners = []
    for participant in participants:
        if participant.level == 1:
            beginners.append(participant)
        else:
            nonbeginners.append(participant)
    beginner_groups = group_by_level(beginners)
    nonbeginner_groups = group_by_level(nonbeginners)
    final_groups = beginner_groups + nonbeginner_groups
    for i in range(len(final_groups)):
        final_groups[i] = [
            participant.to_dict for participant in final_groups[i]]
    headers = {"Content-Type": "application/json",
               "Access-Control-Allow-Origin": "*"}
    return make_response(jsonify(final_groups), 200, headers)


@app.route("/api/join", methods=['POST'])
def join():
    if request.method != 'POST':
        return make_response('Malformed request', 400)
    req_body = request.json
    name = req_body['name']
    level = req_body['level']
    xp = req_body['xp']
    lang1 = req_body['lang1']
    lang2 = req_body['lang2']
    lang3 = req_body['lang3']
    lang_other = req_body['langOther']
    new_participant = Participant(name=name, level=level, xp=xp, lang1=lang1,
                                  lang2=lang2, lang3=lang3, lang_other=lang_other)
    db.session.add(new_participant)
    db.session.commit()
    return make_response(jsonify({"message": "success"}), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})


if __name__ == "__main__":
    app.run()
