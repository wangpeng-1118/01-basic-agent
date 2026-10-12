from .session import Session

class SessionManager:

    def __init__(self):
        # 保存所有的session
        # key: session_id
        # value: Session对象
        self.sessions = {}

    def create_session(self, session_id):

        self.sessions[session_id] = Session()

    def get_session(self, session_id):
        # 如果不存在，则创建
        if session_id not in self.sessions:
            self.create_session(session_id)

        return self.sessions[session_id]

    def delete_session(self, session_id):

        if session_id in self.sessions:
            del self.sessions[session_id]

    def list_session(self):

        return list(self.sessions.keys())

    
