import re
import math
from collections import Counter
from urllib.parse import urlparse
import tldextract
TRUSTED_GLOBAL_DOMAINS = {
    "google.com",
    "whatsapp.com",
    "facebook.com",
    "yahoo.com",
}
TRUSTED_RESTRICTED_SUFFIXES = (".ac.id")
def is_safelisted_domain(url):
    check_url = url if url.startswith(("http://", "https://")) else "http://" + url
    hostname = (urlparse(check_url).hostname or "").lower()
    if hostname.endswith(TRUSTED_RESTRICTED_SUFFIXES):
        return True
    extracted = tldextract.extract(hostname)
    registered_domain = f"{extracted.domain}.{extracted.suffix}".lower()
    return registered_domain in TRUSTED_GLOBAL_DOMAINS
def get_entropy(text):
    if not text:
        return 0.0
    counter = Counter(text)
    length = len(text)
    entropy = 0.0
    for count in counter.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    return round(entropy, 4)
def count_special_chars(text):
    return len(re.findall(r'[^A-Za-z0-9]', text))
def has_repeated_digits(text):
    return 1 if re.search(r'(\d)\1+', text) else 0
def extract_features(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""
    fragment = parsed.fragment or ""
    extracted = tldextract.extract(hostname)
    subdomains = []
    subdomain_str = ""
    if extracted.subdomain:
        subdomains = extracted.subdomain.split(".")
        subdomain_str = extracted.subdomain
    if len(subdomains) > 0:
        avg_sub_len = sum(len(x) for x in subdomains) / len(subdomains)
        avg_sub_dots = subdomain_str.count(".") / len(subdomains)
        avg_sub_hyphens = subdomain_str.count("-") / len(subdomains)
    else:
        avg_sub_len = 0
        avg_sub_dots = 0
        avg_sub_hyphens = 0
    features = {
        'url_length': len(url),
        'count_dot_url': url.count('.'),
        'having_repeated_digits_url':
            has_repeated_digits(url),
        'count_digit_url':
            sum(c.isdigit() for c in url),
        'count_special_char_url':
            count_special_chars(url),
        'count_hyphen_url':
            url.count('-'),
        'count_underline_url':
            url.count('_'),
        'count_slash_url':
            url.count('/'),
        'count_question_url':
            url.count('?'),
        'count_equal_url':
            url.count('='),
        'count_at_url':
            url.count('@'),
        'count_dollar_url':
            url.count('$'),
        'count_exclamation_url':
            url.count('!'),
        'count_hashtag_url':
            url.count('#'),
        'count_percent_url':
            url.count('%'),
        'domain_length':
            len(hostname),
        'count_dot_domain':
            hostname.count('.'),
        'count_hyphen_domain':
            hostname.count('-'),
        'having_special_char_domain':
            1 if count_special_chars(hostname) > 0 else 0,
        'count_special_char_domain':
            count_special_chars(hostname),
        'having_digit_domain':
            1 if any(c.isdigit() for c in hostname) else 0,
        'count_digit_domain':
            sum(c.isdigit() for c in hostname),
        'having_repeated_digits_domain':
            has_repeated_digits(hostname),
                    'count_subdomain':
            len(subdomains),
        'having_dot_subdomain':
            1 if '.' in subdomain_str else 0,
        'having_hyphen_subdomain':
            1 if '-' in subdomain_str else 0,
        'avg_subdomain_length':
            round(float(avg_sub_len), 4),
        'avg_dot_subdomain':
            round(float(avg_sub_dots), 4),
        'avg_hyphen_subdomain':
            round(float(avg_sub_hyphens), 4),
        'having_special_char_subdomain':
            1 if count_special_chars(subdomain_str) > 0 else 0,
        'count_special_char_subdomain':
            count_special_chars(subdomain_str),
        'having_digit_subdomain':
            1 if any(c.isdigit() for c in subdomain_str) else 0,
        'count_digit_subdomain':
            sum(c.isdigit() for c in subdomain_str),
        'having_repeated_digits_subdomain':
            has_repeated_digits(subdomain_str),
        'having_path':
            1 if len(path) > 1 else 0,
        'path_length':
            len(path),
        'having_query':
            1 if len(query) > 0 else 0,
        'having_fragment':
            1 if len(fragment) > 0 else 0,
        'having_anchor':
            1 if "#" in url else 0,
        'entropy_url':
            get_entropy(url),
        'entropy_domain':
            get_entropy(hostname)
    }
    return features