from datetime import datetime
from app.getRepo.query_pull_request import get_pull_requests
import app.csv.csvPull as sm
import pandas as pd


def pullRquestValido(pull_request):
    reviews = pull_request['reviews']['totalCount']
    createdAt = datetime.strptime(
        pull_request['createdAt'], "%Y-%m-%dT%H:%M:%SZ")
    closedAt = datetime.strptime(
        pull_request['closedAt'], "%Y-%m-%dT%H:%M:%SZ")
    diff = closedAt - createdAt
    hours = diff.total_seconds() / 3600
    return reviews > 0 and hours >= 1


def importarPullRequest(repo, repo_index, pr_first, page_info, total, max_prs):
    sucess = True
    while page_info['hasNextPage']:
        try:
            data = get_pull_requests(
                repo['nome'], repo['dono'], pr_first, page_info['endCursor'])
            new_prs = data['pull_requests']
            size = len(new_prs)
            total += size
            page_info = data['page_info']
            sm.write_pull_file(repo['nome'], [pullRquestData(
                x, repo) for x in new_prs if pullRquestValido(x)])
            sm.write_pull_state(
                page_info['endCursor'], page_info['hasNextPage'], repo_index, total)
        except (Exception) as e:
            print(e)
            success = False
            break
    return sucess


def pullRquestData(pr, repo):
    return {
        "repo": repo['url'],
        "fechado_em": pr['closedAt'],
        "estado": pr['state'],
        "reviews": pr['reviews']['totalCount'],
        "comentarios": pr['comments']['totalCount'],
        "participantes": pr['participants']['totalCount'],
        "tamanho": pr['additions'] + pr['deletions'],
        "descricao": len(pr['body']),
        "criado_em": pr['createdAt'],
        "id": pr['id']
    }


def iniciar(repo_limit, pr_first):
    df = pd.read_csv('tmp/repos/repositories.csv')
    page_info, total, repo_index = sm.load_pull_state()
    for index in range(repo_index, repo_limit):
        repo = df.iloc[index].to_dict()
        max_prs = repo['pull_requests_closed'] + repo['pull_requests_merged']
        sucess = importarPullRequest(
            repo, repo_index, pr_first, page_info, total, max_prs)
        if not sucess:
            break
        page_info['endCursor'] = ""
        page_info['hasNextPage'] = True
        sm.write_pull_state(
            page_info['endCursor'], page_info['hasNextPage'], repo_index + 1, 0)
