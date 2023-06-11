import sys
from PIL import Image
from joblib import load
import numpy as np
import matplotlib.pyplot as plt
from equation_resolver import EquationSolver


def predictImage(image, modele):
    pixels = list(image.getdata())
    ready_data = np.array([pixels])
    indice = modele.predict(ready_data)[0]
    significative = ['0', '1', '2', '3', '4', '5', '6',
                     '7', '8', '9', '*', '+', '-', '=', '(', ')', 'H']
    return significative[indice]


def dropWhiteLine(image_array):
    # Efface ligne horizontal blanc
    sums = np.sum(image_array, axis=1)
    indices = np.where(sums == 255 * image_array.shape[1])
    image_array = np.delete(image_array, indices, axis=0)

    return image_array

# Trouve les indices a partir du quelle on doit prendre l'image


def getSeparationIndice(indices):
    indices = indices[0]  # Les elements sont tous dans un tableau
    result = []
    for i in range(1, len(indices)):
        if (indices[i] - indices[i-1]) != 1:
            result.append([indices[i - 1], indices[i]])
    return result

# Preparer image de sortie pour la prédiction


def prepareResultImage(image):
    # Efface ligne horizontal blanc
    image_array = np.array(image)
    sums = np.sum(image_array, axis=1)
    maxVal = np.max(sums)
    indices = np.where(sums == maxVal)
    image_array = np.delete(image_array, indices, axis=0)

    image = (Image.fromarray(image_array)).resize((28, 28))

    image_array = np.array(image)

    image_array = np.where(image_array < 200, 0, image_array)
    image_array = np.where(image_array >= 200, 255, image_array)

    return (Image.fromarray(image_array))

# Meilleur format d'image : 500 largeur et 100 hauteur
# Fonction pour découper une image en plusieur image


def cutImageIntoArray(image):
    image = Image.open(image)
    resized_image = ((image.resize((500, 100))).convert('L'))
    image_array = np.array(resized_image)
    image_array = dropWhiteLine(image_array)   # Efface ligne blanc

    # Encadrement nouvelle image
    sums = np.sum(image_array, axis=0)
    maxi = sums.max()
    indices = np.where(sums == maxi)
    # Indices de separation des images
    separation = getSeparationIndice(indices)
    list_image = []  # Tableau des images séparés
    for limit in separation:
        temp_image = Image.fromarray(image_array[:, limit[0]:limit[1]])
        plt.imshow(temp_image)
        list_image.append(prepareResultImage(temp_image))
    return list_image


def predict(image_path):
    modele = load('src/MLModel/model_h.joblib')
    image_list = cutImageIntoArray(image_path)
    result = ""
    for i in image_list:
        letter = predictImage(i, modele)
        result += letter
    final_result = ""
    for index in range(len(result)):
        final_result += result[index]
        if index != len(result) - 1 and result[index + 1] != 'H':
            final_result += ' '
    return final_result


if __name__ == "__main__":
    equation = predict(sys.argv[1])
    print(equation)
