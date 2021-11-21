from typing import Optional
from datetime import datetime
from fastapi import FastAPI
from fastapi import APIRouter

from app.v1.endpoint.s3_endpoint import s3_endpoint, create_csv_file
from app.core.config import settings
from app.core.aiohttpclient import AiohttpClient

app = FastAPI()
router = APIRouter()
ct = datetime.now().date()

@router.get('/everything')
async def get_news(
    q: str = 'all',
    q_in_title: str = '',
    sources: Optional[str] = '',
    domains: Optional[str] = '',
    exclude_domains: Optional[str] = '',
    date_from: Optional[str] = '',
    date_to: Optional[str] = '',
    language: Optional[str] = '',
    sort_by: Optional[str] = '',
    page_size: Optional[int] = 100,
    page: Optional[int] = 1
):
    url = f'https://newsapi.org/v2/everything?q={q}&qInTitle={q_in_title}&sources={sources}&from={date_from}' \
          f'&domains={domains}&excludeDomains={exclude_domains}&to={date_to}&language={language}' \
          f'&sortBy={sort_by}&pageSize={page_size}&page={page}&apiKey={settings.API_KEY}'
    return await AiohttpClient.get(url, ssl=False)


@router.get('/top-headlines')
async def get_top_headlines(
    country: Optional[str] = 'us',
    category: Optional[str] = 'business',
    sources: Optional[str] = '',
    q: Optional[str] = '',
    page_size: Optional[int] = 20,
    page: Optional[int] = None
        ):
    url = f'https://newsapi.org/v2/top-headlines?country={country}&category={category}&sources={sources}' \
          f'&q={q}&pageSize={page_size}&page={page}&apiKey={settings.API_KEY}'
    return await AiohttpClient.get(url, ssl=False)


@router.get('/sources')
async def get_sources(
    country: Optional[str] = '',
    category: Optional[str] = '',
    language: Optional[str] = '',
        ):
    url = f'https://newsapi.org/v2/top-headlines/sources?country={country}&category={category}' \
          f'&language={language}&apiKey={settings.API_KEY}'
    return await AiohttpClient.get(url, ssl=False)


@router.get('get_s3_client')
async def get_s3_client():
    data = await get_news(language='en', date_from=str(ct))
    data_file = []
    for i in data['articles']:
        data_file.append([i['author'], i['source']['name'], i['url']])

    file_name = create_csv_file(data_file)
    return s3_endpoint(file_name)
