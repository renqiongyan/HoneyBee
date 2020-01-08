from flask import render_template

from application import create_app

app = create_app('development')


@app.route('/')
def app_home_index():
    return render_template('home/index.html')


if __name__ == '__main__':
    app.run()
