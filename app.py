from flask import Flask
from flask import request
app = Flask(__name__)




@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'You want path: %s' % path

# @app.route('/<params>')
# def hello_world(params):  # put application's code here
#     return f'Hello {params}'


@app.errorhandler(404)
def not_found(error):
    print(error)
    return f"error page: {error}",200
    # return error, 404


if __name__ == '__main__':
    app.run()
