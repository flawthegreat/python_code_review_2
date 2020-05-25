from enum import Enum
from code_manager import CodeType


class Request:
    class Type(Enum):
        generate = 0
        read = 1

    def __init__(self, request_type: Type, code_type: CodeType, data: str):
        self.type = request_type
        self.code_type = code_type
        self.data = data

    @property
    def description(self) -> str:
        return f'{"Generated" if self.type == self.Type.generate else "Read"}' \
            f' {self.code_type.value} code with data: "{self.data}"'


class Session:
    def __init__(self, id: int):
        self.id = id
        self.request_history = []


class SessionManager:
    def __init__(self):
        self.__free_id = 0
        self.__active_sessions = {}

    def create_new_session(self) -> int:
        session = Session(self.__free_id)
        self.__free_id += 1

        self.__active_sessions[session.id] = session

        return session.id

    def terminate_session(self, session_id: int):
        self.__check_if_session_exists(session_id)

        del self.__active_sessions[session_id]

    def add_request_to_history(self, session_id: int, request: Request):
        self.__check_if_session_exists(session_id)

        self.__active_sessions[session_id].request_history.append(request)

    def session_history(self, session_id: int) -> str:
        self.__check_if_session_exists(session_id)

        return '\n'.join(
            request.description
            for request in self.__active_sessions[session_id].request_history
        )

    def clear_session_history(self, session_id: int):
        self.__check_if_session_exists(session_id)

        self.__active_sessions[session_id].request_history.clear()

    def __check_if_session_exists(self, session_id: int):
        if session_id not in self.__active_sessions.keys():
            raise ValueError(f'Session {session_id} does not exist')
