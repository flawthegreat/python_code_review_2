import flask
from session_manager import Request, SessionManager
from code_manager import CodeType, CodeManager
import base64
import argparse


DEFAULT_HOST = '::'
DEFAULT_PORT = 8000
DEBUG = False

app = flask.Flask(__name__)
session_manager = SessionManager()


class Response:
    WRONG_FORMAT = {
        'status': 'failed',
        'message': 'Wrong request format',
    }

    SESSION_DOES_NOT_EXIST = {
        'status': 'failed',
        'message': f'Session does not exist',
    }


@app.route('/start_new_session', methods=['POST'])
def start_new_session() -> flask.Response:
    return flask.make_response({
        'status': 'ok',
        'session_id': session_manager.create_new_session(),
    })


@app.route('/terminate_session', methods=['POST'])
def terminate_session() -> flask.Response:
    try:
        session_id = int(flask.request.args['session_id'])
    except:
        return flask.make_response(Response.WRONG_FORMAT)

    try:
        session_manager.terminate_session(session_id)

        return flask.make_response({
            'status': 'ok',
            'message': f'Session {session_id} has been terminated',
        })
    except ValueError:
        return flask.make_response(Response.SESSION_DOES_NOT_EXIST)


@app.route('/generate_code', methods=['GET'])
def generate_code() -> flask.Response:
    try:
        session_id = int(flask.request.args['session_id'])
        code_type = CodeType(flask.request.args['code_type'])
        data = str(flask.request.args['data'])
    except:
        return flask.make_response(Response.WRONG_FORMAT)

    try:
        session_manager.add_request_to_history(
            session_id,
            Request(Request.Type.generate, code_type, data)
        )
    except ValueError:
        return flask.make_response(Response.SESSION_DOES_NOT_EXIST)

    if not CodeManager.data_is_correct(code_type, data):
        return flask.make_response({
            'status': 'failed',
            'message': f'Incorrect code data',
        })

    image_data = CodeManager.generate(code_type, data)

    return flask.make_response({
        'status': 'ok',
        'data': base64.b64encode(image_data).decode('utf-8')
    })


@app.route('/read_code', methods=['GET'])
def read_code() -> str:
    try:
        session_id = int(flask.request.args['session_id'])
        code_type = CodeType(flask.request.args['code_type'])
        image_data = base64.b64decode(flask.request.args['image_data'])
    except:
        return flask.make_response(Response.WRONG_FORMAT)

    decoded_data = CodeManager.read(image_data)
    print('anus', decoded_data)

    try:
        session_manager.add_request_to_history(
            session_id,
            Request(Request.Type.read, code_type, decoded_data)
        )
    except ValueError:
        return flask.make_response(Response.SESSION_DOES_NOT_EXIST)

    return flask.make_response({
        'status': 'ok',
        'data': decoded_data
    })


@app.route('/get_history', methods=['GET'])
def get_history() -> str:
    try:
        session_id = int(flask.request.args['session_id'])
    except:
        return flask.make_response(Response.WRONG_FORMAT)

    try:
        history = session_manager.session_history(session_id)
    except ValueError:
        return flask.make_response(Response.SESSION_DOES_NOT_EXIST)

    return flask.make_response({
        'status': 'ok',
        'data': history
    })


@app.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        session_id = int(flask.request.args['session_id'])
    except:
        return flask.make_response(Response.WRONG_FORMAT)

    try:
        session_manager.clear_session_history(session_id)
    except ValueError:
        return flask.make_response(Response.SESSION_DOES_NOT_EXIST)

    return flask.make_response({
        'status': 'ok',
        'message': f'History for session {session_id} has been cleared'
    })


def parse_address() -> (str, int):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=DEFAULT_HOST)
    parser.add_argument('--port', default=DEFAULT_PORT, type=int)

    arguments = parser.parse_args()

    return arguments.host, arguments.port


def main():
    host, port = parse_address()
    app.run(host, port=port, debug=DEBUG)


if __name__ == '__main__':
    main()
