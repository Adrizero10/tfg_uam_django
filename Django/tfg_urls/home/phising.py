from Django.tfg_urls.home.algoritmosdist import hamming_distance, levenshtein_distance, damerau_levenshtein, jaccard_distance, cosine_distance, jaro_similarity

def url_phising(url):

    with open("domain-names.txt") as archivo:
        for linea in archivo:
            hamming_dist = hamming_distance(linea,url)
            if hamming_dist < 0:
                percentage_hamming = 0
            else:
                similarity = 1 - (hamming_dist / len(url))
                percentage_hamming = similarity * 100
            if percentage_hamming > 80:
                print(f"Hamming distance between {linea} and {url} is {hamming_dist} ({percentage_hamming:.2f}%)")

            max_len = max(len(linea), len(url))
            levenshtein_dist = levenshtein_distance(linea, url)
            similarity = 1 - (levenshtein_dist / max_len)
            percentage_levenshtein = similarity * 100
            if percentage_levenshtein > 80:
                print(f"Levenshtein distance between {linea} and {url} is {levenshtein_dist} ({percentage_levenshtein:.2f}%)")

            damerau_levenshtein_dist = damerau_levenshtein(linea, url)
            if max_len == 0:
                percentage_damerau_levenshtein = 100.0
            else:
                percentage_damerau_levenshtein = (1 - damerau_levenshtein_dist / max_len) * 100
            
            if percentage_damerau_levenshtein > 80:
                print(f"Damerau_levenshtein distance between {linea} and {url} is {damerau_levenshtein_dist} ({percentage_damerau_levenshtein:.2f}%)")


            # Calcular la distancia de Jaccard
            jaccard_dist = jaccard_distance(linea, url)
            similarity = 1 - jaccard_dist
            percentage_jaccard = similarity * 100
            if percentage_jaccard > 80:
                print(f"Jaccard distance between {linea} and {url} is {jaccard_dist} ({percentage_jaccard:.2f}%)")

            # Calcular la distancia de Cosine
            cosine_dist = cosine_distance(linea, url)
            similarity = 1 - cosine_dist
            percentage_cosine = similarity * 100
            if percentage_cosine > 80:
                print(f"Cosine distance between {linea} and {url} is {cosine_dist} ({percentage_cosine:.2f}%)")

            # Calcular la distancia de Jaro-Winkler
            jaro_winkler_dist = jaro_similarity(linea, url)
            percentage_jaro_winkler = jaro_winkler_dist * 100
            if percentage_jaro_winkler > 80:
                print(f"Jaro-Winkler distance between {linea} and {url} is {jaro_winkler_dist} ({percentage_jaro_winkler:.2f}%)")


