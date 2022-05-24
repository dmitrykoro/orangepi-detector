import face_recognition
import json
import numpy as np


def compare_encodings():
    all_encodings = json.load(open('encodings.json'))

    all_distances = []

    i = 1

    for user in all_encodings.items():
        current_user_id = user[0]
        current_user_encoding = np.array(user[1])

        print(f'Comparing {i}')

        for compared_user in all_encodings.items():
            compared_user_id = compared_user[0]
            compared_user_encoding = np.array(compared_user[1])

            if compared_user_id == current_user_id:
                continue

            face_distance = np.linalg.norm(current_user_encoding - compared_user_encoding)
            all_distances.append(face_distance)

        i += 1

    with open("distances.json", "w") as write_file:
        json.dump(all_distances, write_file, indent=4)
    print('Finished')






compare_encodings()
