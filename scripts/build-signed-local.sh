#!/usr/bin/env bash
# Build and sign Mikajy-Free.apk on this machine with the owner's local keystore backup (release-key-backup/, gitignored).
# Reads the alias and password from PASSWORD.txt into the environment only; nothing secret is printed or written anywhere else.
# Needs the Android SDK (default ~/Android/Sdk). The published release is still built and signed by GitHub Actions (release.yml);
# this is for local builds and for checking that the backup key matches the certificate GitHub pins.
set -euo pipefail
cd "$(dirname "$0")/.."
K=release-key-backup
[[ -f $K/mikajy-release.jks && -f $K/PASSWORD.txt ]] || { echo "Missing $K/mikajy-release.jks or PASSWORD.txt" >&2; exit 1; }
export MIKAJY_KEYSTORE="$PWD/$K/mikajy-release.jks"
export MIKAJY_ALIAS="$(sed -n 's/^Alias:[[:space:]]*//p' "$K/PASSWORD.txt" | head -1)"
pw="$(sed -n 's/^Store\/key password:[[:space:]]*//p' "$K/PASSWORD.txt" | head -1)"
export MIKAJY_STOREPASS="$pw" MIKAJY_KEYPASS="$pw"; unset pw
: "${MIKAJY_ALIAS:?alias not found in PASSWORD.txt}"
export ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT:-$HOME/Android/Sdk}"
bash build_apk.sh
TOOLS="$(find "$ANDROID_SDK_ROOT/build-tools" -mindepth 1 -maxdepth 1 -type d | sort -V | tail -1)"
echo "Signing certificate SHA-256: $("$TOOLS/apksigner" verify --print-certs Mikajy-Free.apk | sed -n 's/^Signer #1 certificate SHA-256 digest: //p')"
echo "Package: $("$TOOLS/aapt" dump badging Mikajy-Free.apk | sed -n "s/^package: name='\([^']*\)' versionCode='\([^']*\)' versionName='\([^']*\)'.*/\1 \3 (code \2)/p")"
