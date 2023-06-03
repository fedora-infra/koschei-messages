# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Unit tests for common properties of the message schemas."""

import pytest

from koschei_messages.package import PackageStateChange


@pytest.fixture
def dummy_data():
    return {
        "name": "rust-tokio",
        "new": "ok",
        "old": "failing",
        "collection": "f37",
        "collection_name": "Fedora 37",
        "groups": ["rust-sig"],
        "koji_instance": "primary",
    }


def test_properties(dummy_data):
    """Assert some properties are correct."""
    message = PackageStateChange(body=dummy_data)

    assert message.app_name == "Koschei"
    assert message.app_icon == "https://apps.fedoraproject.org/img/icons/koschei.png"
