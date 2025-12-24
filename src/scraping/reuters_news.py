def scrape_reuters(symbol):
    url = f"https://www.reuters.com/companies/{symbol}.OQ"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    data = []
    for h in soup.find_all("h3"):
        data.append({
            "symbol": symbol,
            "source": "Reuters",
            "headline": h.text.strip(),
            "published_at": datetime.now()
        })

    return pd.DataFrame(data)
