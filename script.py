import git
import urllib.request
from bs4 import BeautifulSoup
import urllib.request
import csv

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

def extractTimeStamps(gitlog):
    timestamps = list()
    searchQuery = "Date:   "
    for log in gitlog:
        if searchQuery in log:
            beginningIndex = log.index(searchQuery) + len(searchQuery)
            timestamps.append(log[beginningIndex:])
            
    return timestamps

def constructURL(author, project_name, commit):
    url = "http://github.com/" + author + "/" + project_name + "/commit/" + commit
    return url
            
def run(path):
    path_to_repo = path
    g = git.Repo(path_to_repo)
    gitlog = g.git.log(p=True).split("\n")
    
    
    author = extractAuthor(gitlog)
    project_name = extractProjectName(path_to_repo)
    commits = extractCommitHashCodes(gitlog)
    time_stamps = extractTimeStamps(gitlog)
    
    urls = list()
    for commit in commits:
        urls.append(constructURL(author,project_name,commit))
    
    commit_messages = list()
    for url in urls:
        html_doc = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        commit_messages.append(soup.title.text)
    
    table = zip(time_stamps,commits,commit_messages,urls)
    filename = project_name + ".csv"
    with open(filename, 'w') as output_file:
        output_writer = csv.writer(output_file,delimiter=",",quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(['Time','Hashcode','Commit Title','URL'])
        for row in table:
            output_writer.writerow(row)
        
if __name__ == '__main__':
    input_file_path = sys.argv[1]
    repo_list = input_file_path.readlines()
    for repo in repo_list:
        run(repo)
#     run("C:/Users/Vinay_2/Documents/Mondego/ByteCodeAnalyzer")     