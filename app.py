import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ChoiceType
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView


db = SQLAlchemy()


COLOR_CHOICES = [
    ('r', 'Red'),
    ('g', 'Green'),
    ('b', 'Blue'),
]


class Widget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    color = db.Column(ChoiceType(COLOR_CHOICES))


class WidgetType(SQLAlchemyObjectType):
    class Meta:
        model = Widget
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    widgets = SQLAlchemyConnectionField(WidgetType)


schema = graphene.Schema(query=Query, types=[WidgetType])


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

# Add some CLI commands, for ease of setup

@click.group('db')
def db_group():
    pass

@db_group.command('create')
@with_appcontext
def db_create():
    db.create_all()

@db_group.command('seed')
@with_appcontext
def db_seed():
    w1 = Widget(name="one", color="r")
    w2 = Widget(name="two", color="g")
    w3 = Widget(name="three", color="b")
    db.session.add_all([w1, w2, w3])
    db.session.commit()

app.cli.add_command(db_group)
