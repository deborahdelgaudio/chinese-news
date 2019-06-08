import flask
from models.model_news import ModelNews

app = flask.Flask(__name__)
app.config.from_pyfile('config/config.cfg')

model_news = ModelNews(app.config)

@app.route('/')
def index():
    return flask.jsonify({'Status': 'OK'})

@app.route('/news')
def all_news():
    return flask.jsonify(model_news.get_all_news())

if __name__ == '__main__':
    app.run()