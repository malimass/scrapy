"""Scraper per estrarre i dati delle batterie dal sito SGR.

Uso rapido:
    python sgr_batterie_scraper.py \
        --search-url "https://www.sgr-it.com/it/ricerca.html?token=..." \
        --output batterie.csv

Lo script:
1. scarica la pagina di ricerca,
2. individua i link ai prodotti,
3. filtra i prodotti che sembrano batterie,
4. visita ogni dettaglio prodotto,
5. esporta i dati in CSV e/o JSON.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Iterator
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

BATTERY_KEYWORDS = [
    "batteria",
    "batterie",
    "battery",
    "accumulatore",
    "lithium",
    "litio",
    "agm",
]

PRODUCT_LINK_SELECTORS = [
    "a[href*='prodotto']",
    "a[href*='product']",
    "a[href*='ricambi']",
    "a.card",
    "article a[href]",
    ".product a[href]",
]

TITLE_SELECTORS = ["h1", ".product-title", ".page-title", "title"]


@dataclass
class BatteryProduct:
    title: str
    url: str
    code: str = ""
    brand: str = ""
    description: str = ""
    specs: dict[str, str] = field(default_factory=dict)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def is_battery_text(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in BATTERY_KEYWORDS)


def fetch(session: requests.Session, url: str, timeout: int = 30) -> str:
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def extract_product_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: set[str] = set()

    for selector in PRODUCT_LINK_SELECTORS:
        for anchor in soup.select(selector):
            href = anchor.get("href")
            if not href:
                continue
            full_url = urljoin(base_url, href)
            links.add(full_url)

    # fallback: qualsiasi link che sembra riferito ai prodotti
    for anchor in soup.select("a[href]"):
        href = anchor.get("href", "")
        text = clean_text(anchor.get_text(" "))
        combined = f"{href} {text}".lower()
        if "prod" in combined or is_battery_text(combined):
            links.add(urljoin(base_url, href))

    return sorted(links)


def extract_title(soup: BeautifulSoup) -> str:
    for selector in TITLE_SELECTORS:
        node = soup.select_one(selector)
        if node:
            text = clean_text(node.get_text(" "))
            if text:
                return text
    return ""


def extract_specs(soup: BeautifulSoup) -> dict[str, str]:
    specs: dict[str, str] = {}

    for row in soup.select("table tr"):
        columns = row.find_all(["th", "td"])
        if len(columns) < 2:
            continue
        key = clean_text(columns[0].get_text(" "))
        value = clean_text(columns[1].get_text(" "))
        if key and value:
            specs[key] = value

    for item in soup.select(".specs li, .product-features li, .characteristics li"):
        raw = clean_text(item.get_text(" "))
        if ":" in raw:
            key, value = [clean_text(part) for part in raw.split(":", 1)]
            if key and value and key not in specs:
                specs[key] = value

    return specs


def extract_code(text: str) -> str:
    match = re.search(r"\b(?:cod(?:ice)?|sku|articolo)\s*[:#-]?\s*([A-Z0-9._/-]{3,})", text, re.I)
    return match.group(1).strip() if match else ""


def extract_brand(text: str) -> str:
    match = re.search(r"\b(?:marca|brand)\s*[:#-]?\s*([\w\s.-]{2,40})", text, re.I)
    return clean_text(match.group(1)) if match else ""


def parse_product(html: str, product_url: str) -> BatteryProduct | None:
    soup = BeautifulSoup(html, "html.parser")
    title = extract_title(soup)

    content_text = clean_text(soup.get_text(" "))
    if not is_battery_text(f"{title} {content_text}"):
        return None

    description_node = soup.select_one(".description, .product-description, .desc")
    description = clean_text(description_node.get_text(" ")) if description_node else ""

    specs = extract_specs(soup)

    code = extract_code(content_text)
    brand = extract_brand(content_text)

    return BatteryProduct(
        title=title,
        url=product_url,
        code=code,
        brand=brand,
        description=description,
        specs=specs,
    )


def iter_battery_products(session: requests.Session, search_url: str) -> Iterator[BatteryProduct]:
    search_html = fetch(session, search_url)
    candidate_links = extract_product_links(search_html, search_url)

    for link in candidate_links:
        try:
            html = fetch(session, link)
            product = parse_product(html, link)
            if product:
                yield product
        except requests.RequestException:
            continue


def flatten_products(products: Iterable[BatteryProduct]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for product in products:
        base = asdict(product)
        specs = base.pop("specs", {})
        row = {**base}
        row.update({f"spec_{k}": v for k, v in specs.items()})
        rows.append(row)

    return rows


def save_outputs(rows: list[dict[str, str]], output_csv: Path | None, output_json: Path | None) -> None:
    if output_csv:
        df = pd.DataFrame(rows)
        df.to_csv(output_csv, index=False)

    if output_json:
        output_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scraper batterie SGR")
    parser.add_argument("--search-url", required=True, help="URL pagina ricerca SGR")
    parser.add_argument("--output", dest="output_csv", default="batterie_sgr.csv", help="File CSV output")
    parser.add_argument("--output-json", dest="output_json", default="", help="File JSON output opzionale")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout richieste HTTP in secondi")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    products = list(iter_battery_products(session, args.search_url))
    rows = flatten_products(products)

    output_csv = Path(args.output_csv) if args.output_csv else None
    output_json = Path(args.output_json) if args.output_json else None

    save_outputs(rows, output_csv, output_json)

    print(f"Prodotti batteria trovati: {len(rows)}")
    if output_csv:
        print(f"CSV salvato in: {output_csv}")
    if output_json:
        print(f"JSON salvato in: {output_json}")


if __name__ == "__main__":
    main()
