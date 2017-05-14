import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
os.environ["DEBUG"] = "True"

from webapp.app import app
app.run(debug=True)
