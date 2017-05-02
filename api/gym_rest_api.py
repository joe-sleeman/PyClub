from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'user':
        return 'password'


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

exercises = [
    {
        'id': 1,
        'title': u'Bench Press',
        'sets': 4,
        'reps': 8,
        'weight': 20,
        'done': False
    },
    {
        'id': 2,
        'title': u'DB Curls',
        'sets': 4,
        'reps': 8,
        'weight': 15.00,
        'done': False
    },
]

exercise_fields = {
    'title': fields.String,
    'sets': fields.Integer,
    'reps': fields.Integer,
    'weight': fields.Float,
    'done': fields.Boolean,
    'uri': fields.Url('exercise')
}


class ExerciseListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No title provided',
                                   location='json')
        self.reqparse.add_argument('sets', type=int, default=3,
                                   location='json')
        self.reqparse.add_argument('reps', type=int, default=9,
                                   location='json')
        self.reqparse.add_argument('weight', type=float, default=10.00,
                                   location='json')
        super(ExerciseListAPI, self).__init__()

    def get(self):
        return {'exercises': [marshal(x, exercise_fields) for x in exercises]}

    def post(self):
        args = self.reqparse.parse_args()
        exercise = {
            'id': exercises[-1]['id'] + 1,
            'title': args['title'],
            'sets': args['sets'],
            'reps': args['reps'],
            'weight': args['weight']
        }
        exercises.append(exercise)
        return {'exercise': marshal(exercise, exercise_fields)}, 201


class ExerciseAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('sets', type=int, location='json')
        self.reqparse.add_argument('reps', type=int, location='json')
        self.reqparse.add_argument('weight', type=float, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(ExerciseAPI, self).__init__()

    def get(self, id):
        exercise = [ex for ex in exercises if ex['id'] == id]
        if len(exercise) == 0:
            abort(404)
        return {'exercise': marshal(exercise[0], exercise_fields)}

    def put(self, id):
        exercise = [ex for ex in exercises if ex['id'] == id]
        if len(exercise) == 0:
            abort(404)
        exercise = exercise[0]
        args = self.reqparse.parse_args()
        for i, j in args.items():
            if j is not None:
                exercise[i] = j
        return {'exercise': marshal(exercise, exercise_fields)}

    def delete(self, id):
        exercise = [ex for ex in exercises if ex['id'] == id]
        if len(exercise) == 0:
            abort(404)
        exercises.remove(exercise[0])
        return {'result': True}


api.add_resource(ExerciseListAPI, '/gym/api/v1.0/exercises',
                 endpoint='exercises')
api.add_resource(ExerciseAPI, '/gym/api/v1.0/exercises/<int:id>',
                 endpoint='exercise')


if __name__ == '__main__':
    app.run(debug=True)
