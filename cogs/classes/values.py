from locale import getlocale

BASE = 'https://{region}.api.riotgames.com/'
LOCALE = getlocale()[0].replace('_', '-')
ROUTES = ('americas', 'asia', 'europe')

REGIONS = (
    'eu', 'eune', 'euw', 'jp', 'kr', 'lan', 'br',
    'las', 'na', 'oce', 'ru', 'tr', 'latam', 'ap'
)

ENDPOINTS = {

}

HEADERS = {
    'Accept-Charset' : 'application/x-www-form-urlencoded; charset=UTF-8'
}