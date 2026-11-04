#!/data/data/com.termux/files/usr/bin/sh
# Read-only ARTEMIS preflight for a Termux device. Does not install packages,
# download models, change settings, or invoke llama.cpp.
set -u

echo "ARTEMIS / llama.cpp Termux preflight"
echo "===================================="
printf 'Date (device): '; date 2>/dev/null || echo unavailable
printf 'Kernel: '; uname -a 2>/dev/null || echo unavailable
printf 'Architecture: '; uname -m 2>/dev/null || echo unavailable
printf 'Android release: '
if command -v getprop >/dev/null 2>&1; then
  getprop ro.build.version.release 2>/dev/null || echo unavailable
else
  echo "getprop unavailable (not a standard Termux shell?)"
fi
printf 'Device model: '
if command -v getprop >/dev/null 2>&1; then
  getprop ro.product.model 2>/dev/null || echo unavailable
else
  echo unavailable
fi

echo
echo "Memory:"
if [ -r /proc/meminfo ]; then
  grep -E '^(MemTotal|MemAvailable|SwapTotal|SwapFree):' /proc/meminfo
else
  echo "/proc/meminfo unavailable"
fi

echo
echo "Storage:"
df -h "$HOME" 2>/dev/null || echo "df unavailable"

echo
echo "Build tools:"
for tool in git cmake make clang python; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf '%s: %s\n' "$tool" "$(command -v "$tool")"
  else
    printf '%s: MISSING\n' "$tool"
  fi
done

echo
echo "Termux environment:"
case "${PREFIX:-}" in
  /data/data/com.termux*) echo "PREFIX: Termux detected" ;;
  *) echo "PREFIX: not recognised as the standard Termux path (${PREFIX:-unset})" ;;
esac

echo
echo "Interpretation:"
echo "- This is a read-only inventory, not a build or inference test."
echo "- No model was downloaded and no package was installed."
echo "- Confirm free storage, available memory, thermal behaviour and battery"
echo "  before attempting a local build or loading a GGUF model."
echo "- ARTEMIS must record actual build and inference results separately."
