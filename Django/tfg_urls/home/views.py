from django.shortcuts import render
import requests
import pandas as pd
from io import BytesIO
from zipfile import ZipFile

def homeView(request):
    template_name = 'home.html'
    url = "https://www.whoisds.com/sample/other-db/nrd-crd-exd.zip"
    
    response = requests.get(url)
    response.raise_for_status()
    zipfile_content = BytesIO(response.content)
    
    with ZipFile(zipfile_content) as thezip:
        # Asumiendo que hay un solo archivo en el zip
        for filename in thezip.namelist():
            with thezip.open(filename) as thefile:
                df = pd.read_csv(thefile)
    
    # Obtener las primeras 10 filas y los nombres de las columnas
    first_10_rows = df.head(300).to_html(index=False, classes='table table-bordered table-striped')
    
    context = {
        'df_html': first_10_rows,
    }

    return render(request, template_name, context)

def homeSearchView(request):
    template_name = 'home.html'
    url = "https://www.whoisds.com/sample/other-db/nrd-crd-exd.zip"
    
    response = requests.get(url)
    response.raise_for_status()
    url_legit = request.GET.get('url_legit', '')
    zipfile_content = BytesIO(response.content)
    
    with ZipFile(zipfile_content) as thezip:
        # Asumiendo que hay un solo archivo en el zip
        for filename in thezip.namelist():
            with thezip.open(filename) as thefile:
                df = pd.read_csv(thefile)
    

    df['jaro_winkler_score'] = df['domain_name'].apply(lambda x: jaro_similarity(url_legit, x))

    # Establecer estilos CSS basados en los valores de jaro_winkler_score
    def set_color(value):
        if value > 1:
            return 'Very Hight'
        elif value >= 0.9 and value <= 1:
            return 'Hight'
        elif value >= 0.8 and value < 0.9:
            return 'Medium'
        else:
            return 'Low'

    df['Risk'] = df['jaro_winkler_score'].apply(set_color)

    # Convertir el DataFrame a HTML, incluyendo los estilos CSS
    top_10_html = df.nlargest(10, 'jaro_winkler_score').to_html(index=False, classes='table table-bordered table-striped', escape=False)
    df.drop(columns=['jaro_winkler_score'], inplace=True)
    context = {
        'df_html': top_10_html,
    }
    
    context = {
        'df_html': top_10_html,
    }

    return render(request, template_name, context)





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
