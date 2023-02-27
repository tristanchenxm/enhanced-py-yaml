# -*- coding: utf-8 -*-
import yaml
import re
import os
from yaml.loader import Loader

class YamlReader(object):
    def __init__(self, config_file_location='application.yaml', config=None):
        if config:
            if isinstance(config, dict):
                self.config = config
            elif isinstance(config, str):
                self.config = yaml.load(config, Loader)
        else:
            with open(config_file_location, 'r') as f:
                self.config = yaml.load(f, Loader)
        if self.config is None:
            self.config = {}
        self._resolve_placeholders()

    def _resolve_placeholders(self) -> None:
        flat_dict = {}
        self._flatten_dict(self.config, flat_dict)
        for k, v in flat_dict.items():
            self._resolve_placeholders_0(flat_dict, k, v)

    def _resolve_placeholders_0(self, flat_dict: dict, k:str, v: str) -> str:
        if not isinstance(v, str):
            return v
        placeholders = re.findall('\\${([^}]+)}', v)
        for placeholder in placeholders:
            placeholder_value = os.environ.get(placeholder)
            if placeholder_value:
                v = v.replace('${' + placeholder + '}', placeholder_value)
            else:
                placeholder_value = flat_dict.get(placeholder)
                if not placeholder_value:
                    raise ValueError(placeholder + " is not configured")
                v = v.replace('${' + placeholder + '}', str(self._resolve_placeholders_0(flat_dict, placeholder, placeholder_value)))
        flat_dict[k] = v
        self._replace_application_config(k, v)
        return v

    def _flatten_dict(self, src: dict, target: dict, parent_key: str = None):
        def _concat(s1: str, s2: str):
            if s1:
                return s1 + '.' + s2
            else:
                return s2

        for k, v in src.items():
            new_key = _concat(parent_key, k)
            if isinstance(v, dict):
                for sub_key, sub_value in v.items():
                    self._flatten_object(sub_value, target, _concat(new_key, sub_key))
            elif isinstance(v, list) \
                or isinstance(v, tuple) \
                 or isinstance(v, set):
                self._flatten_object(v, target, new_key)
            else:
                target[new_key] = v

    def _flatten_object(self, src, target: dict, parent_key: str = None):
        if isinstance(src, dict):
            self._flatten_dict(src, target, parent_key)
        elif isinstance(src, list) \
                or isinstance(src, tuple) \
                 or isinstance(src, set):
            for i, o in enumerate(src):
                self._flatten_object(o, target, parent_key + '[' + str(i) + ']')
        else:
            target[parent_key] = src


    def _replace_application_config(self, k, v):
        target_dict = self.config
        original_keys = k.split(".")
        depth = len(original_keys)
        for i, original_key in enumerate(original_keys):
            match = re.search('(.*)(\\[\\d+\\])+$', original_key)
            if match:
                for j, group in enumerate(match.groups()):
                    if j == 0:
                        target_dict = target_dict[group]
                    else:
                        if i == depth - 1:
                            target_dict[int(group[1:-1])] = v
                        else:
                            target_dict = target_dict[int(group[1:-1])]
            else:
                if i == depth - 1:
                    target_dict[original_key] = v
                else:
                    target_dict = target_dict[original_key]




    def get_config(self):
        return self.config