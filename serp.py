import os
import requests
from dotenv import load_dotenv

load_dotenv()


def serp(keyword: str) -> list[dict]:
    login = os.getenv("DATAFORSEO_LOGIN")
    password = os.getenv("DATAFORSEO_PASSWORD")

    payload = [
        {
            "keyword": keyword,
            "location_code": 2840,  # United States
            "language_code": "en",
            "depth": 10,
        }
    ]

    response = requests.post(
        "https://api.dataforseo.com/v3/serp/google/organic/live/regular",
        auth=(login, password),
        json=payload,
    )
    response.raise_for_status()

    data = response.json()
    items = (
        data["tasks"][0]["result"][0]["items"]
        if data["tasks"][0]["result"]
        else []
    )

    results = []
    for item in items:
        if item.get("type") != "organic":
            continue
        results.append(
            {
                "title": item.get("title"),
                "domain": item.get("domain"),
                "url": item.get("url"),
            }
        )
        if len(results) == 10:
            break

    return results
