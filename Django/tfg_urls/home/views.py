import datetime
from django.conf import settings
from django.shortcuts import render
import requests
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from django.core.mail import EmailMessage
from django.http import HttpResponse
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import os
import openai
from django.http import JsonResponse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textdistance

url = 'https://www.whoisds.com/sample/other-db/nrd-crd-exd.zip'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'tu_clave_de_openai')

def homeView(request):
    template_name = 'home.html'
    
    response = requests.get(url)
    response.raise_for_status()
    zipfile_content = BytesIO(response.content)
    
    with ZipFile(zipfile_content) as thezip:
        # Asumiendo que hay un solo archivo en el zip
        for filename in thezip.namelist():
            with thezip.open(filename) as thefile:
                df = pd.read_csv(thefile)
    
    # Obtener las primeras 10 filas y los nombres de las columnas
    df = df.head(20)
    df.columns = [col.replace('_', ' ').title() for col in df.columns]

    context = {
        'df_html': df.to_html(index=False, classes='table table-bordered table-striped', escape=False),
    }

    return render(request, template_name, context)

def homeSearchView(request,sendmailok = False,url_legit = None):
    template_name = 'home.html'
    
    response = requests.get(url)
    response.raise_for_status()
    if url_legit is None:
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
            return 'Very High'
        elif value >= 0.9 and value <= 1:
            return 'High'
        elif value >= 0.8 and value < 0.9:
            return 'Medium'
        else:
            return 'Low'

    df['Risk'] = df['jaro_winkler_score'].apply(set_color)

    # Filtrar las entradas de tipo "Low"
    df_filtered = df[df['Risk'] != 'Low']

    # Contar el número de URLs por tipo de riesgo
    risk_counts = df_filtered['Risk'].value_counts()
    # Convertir el DataFrame a HTML, incluyendo los estilos CSS
    df = df.nlargest(10, 'jaro_winkler_score')
    df.drop(columns=['jaro_winkler_score'], inplace=True)
    df.columns = [col.replace('_', ' ').title() for col in df.columns]
    


    buf = BytesIO()
    plt.figure(figsize=(10, 6))
    risk_counts.plot(kind='bar', color=[ 'yellow', 'orange','red', 'green'])
    plt.xlabel('Tipo de Riesgo')
    plt.ylabel('Número de URLs')
    plt.xticks(rotation=0)
    plt.savefig(buf, format='png')
    buf.seek(0)
    graphic_plot_chart = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    total_urls = len(df)
    suspicious_urls = len(df_filtered)
    risk_percentages = df_filtered['Risk'].value_counts(normalize=True) * 100
    risk_percentages = risk_percentages.round(1) 

    context = {
        'df_html': df.to_html(index=False, classes='table table-bordered table-striped', escape=False),
        'url_legit' : url_legit,
        'send_mail_ok' : sendmailok,
        'send_mail_option' : True,
        'image_base64': graphic_plot_chart,
        'total_urls': total_urls,
        'suspicious_urls': suspicious_urls,
        'risk_percentages': risk_percentages.to_dict(),
    }

    return render(request, template_name, context)



def send_mail_phising_warnings(request):

    url_legit = request.GET.get('url_legit_mail', '')
    
    response = requests.get(url)
    response.raise_for_status()
    url_legit = request.GET.get('url_legit_mail', '')
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
            return 'Very High'
        elif value >= 0.9 and value <= 1:
            return 'High'
        elif value >= 0.8 and value < 0.9:
            return 'Medium'
        else:
            return 'Low'

    df['Risk'] = df['jaro_winkler_score'].apply(set_color)


    # Filtrar las entradas de tipo "Low"
    df_filtered = df[df['Risk'] != 'Low']

    # Contar el número de URLs por tipo de riesgo
    risk_counts = df_filtered['Risk'].value_counts()
    # Convertir el DataFrame a HTML, incluyendo los estilos CSS
    df = df.nlargest(10000, 'jaro_winkler_score')
    df.drop(columns=['jaro_winkler_score'], inplace=True)
    df.columns = [col.replace('_', ' ').title() for col in df.columns]
    file_path = 'informe_phishing.xlsx'
    df.to_excel(file_path, index=False)


    # Crear el diagrama de barras
    plt.figure(figsize=(10, 6))
    risk_counts.plot(kind='bar', color=[ 'yellow', 'orange','red', 'green'])
    plt.title('Número de URLs por Tipo de Riesgo')
    plt.xlabel('Tipo de Riesgo')
    plt.ylabel('Número de URLs')
    plt.xticks(rotation=0)

    # Guardar el gráfico como imagen
    plt.savefig('risk_bar_chart.png')



    #dia de hoy en strign
    fecha = datetime.datetime.now().strftime("%Y-%m-%d") 

    subject = 'Informe dia ' + fecha
    message = 'Adjunto se encuentra el informe de phishing del dia ' + fecha + ', con las 10.000 direcciones mas parecidas a la url ' + str(url_legit) + '\n\n' + 'Saludos, \n\n' + 'Equipo de seguridad phishing'
    recipient_list = ['adrizero2001@gmail.com', 'lucipeich7@gmail.com', request.user.email]
    
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    email.attach('informe_phishing.xlsx', open('informe_phishing.xlsx', 'rb').read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.attach('risk_bar_chart.png', open('risk_bar_chart.png', 'rb').read(), 'image/png')

    email.send()
    
    return homeSearchView(request,sendmailok = True,url_legit = url_legit)





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



def phishing(request):
    return render(request, 'phishing.html')


def cosine_distance(s1, s2):
    vectorizer = CountVectorizer().fit_transform([s1, s2])
    vectors = vectorizer.toarray()
    return 1 - cosine_similarity(vectors)[0, 1]