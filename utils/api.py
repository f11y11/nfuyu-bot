import aiohttp

from bot.bot import config

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
        self.SUBDOMAIN = subdomain
        self.VERSION = config.get('api_version') or 1

    async def get(self, path: str, params: dict):
        """
        Performs a GET request on the server
            Parameters:
                path (string): request address
                params (list): key: value pairs of query parameters
            Returns:
                {data: ..., success: boolean}
        """

        query_params = '&'.join([f'{k}={v}' for k, v in params.items()])

        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.request(
                    'GET', f'https://{self.SUBDOMAIN}.{BASE_URL}/v{self.VERSION}/{path}?{query_params}'
            ) as response:
                data = await response.json(content_type=None)

                if str(response.status).startswith('2'):
                    return data

                raise ValueError("Request failed")


avatars = SubdomainHandler(subdomain='a')
api = SubdomainHandler(subdomain='api')
osu = SubdomainHandler(subdomain='osu')
beatmaps = SubdomainHandler(subdomain='b')
server = SubdomainHandler(subdomain='c')

