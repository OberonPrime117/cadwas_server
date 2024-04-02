from mongoengine import EmbeddedDocumentField, EmbeddedDocument, BinaryField, IntField, BooleanField, ListField, Document, StringField, DateTimeField, ImageField

# -----------------------------
# GENERAL
# -----------------------------

class Hold(Document):
    unitval = StringField(required=True, default="search")
    currentStat = StringField(required=True)
    time = DateTimeField(required=True)

# -----------------------------
# DETAILS EXTRACT - STATUS
# -----------------------------

class LinkStatus(Document):
    link = StringField(required=True, unique=True)
    status = BooleanField(required=True) # True, False - online/offline

# -----------------------------
# LINK EXTRACT
# -----------------------------

class Relation(Document):
    link = StringField(required=True, unique=True)
    base_url = StringField(required=True)
    parent_url = StringField(required=True)

class Category(Document):
    base_url = StringField(required=True, unique=True)
    category = StringField(required=True, default="Orphan") # LINK DIRECTORY , VENDOR , FORUM , OTHER

# -----------------------------
# KEYWORD EXTRACT - KEYWORD
# -----------------------------

class Keyword(Document):
    link = StringField(required=True)
    keyword = StringField(required=True)

# -----------------------------
# DATA EXTRACT
# -----------------------------

class ipFound(Document):
    link = StringField(required=True)
    ip = StringField(required=True)

class mailFound(Document):
    link = StringField(required=True)
    mail = StringField(required=True)

class numberFound(Document):
    link = StringField(required=True)
    number = StringField(required=True)

# -----------------------------
# LINK DATA
# -----------------------------

'''
SCENARIO 1 : TWO RESOURCES ARE AVAILABLE ON TWO WEBSITES. CORRELATE THEM
SCENARIO 2 : TWO LINKS COME FROM TWO LINK DIRECTORIES. CORRELATE THEM

IN SCENARIO 2, CORRELATION NEEDS TO BE DONE WITH LINK EXTRACT CLASS, NOT ONION LINK CLASS
KEEPING ONION LINK AS UNIQUE LINK FOR NOW
'''

class MultimediaLink(Document):
    link = StringField(required=True, unique=True)
    origin_link = StringField(required=True) # IMAGE LINK

class ImageLink(Document):
    link = StringField(required=True, unique=True)
    origin_link = StringField(required=True) # IMAGE LINK

class ClearnetLink(Document):
    link = StringField(required=True)
    origin_link = StringField(required=True)

class FileLink(Document):
    link = StringField(required=True)
    origin_link = StringField(required=True)

class MailtoLink(Document):
    link = StringField(required=True)
    origin_link = StringField(required=True)

class OnionLink(Document):
    link = StringField(required=True, unique=True)
    html = BinaryField(required=True)
    text = BinaryField(required=True)
    title = StringField(required=True)
    domain = StringField(required=True, default="Other")
    processed_text = BinaryField(required=True)

# -----------------------------
# DONE, VISITED, CONTAINS
# -----------------------------

class BaseDone(Document):
    base_url = StringField(required=True, unique=True)
    category_done = BooleanField(required=True, default=False)
    shodan_done = BooleanField(required=True, default=False)
    selenium_done = BooleanField(required=True, default=False)

class BaseContains(Document):
    base_url = StringField(required=True, unique=True)
    contains_shodan = BooleanField(required=True, default=False)

class LinkDone(Document):
    link = StringField(required=True, unique=True)
    types = StringField(required=True) # donated, interval, important
    time = DateTimeField(required=True) # TIME ADDED TO CRAWL QUEUE (EITHER DNT OR IMP)
    detail_done = BooleanField(required=True, default=False)
    data_done = BooleanField(required=True, default=False)
    bitcoin_done = BooleanField(required=True, default=False)
    keyword_done = BooleanField(required=True, default=False)
    link_done = BooleanField(required=True, default=False)
    image_multimedia_done = BooleanField(required=True, default=True)

# DONE MECHANISM FOR INTERVAL MECHANISM
class LinkContains(Document):
    link = StringField(required=True, unique=True)
    contains_html = BooleanField(required=True, default=False)
    contains_text = BooleanField(required=True, default=False)
    contains_processed = BooleanField(required=True, default=False)
    contains_keyword = BooleanField(required=True, default=False)
    contains_domain = BooleanField(required=True, default=False)
    contains_data = BooleanField(required=True, default=False)
    contains_image = BooleanField(required=True, default=False)
    contains_multimedia = BooleanField(required=True, default=False)
    contains_bitcoin = BooleanField(required=True, default=False)
    contains_ip = BooleanField(required=True, default=False)
    contains_mail = BooleanField(required=True, default=False)
    contains_number = BooleanField(required=True, default=False)
    contains_captcha = BooleanField(required=True, default=False)

# VISITED AT LEAST ONCE ?
class LinkVisited(Document):
    link = StringField(required=True, unique=True)
    time = DateTimeField(required=True) # OG TIME ADDED
    detail_visited = BooleanField(required=True, default=False)
    data_visited = BooleanField(required=True, default=False)
    bitcoin_visited = BooleanField(required=True, default=False)
    keyword_visited = BooleanField(required=True, default=False)
    link_visited = BooleanField(required=True, default=False)

# -----------------------------
# BITCOIN EXTRACT
# -----------------------------

class Address(Document):
    link = StringField(required=True)
    address = StringField(required = True)
    current_balance = StringField(required = True)
    sent = StringField(required=True)
    received = StringField(required=True)

class TransactionId(Document):
    address = StringField(required=True)
    transaction = StringField(required=True)

class Transaction(Document):
    address = StringField(required=True)
    addr_amount = IntField(required=True)
    txid = StringField(required=True)
    status = StringField(required=True) # INPUT OUTPUT
    referral_address = StringField(required=True)
    link = StringField(required=True)
    timestamp = DateTimeField(required=True)

# -----------------------------
# FORUM
# -----------------------------

class Account(Document):
    link = StringField(required=True)
    username = StringField(required=False)
    email = StringField(required=False)
    password = StringField(required=True)

class Identifier(Document):
    value = StringField(required=True) # identifier
    link = StringField(required=True) # link
    type = StringField(required=True) # user , post , subreddit
    contains_addon = BooleanField(required=False)
    limit_val = StringField(required=False)
    contains_limit = BooleanField(required=False)

class NewIdentifier(Document):
    link = StringField(required=True) # link
    value = StringField(required=True) # identifier
    base_url = StringField(required=True) # link
    types = StringField(required=True) # user , post , subreddit

class IdentifierContains(Document):
    link = StringField(required=True)
    contains_addon = BooleanField(required=True, default=False)
    contains_double = BooleanField(required=True, default=False) # /f/post
    contains_php = BooleanField(required=True, default=False) # /PHPSESSID=ADSDADWD

# -----------------------------
# SHODAN EXTRACT
# -----------------------------

class Shodan(Document):
    link = StringField(required=True, unique=True)
    ip = StringField(required=True)
    dns = StringField(required=True)
    country = StringField(required=True)

class ShodanDomain(Document):
    link = StringField(required=True)
    domains = StringField(required=True)

# -----------------------------
# ERROR DETECTION AND DOCUMENTATION
# -----------------------------

class ErrorDetected(Document):
    link = StringField(required=True)
    error = StringField(required=True) # EXCEPTION ERROR
    filename = StringField(required=True) # FILENAME

'''
class Forum(Document):
    link = StringField(required=True) # individual links
    contains_timestamp = BooleanField(required=True,default=False)
    contains_username = BooleanField(required=True,default=False)
    contains_role = BooleanField(required=True,default=False)
    contains_post = BooleanField(required=True,default=False)
    contains_class_approach = BooleanField(required=True,default=False)
    requires_selenium = BooleanField(required=True,default=False)
    contains_captcha = BooleanField(required=True,default=False)
    contains_post_number = BooleanField(required=True,default=False)
    contains_views_number = BooleanField(required=True,default=False)
    contains_replies_number = BooleanField(required=True,default=False)
contains_addon = BooleanField(required=True,default=False)
limit_val = StringField(required=False)
contains_limit = BooleanField(required=False)
'''

# -----------------------------
# REDDIT
# -----------------------------

class RedditPost(Document):
    title = StringField(required = True)
    author = StringField(required = True)
    score = IntField(required = True)
    num_comments = IntField(required = True)
    created_utc = DateTimeField(required = True)

# IT SCRAPES HOT 50K POSTS
# THE HOT POST KEEP CHANGING, 
# THUS, SCRAPING NEEDS TO BE PERIODIC

class RedditStatus(Document):
    status = BooleanField(required=True)
    time = DateTimeField(required=True)

class RedditCorrelation(Document):
    link = StringField(required=True)
    onion_username = StringField(required=True)
    correlation = ListField(StringField(required=True))

class Flaged(Document):
    link = StringField(required=True)
    flag = StringField(required=True)
    timestamp = DateTimeField(required=True)