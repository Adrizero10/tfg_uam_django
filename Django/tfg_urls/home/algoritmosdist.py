from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def hamming_distance(s1, s2):
    """Calcula la distancia de Hamming entre dos cadenas
    devuelve -1 si las cadenas son de diferente longitud"""
    if len(s1) != len(s2):
        return -1
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def levenshtein_distance(str1, str2):
    """Calcula la distancia de Levenshtein entre dos cadenas
    usando el algoritmo de la distancia de Levenshtein"""
    d=dict()
    for i in range(len(str1)+1):
        d[i]=dict()
        d[i][0]=i
    for i in range(len(str2)+1):
        d[0][i] = i
    for i in range(1, len(str1)+1):
        for j in range(1, len(str2)+1):
            d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
    return d[len(str1)][len(str2)]


def damerau_levenshtein(s1, s2):
    """Calcula la distancia de Damerau-Levenshtein entre dos cadenas
    usando el algoritmo de la distancia de Damerau-Levenshtein"""
    d = {}
    len_s1, len_s2 = len(s1), len(s2)
    for i in range(-1, len_s1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, len_s2 + 1):
        d[(-1, j)] = j + 1
    for i in range(len_s1):
        for j in range(len_s2):
            cost = 0 if s1[i] == s2[j] else 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # Eliminación
                d[(i, j - 1)] + 1,  # Inserción
                d[(i - 1, j - 1)] + cost,  # Reemplazo
            )
            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost)  # Transposición
    return d[(len_s1 - 1, len_s2 - 1)]


def jaccard_distance(s1, s2):
    """Calcula la distancia de Damerau-Levenshtein entre dos cadenas
    usando el algoritmo de la distancia de Jaccard"""
    set1 = set(s1)
    set2 = set(s2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return 1 - intersection / union



def cosine_distance(s1, s2):
    """Calcula la distancia de Damerau-Levenshtein entre dos cadenas
    usando el algoritmo de la distancia de Cosine"""
    vectorizer = CountVectorizer().fit_transform([s1, s2])
    vectors = vectorizer.toarray()
    return 1 - cosine_similarity(vectors)[0, 1]



def jaro_similarity(s1, s2):
    """Calcula la distancia de Damerau-Levenshtein entre dos cadenas
    usando el algoritmo de la distancia de Jaro-Winkler"""
    # Calcular la longitud de las cadenas
    len_s1, len_s2 = len(s1), len(s2)

    # Definir la ventana de coincidencia
    match_distance = max(len_s1, len_s2) // 2 - 1

    # Inicializar listas de coincidencias y caracteres coincidentes
    s1_matches, s2_matches = [False] * len_s1, [False] * len_s2
    matches = 0

    # Encontrar coincidencias exactas
    for i, char_s1 in enumerate(s1):
        for j in range(max(0, i - match_distance), min(len_s2, i + match_distance + 1)):
            if not s2_matches[j] and char_s1 == s2[j]:
                s1_matches[i] = s2_matches[j] = True
                matches += 1
                break

    if matches == 0:
        return 0.0

    # Contar transposiciones
    transpositions = 0
    k = 0
    for i, is_match in enumerate(s1_matches):
        if is_match:
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1

    # Calcular la similitud de Jaro
    jaro_similarity = (matches / len_s1 + matches / len_s2 + (matches - transpositions) / matches) / 3

    # Calcular el factor de ajuste de Winkler
    prefix = 0
    for s1_char, s2_char in zip(s1, s2):
        if s1_char == s2_char:
            prefix += 1
        else:
            break
    jaro_winkler_similarity = jaro_similarity + (prefix * 0.1 * (1 - jaro_similarity))

    return jaro_winkler_similarity
