from urllib.parse import urlsplit

from checker import (
    SITES,
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check,
)


def main():
    # Partea 1: apeluri pentru build_url și is_https
    site = urlsplit(SITES[1])
    print("build_url, fără /:", build_url(site.netloc, site.path.lstrip("/")))
    print("build_url, cu /:", build_url(site.netloc, site.path))
    print("is_https, HTTPS:", is_https(SITES[0]))
    print("is_https, HTTP:", is_https(SITES[9]))

    # Partea 2: apeluri pentru show_response
    for url in (SITES[0], SITES[6], SITES[9]):
        print("show_response:", url)
        show_response(url)

    # Partea 3: apeluri pentru check_site
    for url in SITES:
        print("check_site:", url, "->", check_site(url))

    # Partea 4: apelul scan_sites()
    scan_sites()

    # Partea 5: apeluri pentru check_headers
    for url in (SITES[0], SITES[10], SITES[11], SITES[9]):
        print("check_headers:", url, "->", check_headers(url))

    # Partea 6: apeluri pentru retry_check
    for url in (SITES[3], SITES[6], SITES[7], SITES[9], SITES[12]):
        print("retry_check:", url, "->", retry_check(url))
    print("retry_check, attempts=2:", SITES[7], "->", retry_check(SITES[7], attempts=2))


if __name__ == "__main__":
    main()
