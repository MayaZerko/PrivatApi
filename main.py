import asyncio
import sys
import aiohttp

from constants import BASE_URL
from utils import get_days, get_few_dates, get_currencies


async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    return await response.json()
                return {'error_status': response.status, 'details': await response.text()}
        except aiohttp.ClientConnectorError as e:
            return {'errorStatus': e.errno, 'details': e}


def adapter_response(response, currencies=('EUR', 'USD')) -> dict:
    exchange_rate = response['exchangeRate']
    rates = {
        rate.get('currency'): {'sale': rate.get('saleRate', rate.get('saleRateNB')),
                                 'purchase': rate.get('purchaseRate', rate.get('purchaseRateNB'))}
        for rate in exchange_rate if rate.get('currency', '') in currencies
    }
    return rates


async def get_rate(day, currencies) -> dict:
    url = f'{BASE_URL}{day}'
    response = await request(url)
    if 'exchangeRate' in response:
        return {day: adapter_response(response, currencies)}
    return {day: response}


async def get_rates(few_days, currencies) -> tuple:
    results = [get_rate(day, currencies) for day in few_days]
    return await asyncio.gather(*results, return_exceptions=True)


def main():
    days = get_days(sys.argv)
    few_days = get_few_dates(days)
    currencies = get_currencies(sys.argv)
    exchange_rate = asyncio.run(get_rates(few_days, currencies))
    print(exchange_rate)


if __name__ == "__main__":
    exit(main())
