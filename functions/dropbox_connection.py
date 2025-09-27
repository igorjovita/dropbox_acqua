import dropbox

import os
from functions.refresh_token import get_refresh_token
from dotenv import load_dotenv

def dropbox_connection():
    load_dotenv()

    APP_KEY = os.getenv("DROPBOX_APP_KEY")
    APP_SECRET = os.getenv("DROPBOX_APP_SECRET")
    REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN")


    # RODAR APENAS NO PRIMEIRO ACESSO
    # get_refresh_token(APP_KEY, APP_SECRET)



    dbx = dropbox.Dropbox(
        oauth2_refresh_token=REFRESH_TOKEN,
        app_key=APP_KEY,
        app_secret=APP_SECRET
    )

    return dbx