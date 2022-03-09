from elasticsearch import Elasticsearch

#authentication to the elasticsearch base
def authent_es(host, port, user, pwd):
    #print(host, port, user, pwd)
    es = Elasticsearch([{'scheme':'http','host': host, 'port': int(port)}], http_auth=(user, pwd))
    return es


#save object in specific index
def save_es_stack(indexDbName, obj, es):
    es.index(index=indexDbName, document=obj)

