import logging
import os
import subprocess
import tempfile
from collections.abc import Generator
from pathlib import Path

import httpx
from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler

load_dotenv()

logger = logging.getLogger(__name__)
console = Console()


def repo_has_commits(path: Path) -> bool:
    """Check if the git repository at the given path has any commits."""
    result = subprocess.run(
        ["git", "-C", str(path), "rev-list", "--all", "--count"],
        stdout=subprocess.PIPE,
        text=True,
    )
    return int(result.stdout.strip()) > 0


def retrieve_all_repos(
    organization: str, token: str | None = None
) -> Generator[dict, None, None]:
    """Retrieve all repositories for a given organization."""
    base_url = f"https://api.github.com/orgs/{organization}/repos?per_page=100"
    logger.info(f"Fetching repositories for organization: {organization}")
    logger.info(f"Using token: {'Yes' if token else 'No'}")

    headers = (
        {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"}
        if token
        else {}
    )
    page = 1
    repos = []
    while True:
        url = base_url + f"&page={page}"
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        repos = response.json()
        if not repos:
            break
        yield from repos
        page += 1


def backup_repo(repo_url: str, bundle_location: Path) -> None:
    """Clone the repo to a temporary location and create a bundle in the given
    location."""

    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.run(
            ["git", "clone", "--mirror", repo_url, temp_dir],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        repo_name = repo_url.split("/")[-1].replace(".git", "")

        if not repo_has_commits(Path(temp_dir)):
            logger.warning(f"Repository {repo_url} is empty. Skipping bundle creation.")
            return

        bundle_path = bundle_location / f"{repo_name}.bundle"
        bundle_path = bundle_path.resolve()  # absolute path needed inside temp dir
        subprocess.run(
            ["git", "bundle", "create", str(bundle_path), "--all"],
            cwd=temp_dir,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        logger.info(f"Created bundle for {repo_name} at {bundle_path}")


def main():
    """Main function to back up all repositories of the organization."""
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console)],
    )
    token = os.getenv("GITHUB_TOKEN") or None
    organization = os.getenv("ORGANIZATION") or "UMCU-Digital-Health"

    with console.status("Retrieving repositories...") as status:
        repos = retrieve_all_repos(organization, token)
        bundle_dir = Path("bundles")
        bundle_dir.mkdir(exist_ok=True)

        for i, repo in enumerate(repos):
            repo_name = repo["name"]
            status.update(f"Processing repository {i}: {repo_name}")
            logger.info(f"Cloning and creating bundle for repository: {repo_name}")
            backup_repo(
                f"https://{token}@github.com/{organization}/{repo_name}.git", bundle_dir
            )

    console.print(
        "[bold green]All repositories have been backed up successfully![/bold green]"
    )


if __name__ == "__main__":
    main()
