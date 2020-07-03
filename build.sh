#!/usr/bin/env bash
set -e

python rel.py
cd /tmp/gentoo/var/db/repos/localrepo/net-im/telegram-desktop
ebuild --force telegram-desktop-2.1.11.ebuild manifest
emerge telegram-desktop
