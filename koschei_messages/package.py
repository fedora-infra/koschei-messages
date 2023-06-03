# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-2.0-or-later

from .base import BASE_URL, SCHEMA_URL, KoscheiMessage


class PackageStateChange(KoscheiMessage):
    """Messages published by Koschei when a package state changes.

    For example when package starts to fail to build, package
    dependencies become unresolved or when package is fixed.
    """

    topic = "koschei.package.state.change"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new thing is created",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "new": {"type": "string"},
            "old": {"type": "string"},
            "koji_instance": {"type": "string"},
            "collection": {"type": "string"},
            "collection_name": {"type": "string"},
            "repo": {"type": "string"},
            "groups": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": [
            "name",
            "new",
            "old",
            "koji_instance",
            "collection",
            "collection_name",
            "groups",
        ],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return self.summary

    @property
    def summary(self):
        """Return a summary of the message."""
        if self.body["new"] == "ok" and self.body["old"] == "ignored":
            info = "{name} added to Koschei"
        else:
            info = {
                "failing": "{name}'s builds started to fail",
                "ok": "{name}'s builds are back to normal",
                "ignored": "{name} became retired or ignored",
                "unresolved": "{name}'s dependencies failed to resolve",
            }[self.body["new"]]
        info += " in {collection}"
        if self.body["koji_instance"] != "primary":
            info += " ({koji_instance})"
        return info.format(
            name=self.body["name"],
            collection=self.body["collection"],
            koji_instance=self.body["koji_instance"],
        )

    @property
    def url(self):
        return f"{BASE_URL}/package/{self.body['name']}?collection={self.body['collection']}"

    @property
    def groups(self):
        """List of groups affected by the action that generated this message."""
        return self.body["groups"]

    @property
    def packages(self):
        """List of packages affected by the action that generated this message."""
        return [self.body["name"]]
