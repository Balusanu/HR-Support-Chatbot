import json
import datetime

EVAL_LOG_FILE = "retrieval_eval.json"

def evaluate_retrieval(query, retrieved_docs):

    policies = [doc.metadata.get("policy_name") for doc in retrieved_docs]

    unique_policies = list(set(policies))

    eval_record = {
        "timestamp": str(datetime.datetime.now()),
        "query": query,
        "retrieved_policies": policies,
        "unique_policy_count": len(unique_policies),
        "total_chunks": len(retrieved_docs)
    }

    with open(EVAL_LOG_FILE, "a") as f:
        json.dump(eval_record, f)
        f.write("\n")

    return eval_record