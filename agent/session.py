from .context import ContextManager

class Session:
    """
    管理一次用户会话的上下文
    """

    def __init__(self, max_messages=5):
        # 保存聊天记录
        self.messages = []

        self.context_manager = ContextManager()



    def add_message(self, message):
        """
        添加一条消息
        """
        self.messages.append(message)

        self.message = (
            self.context_manager.compress(self.messages)
        )


    def get_messages(self):
        """
        获取当前上下文
        """

        return self.messages


    def clear(self):
        """
        清空当前会话
        """

        self.messages = []