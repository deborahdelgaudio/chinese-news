from src.database.db_manager import DatabaseManager

class ModelNews(object):

    def __init__(self, db_configuration):
        if isinstance(db_configuration, dict):
            self._db_conf = db_configuration
        else:
            raise TypeError("Provide a dict for db configuration")

    def get_all_news(self):
        query = "SELECT * FROM news ORDER BY date DESC LIMIT 100;"
        with DatabaseManager(self._db_conf) as db:
            all_news = db.execute_query(query)
        return all_news

    def get_news_by_id(self,id):
        pass

    def create_news(self, news):
        pass

    def update_news_val(self,val):
        pass

    def delete_news_by_id(self, id):
        pass