import requests
import argparse
import sys
import base64


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8000
CODE_TYPES = ['qr', 'code39', 'code128', 'ean']


def show_help():
    print(
        'Commands:\n'
        'help - show this message\n'
        'generate - create new code\n'
        'read - read code\n'
        'history - show request history\n'
        'clear history - clear request history\n'
        'exit - exit the application'
    )


def start_new_session(server_address: str) -> int:
    response = requests.post(f'{server_address}/start_new_session').json()

    if response['status'] != 'ok':
        print('An error has occured during session creation:')
        print(response['message'])
        exit()
    else:
        return int(response['session_id'])


def terminate_session(server_address: str, session_id: int):
    response = requests.post(f'{server_address}/terminate_session', params={
        'session_id': session_id,
    }).json()

    if response['status'] != 'ok':
        print('Could not terminate session:')
        print(response['message'])
        return


def generate_code(
    server_address: str,
    session_id: int,
    code_type: str,
    data: str,
    image_filepath: str
):
    response = requests.get(f'{server_address}/generate_code', params={
        'session_id': session_id,
        'code_type': code_type,
        'data': data,
    }).json()

    if response['status'] != 'ok':
        print('Could not generate code:')
        print(response['message'])
        return

    with open(image_filepath, 'wb') as image_file:
        image_file.write(base64.b64decode(response['data']))
        print(f'Code has been written to {image_filepath}')


def read_code(
    server_address: str,
    session_id: int,
    code_type: str,
    image_filepath: str
) -> str:
    with open(image_filepath, 'rb') as image_file:
        image_data = image_file.read()

        response = requests.get(
            f'{server_address}/read_code',
            params={
                'session_id': session_id,
                'code_type': code_type,
                'image_data': base64.b64encode(image_data).decode('utf-8')
            }
        ).json()

        if response['status'] != 'ok':
            print('Could not read code:')
            print(response['message'])
            return None

        return response['data']


def get_history(server_address: str, session_id: int) -> str:
    response = requests.get(
        f'{server_address}/get_history',
        params={
            'session_id': session_id,
        }
    ).json()

    if response['status'] != 'ok':
        print('Could not get history:')
        print(response['message'])
        return None

    return response['data']


def clear_history(server_address: str, session_id: int):
    response = requests.post(
        f'{server_address}/clear_history',
        params={
            'session_id': session_id,
        }
    ).json()

    if response['status'] != 'ok':
        print('Could not clear history:')
        print(response['message'])
        return


def terminate(server_address: str, session_id: int, add_newline: bool = False):
    if add_newline:
        print()
    command = input('Are you sure you want to exit? [y/n]> ')

    if command == 'y':
        terminate_session(server_address, session_id)
        exit()
    elif command == 'n':
        pass
    else:
        print('Invalid input')
        terminate()


def parse_server_address() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=DEFAULT_HOST)
    parser.add_argument('--port', default=DEFAULT_PORT, type=int)

    arguments = parser.parse_args()

    return f'http://{arguments.host}:{arguments.port}'


def main():
    server_address = parse_server_address()
    session_id = start_new_session(server_address)

    show_help()

    while True:
        try:
            command_name = input('> ')

            if command_name == 'help':
                show_help()
            elif command_name == 'generate':
                code_type = input(
                    f'Enter code type [{"/".join(CODE_TYPES)}]:\n'
                )
                if code_type not in CODE_TYPES:
                    print('Invalid code type')
                    continue

                print('Enter data to encode:')
                data = str(sys.stdin.read())

                filepath = input('\nEnter code filepath:\n')

                generate_code(
                    server_address,
                    session_id,
                    code_type,
                    data,
                    filepath
                )
            elif command_name == 'read':
                code_type = input(
                    f'Enter code type [{"/".join(CODE_TYPES)}]:\n'
                )
                if code_type not in CODE_TYPES:
                    print('Invalid code type')
                    continue

                image_filepath = input('Enter code image filepath:\n')

                code_data = read_code(
                    server_address,
                    session_id,
                    code_type,
                    image_filepath
                )
                if code_data:
                    print(code_data)
            elif command_name == 'history':
                history = get_history(server_address, session_id)
                if history:
                    print(history)
            elif command_name == 'clear history':
                clear_history(server_address, session_id)
            elif command_name == 'exit':
                terminate(server_address, session_id)
            else:
                print('Invalid command')
        except KeyboardInterrupt:
            try:
                terminate(server_address, session_id, True)
            except Exception as exception:
                print(exception)
                terminate_session(server_address, session_id)
                exit()
        except Exception as exception:
            print(exception)
            terminate_session(server_address, session_id)
            exit()


if __name__ == '__main__':
    main()
