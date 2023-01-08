#MADE BY AyanCh0w

import requests
from bs4 import BeautifulSoup
import openai

openai.api_key = ""
QUERY = "What is taylors new album?"
WORDCOUNT = 100
response = requests.get(f'https://www.google.com/search?q={QUERY.replace(" ", "+")}&safe=active&ssui=on')
soup = BeautifulSoup(response.text, 'html.parser')
urlResults = []

BLACKLIST = [
    "google",
    "youtube",
]
def checkBlacklist(item, blacklist=BLACKLIST):
    for i in range(len(blacklist)):
        if BLACKLIST[i] not in item:
            pass
        else:
            return False
    return True

print("Loading: [++--------]")

# Extract all URLS from page
results = soup.find_all("a")
for result in results:
    if "https://" in result.get("href"):
        if "/url?q=" in result.get("href"):
            if (checkBlacklist(result.get("href"))):
                if "%" in result.get("href"):
                    urlResults.append(result.get("href").split("/url?q=",1)[1].split("&",1)[0].split("%",1)[0])
                else:
                    urlResults.append(result.get("href").split("/url?q=",1)[1].split("&",1)[0])
print("Loading: [++++------]")
context = []
for result in urlResults:
    response = requests.get(result)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    context.append(text.split()[:WORDCOUNT])
print("Loading: [++++++----]")
strContext = ""
for i in range(len(urlResults)):
    strContext += " ".join(context[i])+"\n\n"

prompt = "context:\n" + strContext + "\n" + QUERY
print("Loading: [++++++++--]")
response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print("Loading: [++++++++++]\n\n")
print(response["choices"][0]["text"])
