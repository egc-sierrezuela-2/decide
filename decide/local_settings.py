ALLOWED_HOSTS = ["*"]

# Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
    'social_django',
]

APIS = {
    'authentication': 'http://localhost:8000',
    'base': 'http://localhost:8000',
    'booth': 'hhttp://localhost:8000',
    'census': 'http://localhost:8000',
    'mixnet': 'http://localhost:8000',
    'postproc': 'http://localhost:8000',
    'store': 'http://localhost:8000',
    'visualizer': 'http://localhost:8000',
    'voting': 'http://localhost:8000',
}

BASEURL = 'http://localhost:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'decide',
        'USER': 'decide',
        'PASSWORD': 'decide',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

AUTH_AUTHENTICATION_TYPE = 'both'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'login-success'
LOGOUT_REDIRECT_URL = 'login'

SOCIAL_AUTH_FACEBOOK_KEY = '1006606710196386'
SOCIAL_AUTH_FACEBOOK_SECRET = '12d5bc07c1c41cea14846e85bbe4b460'

SOCIAL_AUTH_GITHUB_KEY = '1d28207db9b47ce585ea'
SOCIAL_AUTH_GITHUB_SECRET = '4da7a5f6d9cf1d91572ad09b62a561df393a7d64'


SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '78ppaogakulk4n'         # Client ID
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = 'aAr8rmN2zlEzw6Vz' # Client Secret
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_liteprofile', 'r_emailaddress']
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['email-address', 'formatted-name', 'public-profile-url', 'picture-url']
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
    ('id', 'id'),
    ('formattedName', 'name'),
    ('emailAddress', 'email_address'),
    ('pictureUrl', 'picture_url'),
    ('publicProfileUrl', 'profile_url'),
]


AUTHENTICATION_BACKENDS = (
    'authentication.backends.EmailOrUsernameModelBackend',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.github.GithubOAuth2',
)

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256
