# Example CI server that serves badges

from flask import Flask
import pybadges

app = Flask(__name__)


@app.route('/')
def serveBadges():
    # First example
    badge_arg = dict(
        left_text='build',
        right_text='passing',
        right_color='#008000'
    )
    badge = pybadges.badge(**badge_arg)

    # Second example
    secondBadge = pybadges.badge('chat', 'online')

    return badge + "\n" + secondBadge


if __name__ == '__main__':
    app.run()
