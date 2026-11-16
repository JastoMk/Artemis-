# Project Runner

The ARTEMIS Project Runner performs **repository validation on a GitHub-hosted Ubuntu Linux machine**. It is not a continuously running service monitor and it is not a Huawei/Android device test.

## Start a run

1. Open the **Actions** tab.
2. Select **Project Runner**.
3. Press **Run workflow**.

The workflow also runs on pull requests and pushes to `main`, plus a weekly scheduled repository-validation run on Monday at 04:17 UTC (06:17 South African Standard Time).

## What the hosted runner checks

- Checks out the selected repository revision on a fresh `ubuntu-latest` runner.
- Runs `sh -n` against the optional Termux preflight script. This checks shell syntax on Ubuntu; it does **not** execute the script in Termux.
- Runs the local ARTEMIS Python unit tests on hosted Linux.
- Writes a run-scoped Markdown artifact and an always-run Actions summary, including the commit and validation scope.
- Uses Node 24-compatible JavaScript action majors (`checkout@v7`, `setup-python@v7`, `upload-artifact@v7`) to avoid legacy Node 20 runtime warnings.

## What a successful run does not prove

A green hosted run means only that the configured repository checks completed on that Linux runner. It does not prove:

- that Termux is installed or usable on the Huawei handset;
- that the preflight script has been executed on the target phone;
- that llama.cpp compiles for the handset's exact Android/ABI/toolchain combination;
- that a GGUF model loads or inference completes;
- that memory, thermal behaviour, battery use or latency are acceptable;
- that ARTEMIS has Android UI automation, notification access, background services or AI-assistant functionality.

Those are separate device acceptance gates in [the llama.cpp Termux trial](docs/LLAMA_CPP_TERMUX_TRIAL.md). Do not report them as passed until they are actually performed on the target handset.

## Safety and scope

- Runner permissions are read-only (`contents: read`).
- No secrets are requested or stored.
- The runner does not deploy, trade, place orders, purchase products or modify external accounts.
- Reports are retained as downloadable Actions artifacts for 7 days.
- Empty or unconfigured projects are reported as requiring bootstrap; a green runner job does not mean the project itself is complete.

## Architecture

Each project repository owns its workflow and uses a fresh GitHub-hosted `ubuntu-latest` runner. This keeps projects isolated and avoids cross-repository credentials. The workflow can run while the user's phone is offline.

## ARTEMIS local prototype (Android / Termux)

The repository includes a standard-library-only Python prototype in `artemis.py`. It stores a small task list locally and does not require internet access after Python is available.

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

This is an offline local task/diagnostics prototype, not yet an AI assistant or Android UI automation tool. It does not read notifications, control apps, send messages or access contacts. Those capabilities require separate Android permission-bridge research and on-device tests.
