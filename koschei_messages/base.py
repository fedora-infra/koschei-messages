# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-2.0-or-later

from fedora_messaging import message

SCHEMA_URL = "http://fedoraproject.org/message-schema/"
# TODO: update Koschei to include a link to the thing so we can
# differentiate between staging and prod
BASE_URL = "https://koschei.fedoraproject.org"


class KoscheiMessage(message.Message):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by Koschei.
    """

    @property
    def app_name(self):
        return "Koschei"

    @property
    def app_icon(self):
        return "https://apps.fedoraproject.org/img/icons/koschei.png"
