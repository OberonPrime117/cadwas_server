from mongoengine import IntField, EmbeddedDocument, FloatField, BooleanField, ListField, Document, StringField, DateTimeField, ImageField, EmbeddedDocumentField

class LinkData(Document):

    parent_link = StringField(required=True)
    link = StringField(required=True, unique=True)
    base_link = StringField(required=True)
    type = StringField(required=True)
    status = BooleanField(required=False, null=True)
    time_last_crawled = DateTimeField(required=False, null=True)
    title = StringField(required=False, null=True)
    text = StringField(required=False, null=True)
    html = StringField(required=False, null=True)

    # EXTRACTION STATUS
    detail_done = BooleanField(required=False, default=False)
    lemma_done = BooleanField(required=False, default=False)
    link_done = BooleanField(required=False, default=False)
    keyword_done = BooleanField(required=False, default=False)
    bitcoin_done = BooleanField(required=False, default=False)
    data_done = BooleanField(required=False, default=False)
    selenium_done = BooleanField(required=False, default=False)
    shodan_done = BooleanField(required=False, default=False)

    # INFORMATION EXTRACTED
    links_extracted = ListField(StringField(required=False,null=True))
    processed_text = StringField(required=False, null=True)
    wc_images = ImageField(required=False, null=True)
    keyword = ListField(StringField(required=False,null=True))
    bitcoin = ListField(StringField(required=False,null=True))
    ip = ListField(StringField(required=False,null=True))
    mail = ListField(StringField(required=False,null=True))
    phone_number = ListField(StringField(required=False,null=True))
    contains_captcha = BooleanField(required=False,null=True)
    contains_data = BooleanField(required=False)
    contains_nothing = BooleanField(required=False)

class Address(Document):
    link = StringField(required=True)
    address = StringField(required = True)
    current_balance = StringField(required = True)
    sent = StringField(required=True)
    received = StringField(required=True)
    transaction = ListField(StringField(required=True))

# class Transaction(EmbeddedDocument):
#     id = StringField(required = True)
#     direction = StringField(required = True)
#     amount = FloatField(required = True)
#     balance_before_tx = FloatField(required=True)
#     balance_after_tx = FloatField(required=True)
#     address = ListField(EmbeddedDocumentField(Address))

class Transaction(Document):
    address = StringField(required=True)
    addr_amount = IntField(required=True)
    txid = StringField(required=True)
    status = StringField(required=True) # INPUT OUTPUT
    referral_address = StringField(required=True)
    link = StringField(required=True)

class Account(Document):
    link = StringField(required=True)
    username = StringField(required=True)
    password = StringField(required=True)

class ShodanMe(Document):
    link = StringField(required=True)
    ip = StringField(required=True)
    dns = StringField(required=True)
    country = StringField(required=True)
    domains = ListField(StringField(required=True))

class SeleniumLinks(Document):
    old_link = StringField(required=True)
    new_link = StringField(required=True)
    html = StringField(required=True)
    new_html = StringField(required=True)
    js_html = StringField(required=False)

class ClearnetLink(Document):
    link = StringField(required = True, unique=True)
    origin_link = StringField(required = True)

class Username(Document):
    username = StringField(required = True, unique=True)
    link = StringField(required = True)
    user_link = StringField(required = True)

class Post(Document):
    post = StringField(required = True, unique=True)
    link = StringField(required = True)
    post_link = StringField(required = True)

class Subreddit(Document):
    subreddit = StringField(required = True, unique=True)
    link = StringField(required = True)
    subreddit_link = StringField(required = True)

class Hold(Document):
    type = StringField(required=True)
    link = StringField(required=True)
    # detail = BooleanField(required=True,default=False)
    # bitcoin = BooleanField(required=True,default=False)
    # data = BooleanField(required=True,default=False)
    # keyword = BooleanField(required=True,default=False)
    # lemma = BooleanField(required=True,default=False)
    # link = BooleanField(required=True,default=False)
    # selenium = BooleanField(required=True,default=False)
    # shodan = BooleanField(required=True,default=False)

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

class BaseURL(Document):
    link = StringField(required=True)
    type = StringField(required=True)

class DomainClass(Document):
    link = StringField(required=True) # link
    domain = StringField(required=True) # identifier

class Correlate(Document):
    link = StringField()
    onion_username = StringField()
    correlation = ListField(StringField())

class Flaged(Document):
    link = StringField(required=True)
    flag = StringField(required=True)
    timestamp = DateTimeField(required=True)