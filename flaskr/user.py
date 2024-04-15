from __future__ import annotations
from typing import Union
import os
import math
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import FileStorage
from flask_login import UserMixin
from sqlalchemy import func
from flaskr import login_manager


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        #self.is_anonymous = True


@login_manager.user_loader
def user_loader(user_id):
    return User(user_id)



