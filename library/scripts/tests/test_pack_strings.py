# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.
#
# This source code is licensed under the Apache 2.0 license found in
# the LICENSE file in the root directory of this source tree.

import unittest

import pack_strings
import string_pack_config


class TestPackStringsMethods(unittest.TestCase):
    def setUp(self):
        self.sp_config = string_pack_config.StringPackConfig()
        self.sp_config.assets_directory = "app/src/main/assets/"

    def test_group_string_files_by_languages_without_mapping(self):
        grouped_file_paths = pack_strings.group_string_files_by_languages(
            {},
            [
                "sp/app_src_main_res/values-cs/strings.xml",
                "sp/app_src_main_res/values-sk/strings.xml",
                "sp/coreui_src_main_res/values-cs/strings.xml",
                "sp/coreui_src_main_res/values-sk/strings.xml",
            ],
        )

        self.assertEqual(2, len(grouped_file_paths))
        self.assertSetEqual(
            {
                "sp/app_src_main_res/values-cs/strings.xml",
                "sp/coreui_src_main_res/values-cs/strings.xml",
            },
            set(grouped_file_paths["cs"]),
        )

        self.assertSetEqual(
            {
                "sp/app_src_main_res/values-sk/strings.xml",
                "sp/coreui_src_main_res/values-sk/strings.xml",
            },
            set(grouped_file_paths["sk"]),
        )

    def test_group_string_files_by_languages_with_mapping(self):
        grouped_file_paths = pack_strings.group_string_files_by_languages(
            {"sk": "cs"},
            [
                "sp/app_src_main_res/values-cs/strings.xml",
                "sp/app_src_main_res/values-sk/strings.xml",
                "sp/coreui_src_main_res/values-cs/strings.xml",
                "sp/coreui_src_main_res/values-sk/strings.xml",
            ],
        )

        self.assertEqual(1, len(grouped_file_paths))
        self.assertSetEqual(
            {
                "sp/app_src_main_res/values-cs/strings.xml",
                "sp/app_src_main_res/values-sk/strings.xml",
                "sp/coreui_src_main_res/values-cs/strings.xml",
                "sp/coreui_src_main_res/values-sk/strings.xml",
            },
            set(grouped_file_paths["cs"]),
        )

    def test_group_string_files_by_languages_two_languages_with_mapping(self):
        grouped_file_paths = pack_strings.group_string_files_by_languages(
            {"sk": "cs"},
            [
                "sp/app_src_main_res/values-sk/strings.xml",
                "sp/app_src_main_res/values-zh-rCN/strings.xml",
                "sp/coreui_src_main_res/values-sk/strings.xml",
                "sp/coreui_src_main_res/values-zh-rCN/strings.xml",
            ],
        )

        self.assertEqual(2, len(grouped_file_paths))

        self.assertSetEqual(
            {
                "sp/app_src_main_res/values-sk/strings.xml",
                "sp/coreui_src_main_res/values-sk/strings.xml",
            },
            set(grouped_file_paths["cs"]),
        )

        self.assertSetEqual(
            {
                "sp/app_src_main_res/values-zh-rCN/strings.xml",
                "sp/coreui_src_main_res/values-zh-rCN/strings.xml",
            },
            set(grouped_file_paths["zh-rCN"]),
        )

    def test_get_dest_pack_file_path_with_module(self):
        self.sp_config.module = "module"
        pack_file_pack = pack_strings.get_dest_pack_file_path(self.sp_config, "ca")
        self.assertEqual("app/src/main/assets/module_strings_ca.pack", pack_file_pack)

    def test_get_dest_pack_file_path_without_module(self):
        pack_file_pack = pack_strings.get_dest_pack_file_path(self.sp_config, "ca")
        self.assertEqual("app/src/main/assets/strings_ca.pack", pack_file_pack)
