import git
import urllib.request
from bs4 import BeautifulSoup
import urllib.request

def extractAuthor(gitlog):
    searchQuery = "Author: "
    for log in gitlog:
        if searchQuery in log:
            beginningIndex = log.index(searchQuery) + len(searchQuery)
            endIndex = beginningIndex + 1
            while(log[endIndex] != " "):
                endIndex += 1
            return log[beginningIndex:endIndex]
        
def extractProjectName(path):
    x = path.find('/')
    while(x != -1):
        path = path[x+1:]
        x = path.find('/')
    return path
  
def extractCommitHashCodes(gitlog: list):
    commits = list()
    searchQuery = "commit "
    for log in gitlog:
        if searchQuery in log:
            beginningIndex = log.index(searchQuery) + len(searchQuery)
            commits.append(log[beginningIndex:])
            
    return commits

def constructURL(author, project_name, commit):
    url = "http://github.com/" + author + "/" + project_name + "/commit/" + commit
    return url
            
def run():
    path_to_repo = "C:/Users/Vinay_2/Documents/CS 171"
    g = git.Repo(path_to_repo)
    gitlog = g.git.log(p=True).split("\n")
    
    
    author = extractAuthor(gitlog)
    project_name = extractProjectName(path_to_repo)
    commits = extractCommitHashCodes(gitlog)
    
    urls = list()
    for commit in commits:
        urls.append(constructURL(author,project_name,commit))
    
    commit_messages = list()
    for url in urls:
        html_doc = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        commit_messages.append(soup.title.text)
    
    table = zip(commits,commit_messages,urls)
    for row in table:
        print(row)
        
if __name__ == '__main__':
    run()