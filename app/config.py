from sqlalchemy import create_engine, MetaData
from configparser import ConfigParser
import os

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLED = True
# TODO: Move to a config file
CSRF_SESSION_KEY = "TOP_SECRET"
SECRET_KEY = "ANOTHER_SECRET"
config = ConfigParser()
config.read(os.path.join(BASE_DIR, os.pardir, 'config.ini'))
conf = {
    'mysql': {
        'user': config.get('mysql', 'user'),
        'pass': config.get('mysql', 'pass'),
        'host': config.get('mysql', 'host'),
        'port': config.get('mysql', 'port'),
        'db': config.get('mysql', 'db'),
    },
}
engine = create_engine(
    'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(
        user=conf['mysql']['user'],
        password=conf['mysql']['pass'],
        host=conf['mysql']['host'],
        port=conf['mysql']['port'],
        db=conf['mysql']['db'],
    )
)
DB_META = MetaData(bind=engine, reflect=True)
ASSESSMENT_TABLE = DB_META.tables['sp_assessments']
NOTIFY_TABLE = DB_META.tables['sp_assessment_notify']
BLACKLIST_TABLE = DB_META.tables['sp_blacklist']
CALLBACK_TABLE = DB_META.tables['sp_callbacks']
HIT_TABLE = DB_META.tables['sp_hits']
USER_TABLE = DB_META.tables['sp_users']
