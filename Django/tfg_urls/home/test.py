# Leer URLs del archivo



import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textdistance

# Funciones de distancia/similitud utilizando bibliotecas optimizadas
def hamming_distance(s1, s2):
    if len(s1) != len(s2):
        return -1
    return textdistance.hamming(s1, s2)

def levenshtein_distance(str1, str2):
    return textdistance.levenshtein(str1, str2)

def damerau_levenshtein(s1, s2):
    return textdistance.damerau_levenshtein(s1, s2)

def jaccard_distance(s1, s2):
    return textdistance.jaccard(s1, s2)



def jaro_similarity(s1, s2):
    return textdistance.jaro_winkler(s1, s2)

with open('url.txt', 'r') as file:
    urls = file.read().splitlines()

# Preparar datos para el análisis
results = []

for i in range(1000):
    for j in range(i + 1, 1000):
        u1, u2 = urls[i], urls[j]
        results.append({
            'URL1': u1,
            'URL2': u2,
            'Hamming': hamming_distance(u1, u2),
            'Jaccard': jaccard_distance(u1, u2),
            'Cosine': cosine_distance(u1, u2),
            'Jaro-Winkler': jaro_similarity(u1, u2)
        })

# Convertir resultados a DataFrame
df = pd.DataFrame(results)

# Calcular promedios
mean_values = df.mean(numeric_only=True)

# Visualizar los resultados
fig, ax = plt.subplots()
mean_values.plot(kind='bar', ax=ax)
ax.set_title('Comparación de Algoritmos de Similitud de Cadenas')
ax.set_ylabel('Distancia Promedio')
ax.set_xlabel('Algoritmo')
plt.xticks(rotation=45)
plt.tight_layout()

# Guardar gráfico en formato PNG
plt.savefig('comparacion_algoritmos.png')

# Mostrar gráfico
plt.show()