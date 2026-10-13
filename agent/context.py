class ContextManager:
    
    def __init__(
        self,
        max_messages=20
    ):

        self.max_messages = max_messages

    def compress(self, messages):
        """
        简单上下文压缩

        保留最近消息
        """
        if len(messages) <= self.max_messages:
            return messages

        return messages[-self.max_messages:]