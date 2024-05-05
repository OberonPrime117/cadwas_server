import os
import time
from urllib.parse import urlparse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import gzip
import lzma
from darkweb.utils.join import join_files
from .utils.final2 import vmain2
from .utils.topic_modelling import preprocess_text, words
from .models import Address, BaseContains, BaseDone, Category, ClearnetLink, ErrorDetected, Keyword, LinkContains, LinkDone, LinkStatus, LinkVisited, OnionLink, Relation, Transaction, TransactionId, ipFound, mailFound, numberFound
from django.core.paginator import Paginator
import math
from .utils.synonym_me import get_synonyms
from gensim.models import LdaModel
from gensim.corpora import Dictionary
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
# from googletrans import Translator
import gensim.corpora
import gensim.downloader as api
from gensim.models import KeyedVectors
from django.http import HttpResponseForbidden
from dotenv import dotenv_values
import nltk

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# config = dotenv_values(".env")
# glove_model_path = config["GLOVE_PATH"]
# glove_model = KeyedVectors.load(glove_model_path)

@api_view(['GET'])
def hello(request):
    # data = json.loads(request.body.decode('utf-8'))
    # query = data['entered']
    return Response("heelo")

@api_view(['POST'])
def search(request):
    data = json.loads(request.body.decode('utf-8'))

    # ~ EXPECTED POST REQUEST DATA - {'entered': 'hack'}
    # ? THIS API REQUEST VALIDATES WHETHER THE URL HAS BEEN CRAWLED OR NOT
    # ~ IF NOT FOUND IN DB, IT ADDS URL TO CRAWL QUEUE

    query = data['entered']

    # ~ MULTIPLE KEYWORDS ARE SEPARATED VIA COMMA
    # ~ BACKEND RECEIVES ALL PARAMETERS AS STRING

    total_search = str(query).split(',')
    
    for unit in total_search:

        # ^ USER IS SEARCHING URL
        if ("http" in str(unit) or "https" in str(unit)) and "onion" in str(unit):

            # ~ CHECK IF URL EXISTS IN DB
            count = LinkDone.objects.filter(link=unit).count()

            # ~ URL DOES NOT EXISTS IN DB
            if count == 0:

                LinkDone(link=unit,types="donated",time=time).save()
                Relation(base_url=unit, parent_url = unit, link=unit).save()
                LinkContains(link=unit).save()
                BaseDone(base_url=unit, category_done=False, shodan_done=False, selenium_done=False).save()
                BaseContains(base_url=unit, contains_shodan=False).save()
                Category(base_url=unit).save()
                LinkVisited(link=unit,time=time).save()

            return Response({'res': True})
            
        # ^ USER IS SEARCHING KEYWORD
        else:
            return Response({'res':True})            

@api_view(['POST'])
def results(request):
    if request.method == "POST":

        data = json.loads(request.body.decode('utf-8'))

        # ~ EXPECTED POST REQUEST DATA - {'entered': 'hack', 'page': 1}
        # ~ THIS API PROVIDES REACT WITH LINKS RELATED TO SEARCHES

        query = data['entered']
        requested_num = data['page']

        # ~ MULTIPLE KEYWORDS ARE SEPARATED VIA COMMA
        # ~ BACKEND RECEIVES ALL PARAMETERS AS STRING
        
        total_search = str(query).split(',')

        # TODO - SEARCH SUPPORT - LINK, KEYWORD, BTC, IP, EMAIL, PHONE NUMBER, SHODAN

        unit_list = []

        # ! REMOVING INCORRECT OR PROBLEMATIC CASES
        if len(total_search) == 1 and "" in total_search:
            return HttpResponseForbidden("Access Denied")

        for unit in total_search:

            unit_abc = list(unit)
            temp_unit = ''.join(unit_abc[0:3])

            # ^ URL SEARCH

            if "http" in unit or "onion" in unit:
                if "://" in unit:
                    parsed_url = urlparse(unit)
                    unit = parsed_url.scheme + "://" + parsed_url.netloc

                values = Relation.objects.filter(base_url=str(unit)).only("link")
                if len(values)>0:
                    for k in values:
                        unit_list.append(k['link'])
            
            # ^ BTC SEARCH
            elif "1" == unit_abc[0] or "3" == unit_abc[0] or "bc1" == temp_unit:
                values = Address.objects.filter(address=unit).only("link")
                if len(values)>0:
                    for k in values:
                        unit_list.append(k['link'])
            
            # ^ KEYWORD SEARCH
            else:

                # ~ ADD SINGULAR URLs BASED ON KEYWORDS
                # val_count = Keyword.objects.filter(keyword=unit).only('link').count()
                # if val_count > 0:
                #     values = Keyword.objects.filter(keyword=unit).only('link')
                #     for k in values:
                #         unit_list.append(k.link)

                # ~ ADD URLs BASED ON DOMAIN ASSOCIATION WITH THE WORD
                # glove_model = api.load('glove-wiki-gigaword-300')
                try:
                    current_directory = os.path.dirname(os.path.realpath(__file__))
                    current_directory = current_directory.split("/")
                    current_directory.pop()
                except Exception as e:
                    print("current directory issue")
                
                try:
                    current_directory = os.path.join(*current_directory)
                    filename = "glove-wiki-gigaword-300"
                    file_path = os.path.join(current_directory, filename)
                    file_path = "/"+file_path

                    filename_check = "glove-wiki-gigaword-300.vectors.npy"
                    file_path_check = os.path.join(current_directory, filename_check)
                    file_path_check = "/"+file_path_check
                except Exception as e:
                    print("join errors")
                
                try:
                    if os.path.exists(file_path_check):
                        pass
                    else:
                        output_file = 'glove-wiki-gigaword-300.vectors.npy'
                        join_files("split_gigaword", output_file)
                
                except:
                    print("join files error")
                
                try:
                    file_path = str(file_path)
                    unit = str(unit)
                    glove_model = KeyedVectors.load(file_path)
                    print(glove_model)
                    html_code,dom,ml= vmain2([unit], glove_model)
                except Exception as e:
                    print("glove model error")
                    print(e)
                
                try:
                    values = OnionLink.objects.filter(domain=dom).only('link').limit(20)
                    for k in values:
                        unit_list.append(k.link)

                except Exception as e:
                    print(e)
                    my_model = ErrorDetected(link=unit, error=e, filename="views.py results API - GLOVE domain failure")
                    my_model.save()
        
        # ~ REMOVE DUPLICATES
        unit_list = list(set(unit_list))

        temp = []
        dash_list = {}

        # ^ ACTUAL URL LIST IS POPULATED (IN ACCORDANCE TO FRONTEND REQUIREMENTS)
        # * DATA POINTS - STATUS, TIME OF CRAWLING, DOMAIN, LINK, CONTAINS DATA
        # TODO - REMOVE STATUS ALTOGETHER (SINCE ALL URLs SHOULD BE ONLINE IDEALLY)
        # TODO - CHANGE THIS TO INCLUDE LINKS RELEVANT TO INPUT_LINK

        for i in unit_list:

            try:

                dash_list = {}

                stat_val = LinkDone.objects.get(link=i)
                dash_list["status"] = stat_val.status

                time_val = LinkDone.objects.get(link=i)
                dash_list["time"] = time_val.time

                domain_val = OnionLink.objects.get(link=i)
                dash_list["type"] = domain_val.domain

                dash_list["link"] = i

                contains_val = LinkContains.objects.get(link=i)
                dash_list["contains_data"] = contains_val.contains_data

                temp.append(dash_list)
            
            except Exception as e:
                print(e)
                my_model = ErrorDetected(link=i, error=e, filename="views.py results API - POPULATE URL LIST WITH DATA POINTS")
                my_model.save()

        # ^ PAGINATOR, 50 ROWS PER PAGE
        p = Paginator(temp,50)
        page = p.get_page(requested_num)

        return Response({'res':page.object_list,'current_page_num':requested_num,'total_page_num':p.num_pages})

@api_view(['POST'])
def link_info(request):
    if request.method == "POST":

        data = json.loads(request.body.decode('utf-8'))

        # ~ EXPECTED POST REQUEST DATA - {'entered': 'http://example.onion'}
        # TODO - ADD USER CORRELATE

        input_link = str(data['entered'])

        # ^ EXTRACT LINK, PARENT LINK, LIST CONTAINS
        # ~ ACTUAL LINKS
        link_list = Relation.objects.all().only('link')
        link_list = [i.link for i in link_list]

        # ~ ACTIONABLE OR NOT
        contains_list = []
        for i in link_list:
            val = LinkContains.objects.get(link=i)
            contains_list.append(val.contains_data)
        
        # ~ PARENT LINKS OF ACTUAL LINKS
        parent_list = []
        for i in link_list:
            val = Relation.objects.get(link=i)
            parent_list.append(val.parent_url)
        
        node_list = []
        type_node_list = []
        approved_edge_link = []
        approved_edge_parent_link = []

        # ^ POPULATE INITIAL LIST OF NODES
        for i,j,k in zip(link_list, contains_list, parent_list):

            # ~ ADD TO NODE_LIST IF BOTH AREN'T SAME (TO AVOID DUPLICATES)
            if str(i) != str(k):

                # ~ ADD LINK TO NODE_LIST
                if i not in node_list:
                    
                    node_list.append(i)
                    type_node_list.append(j)
                
                # ~ ADD PARENT LINK TO NODE_LIST
                if k not in node_list:

                    val = LinkContains.objects.get(link=k)
                    node_list.append(k)
                    type_node_list.append(val.contains_data)
        
        # ^ POPULATE SECONDARY LIST OF EDGES
        for i,j,k in zip(link_list, contains_list, parent_list):

            # ~ ADD TO EDGE_LIST IF BOTH AREN'T SAME (TO AVOID DUPLICATES)
            if str(i) != str(k):

                # ~ CHECK IF BOTH LINK & PARENT LINK IN NODE_LIST
                if (i in node_list and k in node_list):

                    # ~ ADD EDGE TO EDGE_LIST & PARENT_EDGE_LIST
                    if i not in approved_edge_link and i not in approved_edge_parent_link:

                        approved_edge_link.append(i)
                        approved_edge_parent_link.append(k)
                    
                    # ~ IF ALREADY EXISTS IN EITHER LIST
                    elif i in approved_edge_link and i in approved_edge_parent_link:

                        # ~ IS THE INCOMING EDGE - NEW OR OLD ?

                        # ~ OLD EDGE - SHOULD NOT HAPPEN IDEALLY
                        if approved_edge_link.index(i) == approved_edge_parent_link.index(k):
                            pass

                        # ~ ADD ANOTHER EDGE TO EDGE_LIST & PARENT_EDGE_LIST
                        else:
                            approved_edge_link.append(i)
                            approved_edge_parent_link.append(k)
        
        # ^ ALLOCATE NODES TO GRAPH
        node = {}
        edges = {}
        index = 0
        graph_node = []
        graph_edge = []
        graph_label = []

        # ^ ADD METADATA TO NODES IN GRAPH
        for node_link, type_link in zip(node_list, type_node_list):
            
            node = {}
            node["id"] = index
            node["label"] = type_link
            node["title"] = node_link
            
            # ~ REQUIRED FOR EDGE GRAPH ALLOCATION
            graph_label.append(node_link)

            # ~ DATA FORMATTING FOR REACT
            graph_node.append(node)

            index = index + 1
        
        # ^ RESET INDEX VALUE

        index = 1

        # ^ ALLOCATE EDGES TO GRAPH
        for edges_link, parent_link in zip(approved_edge_link, approved_edge_parent_link):

            # ~ MATCH EDGE_LIST & PARENT_EDGE_LIST
            parent_id = graph_label.index(parent_link)
            link_id = graph_label.index(edges_link)

            # ~ DATA FORMATTING FOR REACT
            edges = {}
            edges["from"] = parent_id
            edges["to"] = link_id
            
            graph_edge.append(edges)
        
        # ^ ADD GRAPH DATA TO POST REQUEST KA RESPONSE
        graph = {}
        graph["node"] = graph_node
        graph["edges"] = graph_edge

        result_list = {}
        result_list["graph"] = graph

        parsed_url = urlparse(str(input_link))
        base_url = parsed_url.scheme + "://" + parsed_url.netloc

        # TODO - CHANGE THIS SYSTEM - ENABLE URLs TO ACCESS PARENT URL + THEIR OWN
        # TODO - DISCUSS THIS

        # ^ BTC DATA
        btc_val_count = Address.objects.filter(link=base_url).count()
        if btc_val_count > 0:
            btc_val = Address.objects.filter(link=base_url).only("address")
            temp = []
            for i in btc_val:
                temp.append(i.address)
            result_list["bitcoin"] = temp
        else:
            result_list["bitcoin"] = []

        # ^ IP DATA
        ip_val_count = ipFound.objects.filter(link=base_url).count()
        if ip_val_count > 0:
            ip_val = ipFound.objects.filter(link=base_url).only("ip")
            temp = []
            for i in ip_val:
                temp.append(i.ip)
            result_list["ip"] = temp
        else:
            result_list["ip"] = []
        
        # ^ MAIL DATA
        mail_val_count = mailFound.objects.filter(link=base_url).count()
        if mail_val_count > 0:
            mail_val = mailFound.objects.filter(link=base_url).only("mail")
            temp = []
            for i in mail_val:
                temp.append(i.mail)
            result_list["mail"] = temp
        else:
            result_list["mail"] = []
        
        # ^ PHONE NUMBER DATA
        number_val_count = numberFound.objects.filter(link=base_url).count()
        if number_val_count > 0:
            number_val = numberFound.objects.filter(link=base_url).only("number")
            temp = []
            for i in number_val:
                temp.append(i.number)
            result_list["phone_number"] = temp
        else:
            result_list["phone_number"] = []
        
        # TODO - SHODAN
        
        # result_list["contains_nothing"] = bval["contains_nothing"]

        # if len(shodanw)>0:
        #     for shodan in shodanw:
        #         result_list["contains_shodan"] = True
        #         temp = {}
        #         temp["ip"] = shodan["ip"]
        #         temp["dns"] = shodan["dns"]
        #         temp["country"] = shodan["country"]
        #         temp["domains"] = shodan["domains"]
        #         result_list["shodan"] = temp
        # elif len(shodanw) == 0:
        #     result_list["contains_shodan"] = False

        # print(lk)

        # ^ CLEARNET LINK
        # TODO - CHANGE THIS SYSTEM - ENABLE URLs TO ACCESS PARENT URL + THEIR OWN
            
        clearnet_count = ClearnetLink.objects.filter(origin_link=input_link).count()

        if clearnet_count > 0:

            clearnet_dict = {}
            index = 1

            # ~ EXTRACT CLEARNET LINK DATA
            clearnet = ClearnetLink.objects.filter(origin_link=input_link).limit(10)
            
            for i in clearnet:
                clearnet_dict[index] = i.link
                index = index + 1

        else:
            clearnet_dict = {}
        
        result_list["clearnet"] = clearnet_dict

        # TODO - USERNAME CORRELATION

        # parsed_url = urlparse(input_link)
        # base_url = parsed_url.scheme + "://" + parsed_url.netloc

        # try:
        #     all_correlates = Correlate.objects.filter(link=base_url).limit(5)
        #     correlate_list = {}
        #     for i in all_correlates:
        #         correlate_list[str(i.onion_username)] = i.correlation
        # except:
        #     correlate_list = {}

        result_list["user_correlate"] = {}

        # ^ TOPIC MODELLING
        input_link_text = OnionLink.objects.get(link=input_link)

        plain_string_again = lzma.decompress(input_link_text.text).decode('utf-8')
        stop_separated = plain_string_again.split('.')
        stop_separated = stop_separated

        try:
            current_directory = os.path.dirname(os.path.realpath(__file__))
            current_directory = current_directory.split("/")
            current_directory.pop()
        except Exception as e:
            print("current directory issue")
        
        try:
            current_directory = os.path.join(*current_directory)
            filename = "glove-wiki-gigaword-300"
            file_path = os.path.join(current_directory, filename)
            file_path = "/"+file_path

            filename_check = "glove-wiki-gigaword-300.vectors.npy"
            file_path_check = os.path.join(current_directory, filename_check)
            file_path_check = "/"+file_path_check
        except Exception as e:
            print("join errors")
        
        try:
            if os.path.exists(file_path_check):
                pass
            else:
                output_file = 'glove-wiki-gigaword-300.vectors.npy'
                join_files("split_gigaword", output_file)
        
        except:
            print("join files error")
        
        try:
            file_path = str(file_path)
            unit = str(unit)
            glove_model = KeyedVectors.load(file_path)
            print(glove_model)
            html_code,dom,ml= vmain2([unit], glove_model)
        except Exception as e:
            print("glove model error")
            print(e)

        result_list["html_code"] = html_code
        result_list["dom"] = dom
        result_list["ml"] = ml
        
        return Response({'res':result_list})

@api_view(['POST'])
def bitcoin(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))

        # ~ EXPECTED POST RREQUEST DATA  - {'entered': ['132P7fT5qCXa3WE9PhRPaHRUh5EcF7Ut15']}
        # ~ THIS API REQUEST PROVIDES REACT WITH BITCOIN ADDRESS & TRANSACTION DATA
        
        bits = str(data["entered"][0])

        # ~ EXTRACT METADATA OF ADDRESS
        val = Address.objects.filter(address=str(bits)).only("current_balance","sent","received").first()

        # ~ MATCH TRANSACTION ID WITH ADDRESS AND EXTRACT DATA
        list_txn = TransactionId.objects.filter(address=str(bits))
        list_txn = [i.transaction for i in list_txn]
        list_txn = list(set(list_txn))

        # ~ REMOVE TRANSACTION WHOSE DATA WE DON'T HAVE
        for i in list_txn:
            dval_count = Transaction.objects.filter(txid=str(i)).count()
            if dval_count == 0:
                list_txn.remove(i)
        
        list_addr = []    
        index = 0
        node_label = []
        graph_node = []
        graph_edge = []
        node = {}

        # ^ ADD TRANSACTION NODES TO NODE LIST
        for node_link in list_txn:

            node = {}
            node["id"] = index # ID
            node["label"] = "transaction" # LABEL
            node["title"] = node_link # HOVER VALUE

            node_label.append(node_link)
            graph_node.append(node) # FINAL NODES FOR GIVING TO FRONTEND

            index = index + 1 # INCREMENT
            
        # ^ EXTRACT BTC NODES
        for i in list_txn:

            newval = Transaction.objects.filter(txid=str(i),status="receiver").only('address').distinct('address')

            for j in newval:
                list_addr.append(j)

            newval2 = Transaction.objects.filter(txid=str(i),status="sender").only('address').distinct('address')

            for j in newval2:
                list_addr.append(j)

        # ^ ADD BTC NODES TO NODE LIST
        for node_link in list_addr:

            node = {}
            node["id"] = index # ID
            node["label"] = "btc" # LABEL
            node["title"] = node_link # HOVER VALUE

            node_label.append(node_link)
            graph_node.append(node) # FINAL NODES FOR GIVING TO FRONTEND

            index = index + 1 # INCREMENT
        
        edges = {}
        final_val_from = []
        final_val_to = []

        # ^ CREATE EDGES (TO & FRO) VIA NODE LIST
        for i in list_txn:

            newval = Transaction.objects.filter(txid=str(i),status="receiver").only('address').distinct('address')

            for j in newval:
                final_val_from.append(node_label.index(i))
                final_val_to.append(node_label.index(j))
                
            newval2 = Transaction.objects.filter(txid=str(i),status="sender").only('address').distinct('address')

            for j in newval2:
                final_val_from.append(node_label.index(j))
                final_val_to.append(node_label.index(i))
        
        # ^ ADD EDGES TO FINAL LIST
        for receiver, sender in zip(final_val_to, final_val_from):

            edges = {}
            edges["from"] = sender
            edges["to"] = receiver

            graph_edge.append(edges)
            
            
        result_list = {}

        graph = {}
        graph["node"] = graph_node
        graph["edges"] = graph_edge

        result_list["graph"] = graph
        result_list["current_balance"] = val.current_balance
        result_list["sent"] = val.sent
        result_list["received"] = val.received
        result_list["transaction"] = len(list_txn)

        index = 1
        txn = {}

        # ^ TXN TABLE
        for i in list_txn:

            dval_count = Transaction.objects.filter(txid=str(i)).count()

            if dval_count > 0:

                dval = Transaction.objects.filter(txid=str(i)).only("txid","addr_amount","status","address").first()

                txn[index] = {}
                txn[index]["id"] = dval.txid
                txn[index]["amount"] = dval.addr_amount
                txn[index]["status"] = dval.status
                txn[index]["address"] = dval.address

                index = index + 1

        result_list["txn"] = txn

        return Response({'res':result_list})

@api_view(['POST'])
def flag(request):
    if request.method == "POST":
        # -------- API POST REQUEST -------- #
        data = json.loads(request.body.decode('utf-8'))
        # data = request.body.decode('utf-8')
        bits = str(data["link"])
        check = str(data["checked"])
        timeme = str(data["timestamp"])
        # my_model = Flaged(link=bits,flag=check,timestamp=timeme)
        # my_model.save()