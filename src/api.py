import flask

app = flask.Flask(__name__)
#app.config.from_pyfile('config/config.cfg')
#istantiate chinese_news.ModelNews() with config dict

@app.route('/')
def index():
    return "Hello Gabri!"


if __name__ == "__main__":
    app.run()