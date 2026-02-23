import json

MEMORY_FILE = "memory.json"

def save_conversation(user_id, question, answer):

    record = {
        "user_id": user_id,
        "question": question,
        "answer": answer
    }

    with open(MEMORY_FILE, "a") as f:
        json.dump(record, f)
        f.write("\n")