from toolkit.settings_common import *

ROOT_URLCONF = 'toolkit.urls_flat'

MULTIROOM_ENABLED = True
HTML_MAILOUT_ENABLED = True
MEMBERSHIP_EXPIRY_ENABLED = True

VENUE = {
    'name': 'Star and Shadow',
    'longname': 'Star and Shadow',
    'cinemaname': 'Star and Shadow Cinema',
    'url': 'https://starandshadow.xtreamlab.net/',
    'contact_page': '/about/contact/',
    'piwik_id': 29,
    'twitter': 'https://twitter.com/StarAndShadow',
    'facebook': 'https://www.facebook.com/StarAndShadow',
    'instagram': 'https://www.instagram.com/starandshadowcinema/',
    'flickr': '',
    'vimeo': '',
    'youtube': 'https://www.youtube.com/channel/UCJxp1CvJlDsWBEJrguvhoLw/',
    'nav_menu_img': 'content/ss_logo_e3cae3_pink3.jpg',
    'internal_header_img': 'content/star_and_shadow_100_82.png',
    'wagtale_admin_img': '/static/content/star_and_shadow_100_82.png',
    'favicon': '/static/favicon/favicon_ss.ico',
    'font_h2': 'https://fonts.googleapis.com/css?family=Lato',
    # This is used as the hostname for unsubscribe links in emails
    # i.e. emails will have links added to
    # [this]/members/100/unsubscribe)
    'email_unsubscribe_host': 'http://arnold.local:8000',
    # Default address to which reports of a successful mailout
    # delivery are sent:
    'mailout_delivery_report_to': u'admin@starandshadow.org.uk',
    # "From" address for mailout
    'mailout_from_address': u'mailout@starandshadow.org.uk',
    'show_user_management': True
}

WAGTAIL_SITE_NAME = 'The Star and Shadow'

# Disable 'allow editing from magic IP range' for now
CUBE_IP_ADDRESSES = ()

DEFAULT_MUGSHOT = "/static/members/default_mugshot.gif"

# Currently only used for setting an outer limit on what year printed
# programmes can be uploaded
DAWN_OF_TIME = 1998

###############################################################################
#
# Below here are Django settings
#

ADMINS = (
    # ('Your Name', 'your_email@example.com')
)

TEMPLATES[0]['DIRS'] = (
    os.path.join(BASE_DIR, 'star_and_shadow_templates'),
    os.path.join(BASE_DIR, 'templates'),
)
