import wikipediaapi

def fetch_page_details(keyword, language='fr', max_sentences=5):
    """
    Recherche une page par mot-clé et retourne un résumé simplifié sans utiliser de bibliothèques complexes.
    :param keyword: Mot-clé pour rechercher la page Wikipedia
    :param language: Langue pour la recherche (par défaut 'fr')
    :param max_sentences: Nombre maximum de phrases pour le résumé
    :return: Un résumé de la page ou un message d'erreur
    """
    # Définir un user-agent personnalisé pour respecter les règles de Wikipedia
    user_agent = "CustomUserAgent/1.0 (amatek@example.com)"
    wiki_wiki = wikipediaapi.Wikipedia(language=language, user_agent=user_agent)
    
    # Rechercher la page
    page = wiki_wiki.page(keyword)
    
    if not page.exists():
        return "La page demandée n'existe pas ou aucun résultat n'a été trouvé pour ce mot-clé."
    
    # Diviser le contenu en phrases manuellement (sans NLTK)
    content = page.text
    sentences = content.replace('?', '.').replace('!', '.').split('.')  # Diviser par les points
    sentences = [s.strip() for s in sentences if s.strip()]  # Nettoyer les espaces
    
    # Générer un résumé basé sur le nombre de phrases demandé
    summary = " ".join(sentences[:max_sentences])  # Prendre les X premières phrases
    return f"=== Résumé de la page '{page.title}' ===\n{summary}"


# Interaction avec l'utilisateur
keyword = input("Entrez un mot-clé pour rechercher des pages Wikipedia : ")
lang = input("Entrez la langue (par défaut 'fr') : ") or 'fr'

# Résumer la page
result = fetch_page_details(keyword, lang)
print(result)
