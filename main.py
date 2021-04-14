import app.dados.processarRepo as processarRepo
import app.dados.processarPullRequests as processarPullRequests
import os


def main(repo_first, repo_limit, pr_first):
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    processarRepo.iniciar(repo_first, repo_limit)
    processarPullRequests.iniciar(repo_limit, pr_first)


if __name__ == "__main__":
    main(100, 100, 100)
