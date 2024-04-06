from typing import List
from sqlalchemy.orm import Session

from scripts.brave import search as brave_search
from models import SearchResult

def compare_urls(new_urls: List[str], stored_urls: List[str]) -> bool:
    return set(new_urls) != set(stored_urls)

def update_database(db: Session, new_urls: List[str]):
    from your_module import SearchResult  # import your model at the top of the file

    db.query(SearchResult).delete()
    for url in new_urls:
        db.add(SearchResult(url=url))
    db.commit()

def check_for_updates(db: Session):
    new_urls = brave_search()
    stored_urls = db.query(SearchResult.url).all()
    stored_urls = [url[0] for url in stored_urls]

    if compare_urls(new_urls, stored_urls):
        update_database(db, new_urls)
        return True, new_urls
    return False, stored_urls