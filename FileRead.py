import re

regex_methode = r"^(.*?) "  # to know the methde GET or post
regex_url = r" (.*?) "  # to get the part of url
regex_headers = r"\n([^\s]*)([^\n]+)*$"  # to get lines from seconde line to th end
regex_post_data = r"\n\n([^\s]*)([^\n]+)*$" # to get post data
def fromFile(file):
    Headers = dict()

    data = open(file, "rb").read().decode()

    matches_methode = re.search(regex_methode, data)
    matches_url = re.search(regex_url, data)
    matches_headers = re.finditer(regex_headers, data, re.MULTILINE | re.IGNORECASE)
    matches_post_data = re.finditer(regex_post_data, data, re.MULTILINE | re.IGNORECASE)


    try:
        for ff in matches_headers:
            f = (ff.group().replace("\n", "").split(":", 1))

            Headers.update({f[0]: f[1].replace(" ", "")})
    except IndexError:
        pass


    def params(payload):
        try:
            payload1 = dict()
            for xx in payload.split('?',1)[1].replace("/", "").split("&"):
                payload1.update({xx.split("=")[0]: xx.split("=")[1]})

            return payload1
        except IndexError:
            return "NO_parametrs"



    if matches_methode.group(1) == "GET":
        # print("cool its get then ? ")
        url = "https://" + Headers["Host"] + matches_url.group(1)
        parmaeeter = params(matches_url.group(1))

        return url,Headers,parmaeeter
    elif matches_methode.group(1) == "POST":
        url = "https://" + Headers["Host"] + matches_url.group(1)
        parmaeeter = params(matches_url.group(1))
        for xx in matches_post_data:
            if xx.group(1):
                Data_post = xx.group(1)
        #if "json" not in Headers["Content-Type"] and "{" not in Data_post:
        return url,Headers,parmaeeter,Data_post

print(fromFile("Get1.txt"))
print("\n\n")
print(fromFile("post1.txt"))