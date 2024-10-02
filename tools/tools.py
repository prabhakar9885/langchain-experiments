from langchain_community.tools import TavilySearchResults


def get_profile_url_tavily(name: str):
    """Searches for online profiles of a person"""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res