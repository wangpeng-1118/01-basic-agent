from agent.session import Session


def main():

    session = Session()


    for i in range(10):

        session.add_message(
            {
                "role":"user",
                "content":f"message {i}"
            }
        )


    messages = session.get_messages()


    print(messages)



if __name__ == "__main__":
    main()