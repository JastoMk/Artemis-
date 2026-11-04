# llama.cpp on Android / Termux — ARTEMIS feasibility trial

**Status: documented trial plan; not yet tested on the target Huawei handset.**

## Why this candidate

The upstream `llama.cpp` project documents a no-root Android Termux route. That makes it a plausible zero-infrastructure experiment for ARTEMIS. It does **not** establish that this particular phone can compile the project or run a useful model at acceptable speed.

- Upstream: https://github.com/ggml-org/llama.cpp
- Android guide: https://github.com/ggml-org/llama.cpp/blob/master/docs/android.md
- Build guide: https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md

## Phase 0 — inventory only

From the ARTEMIS repository in Termux:

```sh
sh scripts/termux_llama_preflight.sh
```

This script is read-only. It reports architecture, Android release/model where available, memory, free storage and whether common build tools exist. It does not install, download, compile, or modify anything.

Save the output privately for the device test record. Do not commit device identifiers or other personal diagnostics to the public repository.

## Phase 1 — prepare Termux (only after reviewing Phase 0)

The upstream Termux instructions use Git and CMake. Package installation and compilation can consume significant storage, battery and memory. Do not start if the phone is low on free space or already hot.

```sh
pkg update
pkg install git cmake clang make
```

Then obtain the upstream source:

```sh
cd "$HOME"
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release --parallel 2
```

The build command above is a conservative starting point, not a guarantee of success on every Android/Termux release. If CMake fails, retain the complete error output and stop; do not randomly add CPU architecture flags.

## Phase 2 — model test

Only after a successful build, choose a small, permissively licensed GGUF model whose licence and exact file size have been checked. Keep the model in Termux's private home directory, not shared storage, for the first test.

Start with a small context (for example 512 tokens) and a short prompt. Record:
- model name, quantisation, file size and source/licence;
- command and context size;
- whether model loading succeeds;
- time to first token and approximate generation speed, if measurable;
- peak memory / Android low-memory kill;
- phone temperature and battery change over a short controlled run.

Do not infer performance from another phone. Do not use private trading credentials, account data or personal documents as prompts.

## Acceptance gates

| Gate | Pass condition |
|---|---|
| Runtime | Termux and Python/CMake/Clang versions recorded |
| Build | Upstream CLI builds and reports its version |
| Load | A small GGUF loads without process termination |
| Inference | A short prompt completes repeatedly |
| Stability | No thermal shutdown, repeated crashes or severe memory pressure |
| Usability | Latency and battery cost are acceptable for a small offline assistant |

If build or inference fails, ARTEMIS remains a task/diagnostics prototype; do not describe local AI as operational. A successful hosted GitHub Actions run is not a substitute for these on-device gates.

## Safety and scope

This trial does not enable Android UI automation, notifications, contacts, calls, SMS, background services, or trading. It does not connect ARTEMIS to Golden Shield or any exchange. Keep those integrations separate until they have independent permissions, tests and explicit user approval.
