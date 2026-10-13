from agent.context import ContextManager

def main():

    context = ContextManager(
        max_messages=5
    )

    messages = []

    for i in range(10):
        
        messages.append(
            {
                "role": "user",
                "content": f"message {i}"
            }
        )

    messages = context.compress(messages)

    print(messages)

if __name__ =="__main__":
    main()

# import sys
# print(sys.path)
