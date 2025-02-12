import wikipedia
import matplotlib.pyplot as plt
from collections import Counter
from urllib.parse import urlparse

def fetch_page_details(keyword, language='fr'):
    """
    Recherche une page par mot-clé, récupère son contenu, ses liens internes et ses liens externes.
    :param keyword: Mot-clé pour rechercher la page Wikipedia
    :param language: Langue pour la recherche (par défaut 'fr')
    :return: Un dictionnaire contenant le contenu, les liens internes et les liens externes
    """
    wikipedia.set_lang(language)
    try:
        # Recherche des pages correspondant au mot-clé
        search_results = wikipedia.search(keyword)
        if not search_results:
            return {"error": "Aucun résultat trouvé pour ce mot-clé."}

        # Récupérer la première page trouvée
        first_page_title = search_results[0]
        page = wikipedia.page(first_page_title)

        # Rassembler les informations
        return {
            "title": first_page_title,
            "content": page.content,
            "internal_links": page.links,
            "external_links": page.references
        }
    except wikipedia.exceptions.DisambiguationError as e:
        return {"error": f"Ambiguïté détectée. Plusieurs options : {e.options}"}
    except wikipedia.exceptions.PageError:
        return {"error": "La page demandée n'existe pas."}
    except Exception as e:
        return {"error": f"Une erreur s'est produite : {e}"}

def plot_external_links(links):
    """
    Affiche un graphique des domaines des liens externes trouvés.
    """
    # Extraire les domaines des liens externes
    domains = [urlparse(link).netloc for link in links]
    domain_counts = Counter(domains)

    # Préparer les données pour le graphique
    labels = list(domain_counts.keys())
    counts = list(domain_counts.values())

    # Créer un graphique en barres
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color='skyblue')
    plt.xlabel('Domaines')
    plt.ylabel('Nombre de liens')
    plt.title('Distribution des liens externes')
    plt.xticks(rotation=90)  # Rotation des étiquettes pour lisibilité
    plt.tight_layout()  # Ajuste le placement des éléments pour éviter le chevauchement
    plt.show()

if __name__ == "__main__":
    keyword = input("Entrez un mot-clé pour rechercher des pages Wikipedia : ")
    lang = input("Entrez la langue (par défaut 'fr') : ") or 'fr'
    details = fetch_page_details(keyword, lang)

    # Gérer les erreurs
    if "error" in details:
        print(details["error"])
    else:
        # Afficher le contenu complet
        print(f"\n=== Contenu complet de la page '{details['title']}' ===\n")
        print(details["content"])

        # Afficher les liens internes
        print("\n=== Liens internes ===")
        for link in list(details["internal_links"])[:10]:  # Afficher les 10 premiers
            print(link)

        # Afficher les liens externes sous forme de graphique
        print("\n=== Liens externes ===")
        if details["external_links"]:
            plot_external_links(details["external_links"])  # Afficher les liens externes sous forme de graphique
        else:
            print("Aucun lien externe trouvé.")
