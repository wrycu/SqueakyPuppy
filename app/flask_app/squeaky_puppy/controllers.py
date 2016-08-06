from flask import Blueprint, render_template, Response, request
from app import config

squeaky_puppy = Blueprint(
    'squeaky_puppy',
    __name__,
)


@squeaky_puppy.route('/')
def home():
        return render_template(
            'base.html'
        )
