#!/usr/bin/env bash
set -euo pipefail

docker run -it --rm -v "$PWD":/tdesktop amosbird/t1 bash -c "cd out/Release; make -j40; strip -s bin/Telegram"
scp out/Release/bin/Telegram 172.26.178.148:gentoo/usr/local/bin/Telegram
