import flask
import request as urlrequest 
import json

from mysqlconnect import *

app = flask.Flask(__name__)

@app.route("/")


def output(status_code, status, message=None):
    result = {
               "status_code": status_code,
               "status": status,
               "data": []
             }
    if message:
        result['message'] = message
    return result

@app.route("/api/external-books")
def get_book():
    url = "https://www.anapioficeandfire.com/api/books"
    book_name =flask.request.args.get('name')
    if book_name:
        url = "https://www.anapioficeandfire.com/api/books?name={}".format(book_name)
        response = urlrequest.get(url)
        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            if data:
                result = output(response.status_code, "success")
                result['data'].append({
                         "name": data[0].get("name"),
                         "authors": data[0].get("authors"),
                        })
                return flask.jsonify(result)
            else:
                return flask.jsonify(output(response.status_code, "success"))
        else:
            return "External Api returned error :{}".format(response.status_code)
    else:
        return "Please provide a valid Book name"

