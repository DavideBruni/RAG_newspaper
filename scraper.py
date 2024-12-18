from datetime import datetime
import requests
import uuid
from bs4 import BeautifulSoup
from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer
import constant as CONST
import time

model = SentenceTransformer('intfloat/multilingual-e5-large')
CONNECT_TIMEOUT = 15 * 60

def get_full_article(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    article_section = soup.find('main')
    if article_section:
        try:
            title = article_section.find('h1').text
            try:
                author = article_section.find('span', class_='writer').text
            except:
                author = None
            try:
                summary = article_section.find('p', class_='summary-art').text
            except:
                summary = None
            content_divs = article_section.find_all('div', class_='content', id=True)
            content = [div.text for div in content_divs]
            try:
                last_update = article_section.find('p', class_='is-last-update')['datetime']
                parsed_date = datetime.fromisoformat(last_update)

                # Conversione al formato desiderato per ElasticSearch
                elastic_date = parsed_date.strftime('%Y-%m-%dT%H:%M:%S%z')
            except:
                elastic_date = None
            id = uuid.uuid4()
            return {
                "id": str(id),
                'title': title,
                'author': author,
                'summary': summary,
                'content': content,
                'date': elastic_date
            }
        except Exception as e:
            print(f"Error parsing article: {e}")
            return None
    else:
        return None

def get_embeddings(text):
    embeddings = model.encode(text, normalize_embeddings=True, convert_to_tensor=True, device='cuda:0')
    return embeddings.cpu().detach().numpy().tolist()

def store_article(article):
    os_client = OpenSearch(
        CONST.osUrl,
        verify_certs=False,
        http_auth=(CONST.osUser, CONST.osPass),
        timeout=CONNECT_TIMEOUT / 2,
        max_retries=2,
        retry_on_timeout=True
    )
    # Check if the document is already present
    query = {
        "query": {
            "match": {
                "metadata.url.keyword": article["url"]
            }
        }
    }
    search_response = os_client.search(index="corriere_articles", body=query)
    if search_response['hits']['total']['value'] > 0:
        print(f"Article already present: {article['url']}")
        return False
    
    try:
        # Store title document
        if article["title"] is not None:
            title_doc = {
                "metadata":{
                    "id": article["id"],
                    "author": article["author"],
                    "date": article["date"],
                    "section": article["section"], 
                    "url": article["url"],
                    "type": "title"
                },
                "text": article["title"],
                "embeddings": get_embeddings(article["title"])
            }
            os_client.index(index="corriere_articles", body=title_doc)

        if article["summary"] is not None:
            # Store summary document
            summary_doc = {
                "metadata":{
                    "id": article["id"],
                    "author": article["author"],
                    "date": article["date"],
                    "section": article["section"], 
                    "url": article["url"],
                    "type": "summary"
                },
                "text": article["summary"],
                "embeddings": get_embeddings(article["summary"])
            }
            os_client.index(index="corriere_articles", body=summary_doc)

        if article["content"] is not None:
        # Store content documents
            for i, content in enumerate(article["content"]):
                content_doc = {
                    "metadata":{
                        "id": article["id"],
                        "author": article["author"],
                        "date": article["date"],
                        "type": "content",
                        "section": article["section"],
                        "url": article["url"]
                    },
                    "text": content, 
                    "embeddings": get_embeddings(content)
                }
                os_client.index(index="corriere_articles", body=content_doc)

        return True
    except Exception as e:
        print(f"Error storing article: {e}")
        return False
    

def main():
    for section, url in CONST.mapping.items():
        response = requests.get(url, headers=CONST.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            div_containers = soup.find_all('section', class_='body-hp')     #get main section
            for div_container in div_containers: 
                articles = div_container.find_all(class_ = "media-news__content")   #get all news articles
                for i,article in enumerate(articles):
                    for a in article.find_all('a', href=True):                      #get all urls
                        article_url = a['href']
                        if url in article_url:
                            print(article_url)
                            response = requests.get(article_url, headers=CONST.headers)
                            if response.status_code == 200:
                                json_article = get_full_article(response)
                                if json_article is not None:
                                    json_article['section'] = section
                                    json_article['url'] = article_url
                                    if store_article(json_article):
                                        print("Article stored with success")
                                    else:
                                        print("Error storing article")
                                
                        else:
                            print("Article outside the section", article_url)
                        
                        time.sleep(1)
                            
            else:
                print("No articles found")
        else:
            print(f"Error {response.status_code}")
        

if __name__ == "__main__":
    main()