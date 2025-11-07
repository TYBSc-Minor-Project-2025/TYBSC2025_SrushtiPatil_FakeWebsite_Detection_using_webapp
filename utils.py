# utils.py
import re
import socket
import requests
from urllib.parse import urlparse
from datetime import datetime
import whois

def get_features_from_url(url):
    features = {}
    parsed = urlparse(url)

    # Basic URL features
    features["url_length"] = len(url)
    features["hostname_length"] = len(parsed.netloc)
    features["path_length"] = len(parsed.path)
    features["num_dots"] = parsed.netloc.count(".")
    features["num_hyphens"] = parsed.netloc.count("-")
    features["num_at"] = url.count("@")
    features["num_question"] = url.count("?")
    features["num_equal"] = url.count("=")
    features["num_digits"] = sum(c.isdigit() for c in url)
    features["has_https"] = 1 if parsed.scheme == "https" else 0
    features["contains_ip"] = 1 if re.match(r"^\d+\.\d+\.\d+\.\d+$", parsed.netloc) else 0
    features["contains_login"] = 1 if "login" in url.lower() else 0
    features["contains_verify"] = 1 if "verify" in url.lower() else 0
    features["contains_update"] = 1 if "update" in url.lower() else 0
    features["contains_paypal"] = 1 if "paypal" in url.lower() else 0
    features["contains_bank"] = 1 if "bank" in url.lower() else 0
    features["contains_secure"] = 1 if "secure" in url.lower() else 0

    # Suspicious symbols
    features["has_double_slash"] = 1 if "//" in parsed.path else 0
    features["has_percent"] = 1 if "%" in url else 0
    features["has_redirect"] = 1 if "//" in url[7:] else 0

    # WHOIS / Domain features
    try:
        domain_info = whois.whois(parsed.netloc)
        if isinstance(domain_info.creation_date, list):
            creation_date = domain_info.creation_date[0]
        else:
            creation_date = domain_info.creation_date
        if creation_date:
            age = (datetime.now() - creation_date).days
            features["domain_age_days"] = age
        else:
            features["domain_age_days"] = 0
    except Exception:
        features["domain_age_days"] = 0

    # Response features
    try:
        response = requests.get(url, timeout=3)
        features["status_code"] = response.status_code
        features["redirect_count"] = len(response.history)
    except:
        features["status_code"] = 0
        features["redirect_count"] = 0

    return features
