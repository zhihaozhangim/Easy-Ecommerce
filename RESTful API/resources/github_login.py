from flask import request, g    # g: global. (1) only in request (2) per request
from flask_restful import Resource
from schemas.user import UserSchema
from models.user import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token
from oa import github

user_schema = UserSchema()


class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(callback="http://localhost:5000/login/github/authorized")


class GithubAuthorize(Resource):
    # user already permits, send a post request to github to get the request token and then get it
    @classmethod
    def get(cls):
        resp = github.authorized_response()

        if resp is None or resp.get("access_token") is None:
            error_response = {
                "error": request.args["error"],
                "error_description": request.args["error_description"]
            }
            return error_response

        g.access_token = resp['access_token']
        github_user = github.get('user')  # this uses the access_token from the tokengetter function
        github_username = github_user.data['login']

        user = UserModel.query.filter_by(username=github_username).first()

        # we don't the password
        if not user:
            user = UserModel(username=github_username, password=None)
            user.save_to_db()

        # create token
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200
