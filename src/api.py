import sys
import flask

sys.path.insert(0, '.')

from src.models.model_news import ModelNews

app = flask.Flask(__name__)
app.config.from_pyfile('config/config.cfg')

model_news = ModelNews(app.config)


@app.route('/')
def index():
    return flask.jsonify({'Status': 'OK'})


@app.route('/news', methods=['GET', 'POST'])
def all_news():
    if flask.request.method == 'GET':
        return flask.jsonify(model_news.get_all_news())
    else:
        record = flask.request.form.copy().to_dict()

        if len(record) == 0:
            return flask.jsonify([{'Status': 'Bad Request'}, {'Error': 'Record inserted is empty'}]), 400
        else:
            if 'url' not in record.keys() or 'source' not in record.keys() or 'date' not in record.keys() or 'title' not in record.keys() or 'description' not in record.keys() or 'image' not in record.keys():
                return flask.jsonify([{'Status': 'Bad Request'}, {'Error': 'A value is missing'}, record]), 400
            else:
                if record['url'] == '' or record['source'] == '' or record['date'] == '':
                    return flask.jsonify([{'Status': 'Bad Request'}, {'Error': 'NOT NULL value is empty'}, record]), 400
                else:
                    try:
                        model_news.create_news(record)
                    except KeyError as key:
                        return flask.jsonify([{'Status': 'Bad Request'}, {'Key Error': key.args}]), 400

                    return flask.jsonify({'Status': 'OK'})


@app.route('/news/<int:id>')
def news_by_id(id):
    news = model_news.get_news_by_id(id)

    if news is None:
        return flask.jsonify({'Status': 'Not Found'}), 404
    else:
        return flask.jsonify(news)


if __name__ == '__main__':
    app.run()
