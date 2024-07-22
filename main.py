import requests

def get_hits():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Origin': 'https://www.pittarosso.com',
        'Referer': 'https://www.pittarosso.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = '{"requests":[{"indexName":"shopify_prod_products","params":"analyticsTags=%5B%22device%3Amobile%22%2C%22os%3Adroid%22%5D&clickAnalytics=true&distinct=1&facets=%5B%5D&filters=inventory_available%3Atrue%20AND%20price%20%3E%200&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=100000&query=&tagFilters="}]}'

    response = requests.post(
        'https://cmqtx6qv1x-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.23.3)%3B%20Browser%20(lite)%3B%20JS%20Helper%20(3.14.0)%3B%20react%20(18.3.1)%3B%20react-instantsearch%20(6.40.4)&x-algolia-api-key=506d21d2a74394abc76c10684c5c90ea&x-algolia-application-id=CMQTX6QV1X',
        headers=headers,
        data=data,
    ).json()

    hits = response["results"][0]["hits"]
    return hits

def get_articoli(hits):
    articoli = []

    for hit in hits:
        articoli.append({
            "nome": hit["title"],
            "prezzo": hit["price"],
            "url": "https://www.pittarosso.com/it/"+hit["handle"]+"-p",
            "product_type": hit["product_type"],
            "inventory_quantity": hit["inventory_quantity"],
            "image": hit["image"],
            "prezzo_vecchio": hit["compare_at_price"],
            "sconto": int((1-hit["price_ratio"])*100)
        })
    return articoli

def order_by(articoli, key, desc=False):
    return sorted(articoli, key=lambda x: x[key], reverse=desc)

# Generate HTML page from articoli
def generate_HTML(articoli):
    html = """
    <html>
    <head>
        <title>Articoli</title>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            
            th, td {
                text-align: left;
                padding: 8px;
            }
            
            th {
                background-color: #f2f2f2;
            }
            
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
         <script>
            function filterProducts() {
                var input, filter, table, tr, td, i, txtValue;
                input = document.getElementById("searchBar");
                filter = input.value.toUpperCase();
                table = document.getElementById("productsTable");
                tr = table.getElementsByTagName("tr");

                for (i = 0; i < tr.length; i++) {
                    td = tr[i].getElementsByTagName("td")[1]; // Column index for product name
                    if (td) {
                        txtValue = td.textContent || td.innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {
                            tr[i].style.display = "";
                        } else {
                            tr[i].style.display = "none";
                        }
                    }       
                }
            }
        </script>
    </head>
    <body>
        <h1>Articoli</h1>
        Cerca <input type="text" id="searchBar" onkeyup="filterProducts()" placeholder="Nome prodotto...">
        <table id='productsTable'>
            <tr>
                <th>Image</th>
                <th>Nome</th>
                <th>Prezzo</th>
                <th>Sconto</th>
                <th>Product Type</th>
                <th>Inventory Quantity</th>
                <th>Link</th>
            </tr>
    """

    for articolo in articoli:
        html += f"""
            <tr>
                <td><img src="{articolo["image"]}" width="100" height="100"></td>
                <td>{articolo["nome"]}</td>
                <td>{articolo["prezzo"]}</td>
                <td>{articolo["sconto"]}%</td>
                <td>{articolo["product_type"]}</td>
                <td>{articolo["inventory_quantity"]}</td>
                <td><a href="{articolo["url"]}">Vai al prodotto</a></td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    with open("articoli.html", "w") as f:
        f.write(html)


def main():
    hits = get_hits()
    articoli = get_articoli(hits)
    articoli = order_by(articoli, "sconto", desc=True)
    generate_HTML(articoli)


if __name__ == "__main__":
    main()
