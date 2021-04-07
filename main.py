import app.dados.processarPullRequests as processarRepo
import app.extract_data.process_pull_requests as processarPullRequests
import os

def main(repo_first, repo_limit, pr_first, token):
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    processarRepo.iniciar(repo_first, repo_limit, token)
    processarPullRequests.iniciar(repo_limit, pr_first, token)

if __name__ == "__main__":
    main()