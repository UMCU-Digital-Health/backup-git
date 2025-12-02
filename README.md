# Backup Git

This repo provides a script for backing up all git repos from a specified organization or user.


## Requirements

- Python 3.7+
- Git installed (and configured to access the repositories)

## Installation

```bash
git clone https://github.com/yourusername/backup_git.git
cd backup_git
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
python main.py
```

## License

This project is licensed under the MIT License.