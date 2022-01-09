from flask import Flask
from flask_restful import Resource, Api, reqparse

import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self, userId=""):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        if userId:
            for item in data:
                if userId in item["userId"]:
                    return {'data': item}
                else:
                    return {'error': 'User Not Found'}, 404
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)
        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            return {
                       'message': f"'{args['userId']}' already exists."
                   }, 409
        else:
            new_data = pd.DataFrame({
                'userId': [args['userId']],
                'name': [args['city']],
                'city': [args['name']],
                'vehicles': [[]]
            })
            data = data.append(new_data, ignore_index=True)
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict('records')}, 200

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        parser.add_argument('vehicles', required=True)
        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            # evaluate strings of lists to lists !!! Danger, this should never be done in any prod code!
            data['vehicles'] = data['vehicles'].apply(
                lambda x: ast.literal_eval(x)
            )
            user_data = data[data['userId'] == args['userId']]

            user_data['vehicles'] = user_data['vehicles'].values[0] \
                .append(args['vehicles'])

            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict('records')}, 200

        else:
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            data = data[data['userId'] != args['userId']]

            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict('records')}, 200
        else:
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 404


class Oems(Resource):
    def get(self):
        data = pd.read_csv('oems.csv')
        return {'data': data.to_dict()}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('oemId', required=True, type=int)
        parser.add_argument('name', required=False)
        parser.add_argument('rating', required=True)
        args = parser.parse_args()

        data = pd.read_csv('oems.csv')

        if args['oemId'] in list(data['oemId']):
            return {
                       'message': f"'{args['oemId']}' already exists."
                   }, 409
        else:
            new_data = pd.DataFrame({
                'oemId': [args['oemId']],
                'name': [args['name']],
                'rating': [args['rating']]
            })
            data = data.append(new_data, ignore_index=True)
            data.to_csv('oems.csv', index=False)
            return {'data': data.to_dict()}, 200

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('oemId', required=True, type=int)
        parser.add_argument('name', store_missing=False)
        parser.add_argument('rating', store_missing=False)
        args = parser.parse_args()

        data = pd.read_csv('oems.csv')

        if args['oemId'] in list(data['oemId']):
            user_data = data[data['oemId'] == args['oemId']]

            if 'name' in args:
                user_data['name'] = args['name']
            if 'rating' in args:
                user_data['rating'] = args['rating']

            data[data['oemId'] == args['oemId']] = user_data
            data.to_csv('oems.csv', index=False)
            return {'data': data.to_dict()}, 200

        else:
            return {
                       'message': f"'{args['oemId']}' manufacturer does not exist."
                   }, 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('oemId', required=True, type=int)
        args = parser.parse_args()

        data = pd.read_csv('oems.csv')

        if args['oemId'] in list(data['oemId']):
            data = data[data['oemId'] != args['oemId']]
            data.to_csv('oems.csv', index=False)
            return {'data': data.to_dict()}, 200

        else:
            return {
                'message': f"'{args['oemId']}' manufacturer does not exist."
            }


api.add_resource(Users, '/user', '/user/<userId>')
api.add_resource(Oems, '/manufacturers')

if __name__ == '__main__':
    app.run()  # run Flask app
