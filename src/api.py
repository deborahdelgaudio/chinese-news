import sys
import flask

sys.path.insert(0, '.')

from src.models.model_news import ModelNews

app = flask.Flask(__name__)
app.config.from_pyfile('config/config.cfg')

model_news = ModelNews(app.config)
news_attributes = (
            'title',
            'description',
            'image',
            'url',
            'source',
            'date'
        )
news_attributes_not_null = tuple(news_attributes[3:])


@app.route('/')
def index():
    return flask.jsonify({'Status': 'OK'})


@app.route('/news', methods=['GET', 'POST'])
def all_news():
    if flask.request.method == 'GET':
        return flask.jsonify(model_news.get_all_news())

    record = flask.request.form.copy().to_dict()

    if len(record) == 0:
        return flask.jsonify([
            {'Status': 'Bad Request'},
            {'Error': 'Record inserted is empty'}
        ]
        ), 400
    else:

        if not all(attribute in record.keys() for attribute in news_attributes):
            return flask.jsonify([
                {'Status': 'Bad Request'},
                {'Error': 'A value is missing'},
                record]
            ), 400
        else:
            if not all(record.get(attribute) for attribute in news_attributes_not_null):
                return flask.jsonify([
                    {'Status': 'Bad Request'},
                    {'Error': 'NOT NULL value is empty'},
                    record]
                ), 400
            else:
                try:
                    model_news.create_news(record)
                except Exception as err:
                    return flask.jsonify([
                        {'Status': 'Bad Request'},
                        {'Error': err.args[1]}]
                    ), 400

                return flask.jsonify({'Status': 'OK'})


@app.route('/news/<int:id>', methods=['GET', 'POST', 'DELETE']) # TODO: use PUT method
def news_by_id(id):

    if flask.request.method == 'GET':
        news = model_news.get_news_by_id(id)

        if news is None:
            return flask.jsonify({'Status': 'Not Found'}), 404

        return flask.jsonify(news)

    if flask.request.method == 'DELETE':
        try:
            model_news.delete_news_by_id(id)
        except Exception as err:
            return flask.jsonify([
                {'Status': 'Bad Request'},
                {'Error': err.args}]
            ), 400

        return flask.jsonify({'Status': 'OK'})

    record = flask.request.form.copy().to_dict()

    if len(record) == 0:
        return flask.jsonify([
            {'Status': 'Bad Request'},
            {'Error': 'No values found'}
        ]
        ), 400

    keys = record.keys()
    values = record.values()

    for k in keys:
        if k in news_attributes_not_null:
            if not record.get(k):
                return flask.jsonify([
                    {'Status': 'Bad Request'},
                    {'Error': 'A NOT NULL field is empty',
                     'Missing value': k
                     },
                ]
                ), 400
            continue
    try:
        model_news.update_news_val(keys, values, id)
    except Exception as err:
        return flask.jsonify([
            {'Status': 'Bad Request'},
            {'Error': err.args}]
        ), 400

    return flask.jsonify({'Status': 'OK'})


if __name__ == '__main__':
    app.run()
