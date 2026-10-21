#!/bin/sh
# Builds dist/local_owlmascot.zip for Site administration > Plugins > Install plugins.
# Moodle wants the top folder to be the plugin name without its type prefix: "owlmascot".
set -e
cd "$(dirname "$0")/.."
python3 tools/build.py
cp dist/owl-mascot.js moodle/local_owlmascot/owl-mascot.js
rm -rf dist/.pkg && mkdir -p dist/.pkg && cp -r moodle/local_owlmascot dist/.pkg/owlmascot
(cd dist/.pkg && rm -f ../local_owlmascot.zip && zip -qr ../local_owlmascot.zip owlmascot)
rm -rf dist/.pkg
echo "dist/local_owlmascot.zip"
