import cv2
import os
import face_recognition

imagesPath = "media/alumnos"
extractedPath = 'media/alumnos/extracted'
inputPath = 'media/input'
facesEncodings = []
facesNames = []


# Detector facial
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def append_encodings(foto):

    image = cv2.imread(extractedPath + '/' + foto)
    # Face_recognition utilizara Dlib y Dlib necesita las imagenes en RGB y no en BGR
    # Por defecto, OpenCV lee las imagenes en BGR, asi que hacemos la transformacion
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Codificamos cada una de las imagenes
    f_coding = face_recognition.face_encodings(image, known_face_locations=[(0, 150, 150, 0)])[0] # Arriba, derecha, abajo, izquierda
    facesEncodings.append(f_coding)
    facesNames.append(foto.split('.')[0]) # El nombre de los archivos jpg se separa por '.'


def extrae_rostros(foto):
    found = False

    image = cv2.imread(imagesPath + "/" + foto)
    faces = faceClassif.detectMultiScale(image, 1.1, 5) # Informacion de la ubicacion de los rostros dentro de la imagen

    for (x, y, w, h) in faces:
        found = True
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        face = image[y:y + h, x:x + w]
        face = cv2.resize(face, (150, 150)) # Redimencionamos las imagenes a 150 x 150 px
        cv2.imwrite(extractedPath + "/" + foto, face)
    
    if found:
        append_encodings(foto)
    
    return found


# Extraer el vector de 128 elementos
# Codificar los rostros extraidos

def refresh_encodings():
    facesEncodings.clear()
    facesNames.clear()

    for file_name in os.listdir(extractedPath):
        append_encodings(file_name)
    
    print(facesEncodings)
    print(facesNames)


###################################################################
# LEYENDO VIDEO
def recognize_person(foto) -> str:
    resultado = 'unknown'   
    image = cv2.imread(inputPath + '/' + foto)
    frame = cv2.flip(image, 1)
    orig = frame.copy()
    faces = faceClassif.detectMultiScale(frame, 1.1, 5)

    if not facesEncodings: # Si la variable esta vacia se actualizan los encodings de las caras
        refresh_encodings()

    for (x, y, w, h) in faces:
        face = orig[y:y + h, x:x + w]
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        actual_face_encoding = face_recognition.face_encodings(face, known_face_locations=[(0, w, h, 0)])[0]
        result = face_recognition.compare_faces(facesEncodings, actual_face_encoding) # Se compara el rostro guardado con el rostro actual con el que queremos comparar
        print(result)

        if True in result:
            index = result.index(True)
            resultado = facesNames[index]
        
    return resultado



