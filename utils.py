def url_to_filename(url_str):
    filename = url_str.replace(" ", "").split("/")[-1]
    filename = "./posts/%s.json" % filename
    return filename

def filename_to_url(filename):
    url_str = filename.strip().split("/")[-1].split(".")[0]
    return url_str

def title_to_filename(title):
    special_chars = "!@#$%^&*()_+-=/\\}{[]'\";:<>.,"
    filename = ''.join([c for c in title if not c in special_chars])
    filename = "./posts/%s.json" % filename.replace(" ", "-").lower()
    return filename
    
def title_to_url(title):
    return filename_to_url(title_to_filename(title))