import pandas as pd
import io
import urllib, base64
import re
import nltk

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation

def read_xlsx(path):
    if path.endswith(".xlsx"):
        print("File is an excel file")
        df = pd.read_excel(path)
        if [str(x) for x in df.columns] == ['Línea', 'Día', 'Shift', 'Start Time', 'End Time', 'Seconds', 'Minutes',
        'Hours', 'Start Cycles', 'Start Unit', 'End Cycles', 'End Unit',
        'Actual Start/End Ratio', 'Listed Start/End Ratio', 'Super Reason',
        'Reason Lvl1', 'Reason Lvl2', 'Reason Lvl3', 'Reason Lvl4', 'Notes',
        'SKU', 'User', 'Orden de Producción', 'Dataset']:
            print("File is valid")
            return df
        else: 
            print("File is invalid")
    else: 
        print("File is not an excel file")

# Funcion que retorna los datos para graficar el top4 de razones
def getData_top4(df, num_reasons, num_top):

    # Especificamos que tantas razones queremos concatenar
    if num_reasons <= 1:
        df['Reason'] = df['Reason Lvl1']
    elif num_reasons == 2:
        df['Reason'] = df['Reason Lvl1'] + ' ' + df['Reason Lvl2']
    elif num_reasons == 3:
        df['Reason'] = df['Reason Lvl1'] + ' ' + df['Reason Lvl2'] + ' ' + df['Reason Lvl3']
    elif num_reasons > 3:
        df['Reason'] = df['Reason Lvl1'] + ' ' + df['Reason Lvl2'] + ' ' + df['Reason Lvl3'] + ' ' + df['Reason Lvl4']

    # Extraear las 4 razones principales del db general
    top4 = df.groupby('Reason')['Hours'].sum()
    top4 = top4.sort_values(ascending = False)
    top4 = top4.head(num_top)

    tag = top4.index
    
    # Extraer las horas por razones principales
    hours_sum = df[df['Reason'].isin(tag)].groupby('Reason')['Hours'].sum()
    # El total de horas se calcula con el total de TODAS las horas del db, no solo sumas
    hours_total = df['Hours'].sum() 
    hours_sum = hours_sum.sort_values(ascending = False)

    # Calcular los porcentajes de cada suma
    hours_percent = hours_sum / hours_total * 100

    indice_str = [str(x) for x in hours_sum.index]
    sumas_str = [str(x) for x in round(hours_sum,2)]
    porcentajes_str = [str(x) for x in round(hours_percent,2)]

    indice_str.append("Otros")
    sumas_str.append(str(round(hours_total-hours_sum.sum(),2)))
    porcentajes_str.append(str(round(100-sum(hours_percent),2)))

    # Retornamos una matriz con las labels, suma de horas y porcentajes para graficar
    data = [indice_str, sumas_str, porcentajes_str]
    data = dumps(data)

    return data

#Funcion que retorna los datos para graficar los topics de cada razon
def getData_topics(df, reason, num_clusters, num_keywords):

    # Descargar los recursos necesarios de NLTK
    nltk.download('punkt')
    nltk.download('stopwords')

    top4 = df.groupby('Reason')['Hours'].sum()
    top4 = top4.sort_values(ascending = False)
    top4 = top4.head(4)

    df_reason = df[df['Reason'] == top4.index[reason-1]]

    stopword_es = nltk.corpus.stopwords.words('spanish')
    my_stopwords = ['dee', 'agr', 'een', 'nan', 'iw', '']
    stopword_es.extend(my_stopwords)

    # count_vect = CountVectorizer(max_df=0.8, min_df=5, stop_words= stopwords.words('spanish'),lowercase= True, preprocessor=lambda x: re.sub(r'\d+', '', x))
    count_vect = CountVectorizer(max_df=0.8, min_df=5, stop_words= stopwords.words('spanish'),lowercase= True, token_pattern="[^\W\d_]+")
    # count_vect = TfidfVectorizer(max_df=0.8, min_df=5, stop_words= stopword_es, lowercase= True, token_pattern="[^\W\d_]+")
    doc_term_matrix = count_vect.fit_transform(df_reason['Notes'].values.astype('U'))

    LDA = LatentDirichletAllocation(n_components=num_clusters, random_state=42)
    LDA.fit(doc_term_matrix)

    keywords = []

    for i,topic in enumerate(LDA.components_):
        keywords.append([count_vect.get_feature_names_out()[i] for i in topic.argsort()[-num_keywords:]])

    topic_values = LDA.transform(doc_term_matrix)
    topic_values.shape
    df_reason['Topic'] = topic_values.argmax(axis=1)

    # Filtrar el DataFrame y calcular las sumas para cada categoría
    hours_sum = df_reason.groupby('Topic')['Hours'].sum()
    hours_sum = hours_sum.sort_values(ascending=False)

    # Calcular los porcentajes de cada suma
    hours_percent = hours_sum / hours_sum.sum() * 100

    indice_str = ['Topic ' + str(x) for x in hours_sum.index]
    sumas_str = [str(x) for x in round(hours_sum,2)]
    porcentajes_str = [str(x) for x in round(hours_percent,2)]

    # Retornamos una matriz con las labels, suma de horas y porcentajes para graficar
    data = [indice_str, sumas_str, porcentajes_str]
    data = dumps(data)
    keywords = dumps(keywords)
    return data, keywords