import os
import face_recognition
import shutil

global database
global encodes

global root_known
global root_unknown


def load_database():
    """
    Generating a 'DB' out of the existing images in the known folder.
    name = Folder name.
    encoding = The encoded version of the image from that folder.
    :return: returns the DB as a list of dicts.
    """
    print('Loading database....')
    global root_known, root_unknown
    root_known, root_unknown = 'known', 'unknown'
    global database
    global encodes
    database = []
    encodes = []
    known_root = 'known'
    for person_directory in os.listdir('known'):
        images_of_person = os.listdir(f'{known_root}/{person_directory}')
        for face_image in images_of_person:
            image_encoding = face_recognition.face_encodings(
                face_recognition.load_image_file(f'{known_root}/{person_directory}/{face_image}'))[0]
            database.append({person_directory: image_encoding})
            encodes.append(image_encoding)
    print('Cool! Database is loaded!')
    return database, encodes


def get_unknown_face(image_root):
    """
    takes the image, and formats it to the needed format.
    :param image_root:
    :return: returns the images as encoded.
    """
    try:
        image_encoding = face_recognition.face_encodings(face_recognition.load_image_file(image_root))[0]
        return image_encoding
    except Exception as e:
        print(e)


def find_face(encoded_faces, unknown_face):
    """
    Here the unknown image is compared to the list of the known images.
    :param encoded_faces:
    :param unknown_face:
    :return: Name if True
    """
    global database
    try:
        matches = face_recognition.compare_faces(encoded_faces, unknown_face)
        if True in matches:
            return list(database[matches.index(True)].keys())[0]
        else:
            return False
    except Exception as e:
        raise e


def register_new_face(image, name):
    """
    The so called "adding to the db" thing.
    takes the image, the name of the image, and saves it
    :param image:
    :param name:
    :return:
    """
    global database, root_unknown, root_known
    os.mkdir(f'{root_known}/{name}')
    shutil.move(image, f'{root_known}/{name}')
    print('Saved!')


def main():
    global root_unknown
    faces, encodes = load_database()
    while True:
        image_name = input('Write image name:')
        if 'show data' in image_name:
            print('\n---------------')
            for each in faces:
                print(f'|  {list(each.keys())[0]}')
            print('---------------\n')
        elif 'exit' in image_name:
            quit()
        else:
            encoded_unknown_face = get_unknown_face(f'{root_unknown}/{image_name}.jpg')
            search = find_face(encodes, encoded_unknown_face)
            if search:
                print(f"\nFOUND! That's {search}")
            else:
                new_face_name = input('Not found..Who dis? > ')
                register_new_face(f'{root_unknown}/{image_name}.jpg', new_face_name)
                print('New face has been added!\n')
                # Refreshing the database after a new registration.
                faces, encodes = load_database()


if __name__ == '__main__':
    main()
