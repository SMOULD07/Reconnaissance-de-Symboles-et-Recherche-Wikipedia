import matplotlib.pyplot as plt
import networkx as nx
import wikipedia
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk

# Télécharger les ressources nécessaires
nltk.download('punkt')

# Fonction pour extraire les détails de la page Wikipedia
def fetch_page_details(keyword, language='fr'):
    wikipedia.set_lang(language)
    try:
        search_results = wikipedia.search(keyword)
        if not search_results:
            return {"error": "Aucun résultat trouvé pour ce mot-clé."}
        first_page_title = search_results[0]
        page = wikipedia.page(first_page_title)
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

# Fonction pour synthétiser le contenu
def synthesize_content(content):
    try:
        parser = PlaintextParser.from_string(content, Tokenizer("french"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 3)  # Résumer en 3 phrases
        return " ".join(str(sentence) for sentence in summary)
    except Exception as e:
        return f"Erreur de synthèse locale : {e}"

# Fonction pour créer un graphique des liens
def create_graph(links, title):
    # Créer un graphe
    G = nx.DiGraph()
    for i, link in enumerate(links):
        if i < 10:  # Limiter à 10 liens pour simplifier le graphique
            G.add_edge(title, link)
    
    # Dessiner le graphe
    plt.figure(figsize=(12, 8))
    nx.draw(G, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
    plt.title(f"Graphique des liens pour : {title}")
    plt.show()

# Exemple d'utilisation
keyword = "lettre A"
details = fetch_page_details(keyword)

if "error" in details:
    print(details["error"])
else:
    # Résumé synthétisé
    summary = synthesize_content(details["content"])
    print(f"Résumé synthétisé :\n{summary}")

    # Graphique des liens internes
    print("\nCréation du graphique des liens internes...")
    create_graph(details["internal_links"], details["title"])

    # Graphique des liens externes
    print("\nCréation du graphique des liens externes...")
    create_graph(details["external_links"], details["title"])
