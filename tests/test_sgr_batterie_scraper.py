import unittest

from sgr_batterie_scraper import (
    extract_product_links,
    flatten_products,
    parse_product,
    BatteryProduct,
)


class ScraperParserTests(unittest.TestCase):
    def test_extract_product_links_supports_relative_and_absolute_urls(self):
        html = """
        <html>
          <body>
            <a href="/it/prodotto/bat-1">Batteria 12V</a>
            <a href="https://example.com/product/bat-2">Battery AGM</a>
            <a href="/contatti">Contatti</a>
          </body>
        </html>
        """
        links = extract_product_links(html, "https://www.sgr-it.com/it/ricerca.html")
        self.assertIn("https://www.sgr-it.com/it/prodotto/bat-1", links)
        self.assertIn("https://example.com/product/bat-2", links)

    def test_parse_product_returns_none_for_non_battery_page(self):
        html = """
        <html>
          <head><title>Filtro olio</title></head>
          <body><h1>Filtro olio motore</h1></body>
        </html>
        """
        self.assertIsNone(parse_product(html, "https://www.sgr-it.com/prodotto/filtro"))

    def test_parse_product_extracts_specs_for_battery_page(self):
        html = """
        <html>
          <head><title>Batteria AGM 12V</title></head>
          <body>
            <h1>Batteria AGM 12V</h1>
            <div class="description">Batteria ad alte prestazioni.</div>
            <table>
              <tr><th>Tensione</th><td>12V</td></tr>
              <tr><th>Capacità</th><td>9Ah</td></tr>
            </table>
          </body>
        </html>
        """
        product = parse_product(html, "https://www.sgr-it.com/prodotto/bat-1")
        self.assertIsNotNone(product)
        assert product is not None
        self.assertEqual(product.title, "Batteria AGM 12V")
        self.assertEqual(product.specs.get("Tensione"), "12V")
        self.assertEqual(product.specs.get("Capacità"), "9Ah")

    def test_flatten_products_adds_spec_prefix(self):
        products = [
            BatteryProduct(
                title="Batteria Test",
                url="https://www.sgr-it.com/prodotto/bat",
                specs={"Tensione": "12V"},
            )
        ]
        rows = flatten_products(products)
        self.assertEqual(rows[0]["spec_Tensione"], "12V")


if __name__ == "__main__":
    unittest.main()
