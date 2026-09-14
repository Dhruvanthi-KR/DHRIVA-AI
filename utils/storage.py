import json
import os


CHAT_FOLDER = "data/chats"


def create_chat_folder(user_id):
    user_folder = os.path.join(
        CHAT_FOLDER,
        str(user_id)
    )

    os.makedirs(
        user_folder,
        exist_ok=True
    )

    return user_folder


def save_chat(user_id, chat_id, chat_data):
    user_folder = create_chat_folder(user_id)

    file_path = os.path.join(
        user_folder,
        f"{chat_id}.json"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            chat_data,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_chat(user_id, chat_id):
    user_folder = create_chat_folder(user_id)

    file_path = os.path.join(
        user_folder,
        f"{chat_id}.json"
    )

    if not os.path.exists(file_path):
        return None

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def load_all_chats(user_id):
    user_folder = create_chat_folder(user_id)

    chats = []

    for filename in os.listdir(user_folder):

        if filename.endswith(".json"):

            file_path = os.path.join(
                user_folder,
                filename
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:
                chat = json.load(file)
                chats.append(chat)

    chats.sort(
        key=lambda x: x.get(
            "updated_at",
            ""
        ),
        reverse=True
    )

    return chats


def delete_chat(user_id, chat_id):
    user_folder = create_chat_folder(user_id)

    file_path = os.path.join(
        user_folder,
        f"{chat_id}.json"
    )

    if os.path.exists(file_path):
        os.remove(file_path)


def rename_chat(user_id, chat_id, new_title):
    chat = load_chat(
        user_id,
        chat_id
    )

    if chat is None:
        return False

    chat["title"] = new_title

    save_chat(
        user_id,
        chat_id,
        chat
    )

    return True