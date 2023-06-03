# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Unit tests for the message schema."""

import pytest
from jsonschema import ValidationError

from koschei_messages.collection import CollectionStateChange


@pytest.fixture
def dummy_data():
    return {
        "repo_id": "f37",
        "collection": "f37",
        "collection_name": "Fedora 37",
        "new": "ok",
        "old": "failing",
        "koji_instance": "primary",
    }


def test_minimal(dummy_data):
    """
    Assert the message schema validates a message with the required fields.
    """
    message = CollectionStateChange(body=dummy_data)
    message.validate()
    assert message.url == "https://koschei.fedoraproject.org/collection/f37"


def test_missing_fields(dummy_data):
    """Assert an exception is actually raised on validation failure."""
    del dummy_data["collection"]
    message = CollectionStateChange(body=dummy_data)
    with pytest.raises(ValidationError):
        message.validate()


def test_str(dummy_data):
    """Assert __str__ produces a human-readable message."""
    expected_str = "Fedora 37 buildroot was fixed"
    message = CollectionStateChange(body=dummy_data)
    message.validate()
    assert expected_str == str(message)


@pytest.mark.parametrize(
    "new,old,expected",
    [
        ("ok", "unknown", "Fedora 37 added to Koschei"),
        ("ok", "unresolved", "Fedora 37 buildroot was fixed"),
        ("unresolved", "ok", "Fedora 37 buildroot was broken"),
    ],
)
def test_summary(dummy_data, new, old, expected):
    """Assert the summary is correct."""
    dummy_data["new"] = new
    dummy_data["old"] = old
    message = CollectionStateChange(body=dummy_data)
    assert message.summary == expected


def test_koji_instance(dummy_data):
    """Assert the koji instance is taken into account."""
    dummy_data["koji_instance"] = "staging"
    expected_str = "Fedora 37 buildroot was fixed (staging)"
    message = CollectionStateChange(body=dummy_data)
    message.validate()
    assert expected_str == message.summary
