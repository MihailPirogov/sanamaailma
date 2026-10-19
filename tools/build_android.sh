#!/bin/bash
# Android build of Sanamaailma (ru.pirogovlab.sanamaailma), ported from tatar-wow/tools/build_android.sh.
#   tools/build_android.sh          -> signed release/sanamaailma.apk + .aab (needs release/keys/keystore.properties — Sanamaailma's OWN key)
#   tools/build_android.sh signtest -> signed with the release key + Yandex DEMO ads, named *-signtest-NOT-FOR-UPLOAD.{apk,aab} (only to verify signing)
#   tools/build_android.sh debug    -> release/sanamaailma-debug.apk (debug key, Yandex DEMO ad units; for testing only)
# Nothing is uploaded anywhere.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/build_release.py android
if [ -z "${ANDROID_HOME:-}" ]; then for d in /opt/android-sdk "$HOME/tools/android-sdk"; do [ -d "$d/build-tools" ] && ANDROID_HOME=$d && break; done; fi
if ! command -v javac >/dev/null && [ -z "${JAVA_HOME:-}" ]; then for j in "$HOME"/tools/jdk-17*; do [ -x "$j/bin/javac" ] && export JAVA_HOME=$j PATH=$j/bin:$PATH && break; done; fi
export ANDROID_HOME; echo "sdk.dir=$ANDROID_HOME" > android/local.properties
GRADLE="${GRADLE:-gradle}"; command -v "$GRADLE" >/dev/null || for g in /opt/gradle-8.13/bin/gradle "$HOME/tools/gradle-8.13/bin/gradle"; do [ -x "$g" ] && GRADLE=$g && break; done
BT="$ANDROID_HOME/build-tools/36.0.0"
if [ "${1:-}" = debug ]; then
  (cd android && "$GRADLE" --no-daemon -q assembleDebug)
  cp android/app/build/outputs/apk/debug/app-debug.apk release/sanamaailma-debug.apk
  $BT/aapt2 dump badging release/sanamaailma-debug.apk | grep -E "^package|minSdk|targetSdk|application-label:"
  ls -la release/sanamaailma-debug.apk; exit 0
fi
[ -f release/keys/keystore.properties ] || { echo "no release/keys/keystore.properties: create Sanamaailma's own keystore first (release/ANDROID_CHECKLIST.md)"; exit 1; }
if [ "${1:-}" = signtest ]; then OUT=release/sanamaailma-signtest-NOT-FOR-UPLOAD; GFLAGS="-PadsDemo=true"; else OUT=release/sanamaailma; GFLAGS=""; fi
(cd android && "$GRADLE" --no-daemon -q clean assembleRelease bundleRelease $GFLAGS)
cp android/app/build/outputs/apk/release/app-release.apk $OUT.apk
cp android/app/build/outputs/bundle/release/app-release.aab $OUT.aab
$BT/apksigner verify --verbose --print-certs $OUT.apk | grep -E "^Verifie|Signer #1 certificate SHA-256" && echo "apk signature OK"
jarsigner -verify $OUT.aab | grep -m1 "jar verified"
keytool -printcert -jarfile $OUT.aab | grep -m1 "SHA256:"
$BT/aapt2 dump badging $OUT.apk | grep -E "^package|minSdk|targetSdk|application-label:"
$BT/aapt2 dump permissions $OUT.apk | grep -o "name='[^']*'" | tr '\n' ' '; echo
# ad units: real IDs unless built with -PadsDemo=true (see android/app/src/main/res/values/ads.xml)
if [ -n "$GFLAGS" ]; then echo "ads: DEMO units (signtest, -PadsDemo=true)"; elif grep -q 'R-M-[0-9]' android/app/src/main/res/values/ads.xml; then grep -o 'R-M-[0-9]*-[0-9]*' android/app/src/main/res/values/ads.xml | sort -u | tr '\n' ' '; echo "(real Yandex Mobile Ads units)"; else echo "WARNING: ads.xml still has PLACEHOLDER demo units (demo-*-yandex): test ads only, no revenue"; fi
[ -n "$GFLAGS" ] && echo "signtest: built with -PadsDemo=true — NOT FOR UPLOAD"
ls -la $OUT.apk $OUT.aab
