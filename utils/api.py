import aiohttp

from bot.bot import config
from utils.timer import Timer

__all__ = (
    'avatars',
    'api',
    'osu',
    'beatmaps',
    'server'
)

BASE_URL = config.get('domain')


class SubdomainHandler:
    def __init__(self, subdomain):
        self._SUBDOMAIN = subdomain
        self._VERSION = (config.get('api_version'))

    @property
    def version(self):
        """
        Version part of the URL
        :return: str
        """

        return f'v{self._VERSION}' if self._VERSION else ''

    @property
    def url(self):
        """
        Constructs the target request URL by combining subdomain, base URL and API version
        :return: str
        """

        return f'https://{self._SUBDOMAIN}.{BASE_URL}/{self.version}'

    async def get(self, path: str, params: dict = None):
        """
        Performs a GET request on the server
        :param: path (string): request address
        :param: params (list): key: value pairs of query parameters
        :return: dict
        """
        params = params or {}
        query_params = '&'.join([f'{k}={v}' for k, v in params.items()])

        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.request(
                    'GET', f'{self.url}{path}?{query_params}'
            ) as response:
                data = await response.json(content_type=None)

            if str(response.status).startswith('2'):
                return data

            raise ValueError('Unexpected data received from the server.')

    async def latency(self):
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with Timer() as t:
                async with session.request(
                        'GET', f'{self.url}'
                ):
                    pass

            return t.result


avatars = SubdomainHandler(subdomain='a')
api = SubdomainHandler(subdomain='api')
osu = SubdomainHandler(subdomain='osu')
beatmaps = SubdomainHandler(subdomain='b')
server = SubdomainHandler(subdomain='c')

