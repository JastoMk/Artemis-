# Project Runner

This repository uses GitHub-hosted Actions runners. No Android phone, personal computer, self-hosted machine, API key, or paid server is required for these checks.

## Start a run
1. Open the **Actions** tab.
2. Select **Project Runner**.
3. Press **Run workflow**.

A scheduled health check runs every Monday at 04:17 UTC (06:17 South African Standard Time).

## Safety and scope
- Runner permissions are read-only (`contents: read`).
- No secrets are requested or stored.
- The runner performs checks only; it does not deploy, trade, place orders, purchase products, or modify external accounts.
- Reports are retained as downloadable Actions artifacts for 7 days.
- Empty or unconfigured projects are reported as requiring bootstrap; a green runner job does not mean the project itself is complete.

## Architecture
Each project repository owns its own workflow and uses a fresh GitHub-hosted `ubuntu-latest` runner. This keeps projects isolated and avoids cross-repository credentials. The workflows can run while the user's phone is offline.

## ARTEMIS local prototype (Android / Termux)

The repository now includes a standard-library-only Python prototype in `artemis.py`. It stores a small task list locally and does not require internet access after Python is available.

In Termux:

```sh
python --version
python artemis.py doctor
python artemis.py add "Test offline task storage"
python artemis.py list
python artemis.py done 1
python artemis.py status
```

The default data file is `~/.artemis/tasks.json`. To use another local directory, set `ARTEMIS_HOME` before running the script.

This is an offline local task/diagnostics prototype, not yet an AI assistant or Android UI automation tool. It does not read notifications, control apps, send messages, or access contacts. Those capabilities require separate Android permission-bridge research and on-device tests. GitHub Actions tests run on hosted Linux and do not prove compatibility with a Huawei handset.
