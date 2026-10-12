class Session:
    """
    管理一次用户会话的上下文
    """

    def __init__(self, max_messages=20):
        # 保存聊天记录
        self.messages = []

        # 最大保存消息数量
        self.max_messages = max_messages


    def add_message(self, message):
        """
        添加一条消息
        """

        self.messages.append(message)

        # 控制上下文长度
        self.trim()


    def get_messages(self):
        """
        获取当前上下文
        """

        return self.messages


    def trim(self):
        """
        简单的上下文窗口控制

        保留最近 max_messages 条消息
        """

        if len(self.messages) > self.max_messages:

            self.messages = (
                self.messages[-self.max_messages:]
            )


    def clear(self):
        """
        清空当前会话
        """

        self.messages = []