from ..database.db_manager import DatabaseManager


class ModelNews(object):

    def __init__(self, db_configuration):
        if isinstance(db_configuration, dict):
            self._db_conf = db_configuration
        else:
            raise TypeError('Provide a dict for db configuration')

    def get_all_news(self):
        query = 'SELECT * FROM news ORDER BY date DESC LIMIT 100;'
        with DatabaseManager(self._db_conf) as db:
            all_news = db.fetch_records(query)

        return list(
            map(
                lambda record: dict(
                    id=record[0],
                    title=record[1],
                    description=record[2],
                    image=record[3],
                    url=record[4],
                    source=record[5],
                    date=record[6]
                ),
                all_news
            )
        )

    def get_news_by_id(self, id):
        query = 'SELECT * FROM news WHERE id = %s;'
        with DatabaseManager(self._db_conf) as db:
            input = (id,)
            news = db.fetch_records(query, input)

        if len(news) == 0:
            return None
        else:
            news = news[0]
            return dict(
                id=news[0],
                title=news[1],
                description=news[2],
                image=news[3],
                url=news[4],
                source=news[5],
                date=news[6]
            )

    def create_news(self, news):
        query = 'INSERT INTO news(title,description,image,url,source,date) VALUES (%s,%s,%s,%s,%s,%s);'
        with DatabaseManager(self._db_conf) as db:
            input = tuple(news.values())
            db.update_records(query, input)

    def update_news_val(self, keys, values, id):
        queries =[]
        for k in keys:
            queries.append('UPDATE news SET {k}=%s WHERE id=%s;'.format(k=k))


        with DatabaseManager(self._db_conf) as db:
            i = 0
            for val in values:
                input = (val, id)
                db.update_records(queries[i], input)
                i += 1

    def delete_news_by_id(self, id):
        query = 'DELETE FROM news WHERE id=%s;'
        with DatabaseManager(self._db_conf) as db:
            input = (id,)
            db.update_records(query, input)
