# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-2.0-or-later

from .base import BASE_URL, SCHEMA_URL, KoscheiMessage


class CollectionStateChange(KoscheiMessage):
    """Messages published by Koschei when a collection state changes.

    For example when collection buildroot becomes unresolvable
    (broken) or when it is fixed.
    """

    topic = "koschei.collection.state.change"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new thing is created",
        "type": "object",
        "properties": {
            "repo_id": {"type": "string"},
            "new": {"type": "string"},
            "old": {"type": "string"},
            "koji_instance": {"type": "string"},
            "collection": {"type": "string"},
            "collection_name": {"type": "string"},
        },
        "required": [
            "repo_id",
            "new",
            "old",
            "koji_instance",
            "collection",
            "collection_name",
        ],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return self.summary

    @property
    def summary(self):
        """Return a summary of the message."""
        if self.body["new"] == "ok" and self.body["old"] == "unknown":
            info = "{collection} added to Koschei"
        else:
            info = {
                "ok": "{collection} buildroot was fixed",
                "unresolved": "{collection} buildroot was broken",
            }[self.body["new"]]
        if self.body["koji_instance"] != "primary":
            info += " ({koji_instance})"
        collection = self.body["collection_name"]
        return info.format(collection=collection, koji_instance=self.body["koji_instance"])

    @property
    def url(self):
        return f"{BASE_URL}/collection/{self.body['collection']}"
