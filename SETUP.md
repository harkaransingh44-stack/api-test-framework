# Setup: api-test-framework

Repo to create (empty, no README): https://github.com/harkaransingh44-stack/api-test-framework

This folder is a complete git repo with history. You only need to add the GitHub remote and push. Do not run `git init` again.

## 1. Confirm it runs locally

```bash
cd api-test-framework
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
ruff check . && ruff format --check .
pytest -m "not ui"
```

The API suite needs network access to `https://restful-booker.herokuapp.com`. Open `reports/report.html` to see the HTML report.

Optional — UI tests:

```bash
playwright install chromium
pytest -m ui
# or the full suite:
pytest
```

If you skip `playwright install`, `pytest` still passes; the UI tests are skipped with a reason.

## 2. Create the GitHub repo and push

If the GitHub repo does **not** exist yet:

1. Open https://github.com/new
2. Repository name: `api-test-framework`
3. Leave it **empty** — do not add a README, .gitignore, or license (this folder already has them)
4. Create the repository

Then, from this folder:

```bash
git remote -v
# If origin is missing or points somewhere else:
git remote add origin https://github.com/harkaransingh44-stack/api-test-framework.git
# or, if origin already exists:
# git remote set-url origin https://github.com/harkaransingh44-stack/api-test-framework.git

git branch -M main
git push -u origin main
```

If Git asks for a password, GitHub will not accept your account password. Use one of these:

- `brew install gh && gh auth login`, then push again, or
- a Personal Access Token: GitHub > Settings > Developer settings > Fine-grained tokens, with *Contents: read & write* on this repo only. Paste the token when Git asks for a password.

After the push, open the **Actions** tab. The `tests` workflow has two jobs (API and UI). When both are green, the badge on the README turns green too.

### If this GitHub repo already exists

You started an earlier scaffold in this repo. After unzipping this copy:

```bash
cd api-test-framework
git remote set-url origin https://github.com/harkaransingh44-stack/api-test-framework.git
git fetch origin
git log --oneline --decorate -15
```

If `origin/main` is an ancestor of your local `main` (the usual case), just push:

```bash
git push origin main
```

If GitHub has commits you do not have (for example you added a README in the website UI), rebase first:

```bash
git pull --rebase origin main
# If it conflicts, keep this scaffold's files, then:
# git add . && git rebase --continue
git push origin main
```

Do not force-push unless you are sure nothing on GitHub needs to be kept.

## 3. After it is live

For job forms that ask for GitHub, use:

`https://github.com/harkaransingh44-stack/api-test-framework`

You can also pin the repo on your GitHub profile.

## What to say about this in interviews

Keep this factual and tied to what is in the repo. This is a public portfolio project against teaching APIs, not a description of work done for an employer.

- **Why a thin client?** `BookingClient` returns the raw HTTP response. Assertions live in the tests, so a failure points at the check, not at hidden logic in the wrapper.
- **How tests stay isolated.** Write tests use a fixture that creates a booking and deletes it afterwards, so they do not depend on leftover data on a shared public host.
- **Data-driven cases.** Valid and edge-case payloads live in JSON. Adding a case does not require a new test function.
- **Schema checks.** Responses are validated with JSON Schema (types, required keys, date format), not only field-by-field equality.
- **Known quirks of the API.** Be ready to explain that Restful Booker is a teaching API: `DELETE` returns 201, bad credentials return 200 with a reason string, missing required fields return 500, and invalid dates or a negative price are accepted. The edge-case tests record the actual behaviour and are a good place to talk about what a production API should do instead.
- **UI suite.** The Playwright tests use Sauce Demo's `data-test` attributes and a small page-object layer (login, inventory, cart, checkout). They are marked `ui` and skipped when Chromium is not installed, so CI can split API and UI jobs.
- **CI.** GitHub Actions runs lint and API tests in one job and Playwright in another, and uploads HTML/JUnit reports as artifacts.
- **What not to say.** Do not describe this repo as production code from Amazon or any other employer. Do not claim tools that are not in the repo. Do not say you "trained models" here — there is no model training in this project.
