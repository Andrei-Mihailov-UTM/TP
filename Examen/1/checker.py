import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    return "https://" + host + "/" + path.lstrip("/")
    pass


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")
    pass


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    result = check_site(url)
    print("Status:", result["status"])
    if result["status"] is None:
        print("Eroare:", result["error"])
    else:
        print("Content-Type:", result["content_type"])
    pass


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "unknown"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }
    except requests.RequestException as error:
        return {"status": None, "error": type(error).__name__}
    pass


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []
    for url in SITES:
        results.append((url, check_site(url)))

    successful = [item for item in results if item[1]["status"] == 200]
    successful.sort(key=lambda item: item[1]["length"], reverse=True)

    for url, result in successful:
        print(f"{url} -> 200, {result['length']} octeți")
    print(f"Reușite: {len(successful)} | Eșuate: {len(results) - len(successful)}")
    pass


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response = requests.get(url, timeout=5)
        headers = {name.lower() for name in response.headers}
        present = []
        missing = []
        for name in SECURITY_HEADERS:
            if name.lower() in headers:
                present.append(name)
            else:
                missing.append(name)
        return {
            "present": present,
            "missing": missing,
            "score": len(present) * 100 // len(SECURITY_HEADERS),
        }
    except requests.RequestException as error:
        return {"status": None, "error": type(error).__name__}
    pass


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    result = {"status": None, "attempts": 0}
    last_error = None
    for number in range(1, attempts + 1):
        result["attempts"] = number
        try:
            response = requests.get(url, timeout=5)
            result["status"] = response.status_code
            if response.status_code < 500:
                return result
        except requests.RequestException as error:
            last_error = type(error).__name__
    if result["status"] is None and last_error is not None:
        result["error"] = last_error
    return result
    pass
