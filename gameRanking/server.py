from flask import Flask, request, send_from_directory, send_file, jsonify
from utils import  db

app = Flask(__name__, static_url_path='')


@app.route('/', methods=['GET'])
def index():
    return send_file('static/index.html')

@app.route('/static/<path:path>', methods=['GET'])
def send_static(path):
    return send_from_directory('static', path)

@app.route('/comment/<table_name>/<int:begin_id>/<int:offset>', methods=['GET'])
def get_comment(table_name, begin_id, offset):
    fields = ['id','source','game_name','game_logo_url','score','tags']
    return jsonify(db.get_comment(fields, table_name, begin_id, offset))

@app.route('/last_comment/<table_name>/<int:end_id>/<int:offset>', methods=['GET'])
def last_comment(table_name, end_id, offset):
    fields = ['id','source','game_name','game_logo_url','score','tags']
    return jsonify(db.last_comment(fields, table_name, end_id, offset))

# @app.route('/comment', methods=['POST'])
# def update_comment():
#     j = request.get_json()
#     if 'emotion' in j:
#         field = 'emotion'
#         value = j['emotion']
#     elif 'type' in j:
#         field = 'type'
#         value = j['type']
#     else:
#         return jsonify({'res':'error', 'paras':j})
#     if db.update_comment(j['id'], field, value):
#         return jsonify({'res': 'ok'})   
#     else:
#         return jsonify({'res':'error', 'paras':j})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
