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
