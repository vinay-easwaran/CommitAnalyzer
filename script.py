import git
import urllib.request
from bs4 import BeautifulSoup
import urllib.request
import csv
  
def extractCommitHashCodes(gitlog: list):
    commits = list()
    for log in gitlog:
        if log[0:7] == 'commit ':
            commits.append(log[7:])
            
    return commits

def extractTimeStamps(gitlog):
    timestamps = list()
    searchQuery = "Date:   "
    for log in gitlog:
        if searchQuery in log:
            beginningIndex = log.index(searchQuery) + len(searchQuery)
            timestamps.append(log[beginningIndex:])
            
    return timestamps

def extractProjectName(path):
    x = path.find('/')
    while(x != -1):
        path = path[x+1:]
        x = path.find('/')
    return path

def constructURL(base_url, commit):
    url = base_url + "/commit/" + commit
    return url
            
def run(path):
    path_to_repo = path
    g = git.Repo(path_to_repo)
    gitlog = g.git.log(p=True).split("\n")
    remote_origin = g.git.remote(v=True)
    base_url = remote_origin.split("\t")[1].split(" ")[0][:-4]
    
    commits = extractCommitHashCodes(gitlog)
    time_stamps = extractTimeStamps(gitlog)
    project_name = extractProjectName(base_url)
    print("ON PROJECT " + project_name)
    
    urls = list()
    for commit in commits:
        urls.append(constructURL(base_url,commit))
    
    commit_messages = list()
    for url in urls:
        print(url)
        html_doc = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        commit_messages.append(soup.title.text)
    
    table = zip(time_stamps,commits,commit_messages,urls)
    filename = "output/" + project_name + ".csv"
    with open(filename, 'w') as output_file:
        output_writer = csv.writer(output_file,delimiter=",",quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(['Time','Hashcode','Commit Title','URL'])
        for row in table:
            output_writer.writerow(row)
        
if __name__ == '__main__':
    input_file_path = input("Enter link to project paths: ")
    f = open(input_file_path,"r")
    repo_list = f.readlines()
    f.close()
    for repo in repo_list:
        repo = repo.strip("\n")
        run(repo)