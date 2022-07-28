from vedis import Vedis
import config


def get_current_state(user_id):
    with Vedis(config.db_file) as db:
        return db[user_id].decode()


def set_state(user_id, value):
    with Vedis(config.db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False
