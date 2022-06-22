# Connection to the private server's API with support of any possible subdomain

import asyncio
from typing import Tuple, Union
import aiohttp
from bot.bot import config

BASE_URL = config.get('domain')

async def req(subdomain, endpoint, method='GET', params={}) -> Tuple[Union[dict, str], bool]:
    '''
    #### Make a request to your private server's API

    - subdomain: subdomain ex: api, osu, a, b, c
    - endpoint: request endpoint ex: /get_player_scores
    - method: http method (optional, GET by default)
    - params: dict

    #### Returns:
    dict | str: JSON or response text
    bool: False if there are errors either in the function or the request
    '''
    if method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
        return 'Invalid HTTP method', False
    async with aiohttp.ClientSession() as session:
        async with session.request(method, 'https://%s.%s/%s' % (subdomain, BASE_URL, endpoint), params=dict(filter(lambda k: k[1] != None, params.items()))) as r:
            r: aiohttp.ClientResponse
            content = await r.json(content_type=None)
            return content, str(r.status).startswith('2')