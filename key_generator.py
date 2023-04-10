import random
import server_db


def key_gen(num_keys: int) -> list[str]:
    keys = []
    groups = 3
    chars_per_group = 5
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    for i in range(num_keys):
        key = ""
        for j in range(groups):
            group = ""
            for k in range(chars_per_group):
                group += random.choice(alphabet)
            key += group
            if j < groups - 1:
                key += "-"
        server_db.add_key(key)
        keys.append(key)
    return keys