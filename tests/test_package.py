# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Unit tests for the message schema."""

import pytest
from jsonschema import ValidationError

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


def test_minimal(dummy_data):
    """
    Assert the message schema validates a message with the required fields.
    """
    message = PackageStateChange(body=dummy_data)
    message.validate()
    assert message.url == "https://koschei.fedoraproject.org/package/rust-tokio?collection=f37"
    assert message.groups == ["rust-sig"]
    assert message.packages == ["rust-tokio"]


def test_full(dummy_data):
    """
    Assert the message schema validates a message with the required fields.
    """
    dummy_data["repo"] = dummy_data["collection"]
    message = PackageStateChange(body=dummy_data)
    message.validate()


def test_missing_fields(dummy_data):
    """Assert an exception is actually raised on validation failure."""
    del dummy_data["collection"]
    message = PackageStateChange(body=dummy_data)
    with pytest.raises(ValidationError):
        message.validate()


def test_str(dummy_data):
    """Assert __str__ produces a human-readable message."""
    expected_str = "rust-tokio's builds are back to normal in f37"
    message = PackageStateChange(body=dummy_data)
    message.validate()
    assert expected_str == str(message)


@pytest.mark.parametrize(
    "new,old,expected",
    [
        ("ok", "ignored", "rust-tokio added to Koschei in f37"),
        ("failing", "ok", "rust-tokio's builds started to fail in f37"),
        ("ok", "failing", "rust-tokio's builds are back to normal in f37"),
        ("ignored", "failing", "rust-tokio became retired or ignored in f37"),
        ("unresolved", "ok", "rust-tokio's dependencies failed to resolve in f37"),
    ],
)
def test_summary(dummy_data, new, old, expected):
    """Assert the summary is correct."""
    dummy_data["new"] = new
    dummy_data["old"] = old
    message = PackageStateChange(body=dummy_data)
    assert message.summary == expected


def test_koji_instance(dummy_data):
    """Assert the koji instance is taken into account."""
    dummy_data["koji_instance"] = "staging"
    expected_str = "rust-tokio's builds are back to normal in f37 (staging)"
    message = PackageStateChange(body=dummy_data)
    message.validate()
    assert expected_str == message.summary
