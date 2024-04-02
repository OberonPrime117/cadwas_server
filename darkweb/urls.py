from django.urls import path
from .views import bitcoin, flag, search, results, link_info

urlpatterns = [
    # path('get-all-crawled-links', get_all_crawled_links),
    # path('crawl-url', crawl_url),
    # #path('crawl-keyword', crawl_keyword),
    # path('crawl-url-multi', crawl_url_multi),   
    # path('link-similarity-by-url', link_similarity_of_darkweb_urls),
    # path('urls-for-link-similarity', get_urls_for_link_similarity),
    # path('keywords-for-link-similarity', get_keywords_for_link_similarity),
    # path('urls-for-flagging', get_urls_for_flagging),
    # path('flag-links', flag_links_to_track),
    # path('link-to-database', link_to_database),
    # path('bitcoin-address', bitcoin_address),
    path('search', search),
    path('results',results),
    path('link_info',link_info),
    path('bitcoin',bitcoin),
    path('flag',flag)
]