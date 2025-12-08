# Backup GitHub

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![GitHub License](https://img.shields.io/github/license/UMCU-Digital-Health/backup-git)

This repo provides a script for backing up all git repos from a specified organization or user.


## Requirements

- Python 3.7+
- Git installed (and configured to access the repositories)

## Installation

```bash
git clone git@github.com:UMCU-Digital-Health/backup-git.git
cd backup-git
uv sync
```

## Usage

Create a `.env` file in the project root with the following content:

```env
GITHUB_TOKEN=your_github_token_here
ORGANIZATION=your_organization_or_username_here
```
Without this token, the script will only be able to access public repositories.

Run the script:

```bash
uv run main.py
```

To schedule this script to run periodically, you can use cron jobs as follows:
```bash
crontab -e
```

Add the following line to run the script daily at 3 AM:
```bash
0 3 * * * path/to/uv run /path/to/your/script/main.py >> /path/to/your/logfile.log 2>&1
```


## License

This project is licensed under the MIT License.