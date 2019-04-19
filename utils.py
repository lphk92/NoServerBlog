import datetime


def url_to_filename(url_str):
    filename = url_str.replace(" ", "").split("/")[-1]
    filename = "./posts/%s.json" % filename
    return filename


def filename_to_url(filename):
    url_str = filename.strip().split("/")[-1].split(".")[0]
    return url_str


def title_to_filename(title):
    special_chars = "!@#$%^&*()_+-=/\\}{[]'\";:<>.,"
    filename = ''.join([c for c in title if c not in special_chars])
    filename = "./posts/%s.json" % filename.replace(" ", "_").lower()
    return filename


def title_to_url(title):
    return filename_to_url(title_to_filename(title))


def today():
    return datetime.datetime.now().date().strftime("%Y-%m-%d")
