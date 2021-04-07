
from app.api.getRepo import get_repositories
import app.dados.processarPullRequests as processarPullRequests
import app.csv_manager.state_manager_repo as sm

def repositorioValido(repo):
    merged_count = repo['merged']['totalCount']
    closed_count = repo['closed']['totalCount']
    return merged_count + closed_count >= 100

def repositorioData(repo):
    return {
        "nome": repo['name'],
        "dono": repo['owner']['login'],
        "url": repo['url'],
        "id": repo['id'],
        "pull_requests_merged": repo['merged']['totalCount'],
        "pull_requests_closed": repo['closed']['totalCount']
    }

def iniciar(repo_first, repo_limit):
    initial_page_info, initial_total = sm.load_repo_state()
    total = initial_total
    page_info = initial_page_info

    if total == repo_limit:
        print("{} repositories already processed".format(repo_limit))
        return

    while(repo_limit - total > 0):
        data = get_repositories(repo_first, page_info['endCursor'])     
        repositories = [ repositorioData(r) for r in data['repositories'] if repositorioValido(r)]
        size = 0
        if(len(repositories) + total > repo_limit):
            exceed = len(repositories) + total - repo_limit
            index = len(repositories) - exceed
            repositories = repositories[:index]
        size = len(repositories)
        total += size
        sm.write_repo_file(repositories)
        sm.write_repo_state(page_info['endCursor'], total)
        page_info = data['page_info']