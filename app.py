'''
app
'''
from flask import Flask
from flask_graphql import GraphQLView
from models import db_session
from schema import schema
from json import encoder
app = Flask(__name__)
app.debug = True


@app.route("/")
def test():
    query_with_argument = '{ datasetInfo(fileID: "955291fe-a6ac-477a-b587-878d02633f53") { fileName } }'
    result = schema.execute(query_with_argument)
    print(result.data)
    return result.data


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
