"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import Server.views
import Server.data_views
