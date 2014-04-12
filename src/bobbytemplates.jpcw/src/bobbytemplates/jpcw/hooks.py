#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Render bobbytemplates.jpcw hooks.
"""

__docformat__ = 'restructuredtext en'


import getpass
import os
from mrbobby.bobbyexceptions import ValidationError
from datetime import date


def basicnamespace_pre_pkg_ns(configurator, question):
    """Guess default pkg_ns from Output Directory"""
    names = configurator.target_directory.split(os.sep)[-1].split('.')
    if len(names) == 2:
        question.default = names[0]


def basicnamespace_pre_pkg_project(configurator, question):
    """Guess default pkg_project from Output Directory"""
    names = configurator.target_directory.split(os.sep)[-1].split('.')
    if len(names) == 2:
        question.default = names[1]


def basicnamespace_pre_dcvs_nick(configurator, question):
    """Guess default pkg_project from Output Directory"""
    question.default = getpass.getuser()


def valid_pkg_license(configurator, question, answer):
    """Check license answer."""
    licenses = ['BSD', 'GPL']
    if answer.upper().strip() not in licenses:
        raise ValidationError("'{0}' is not in {1}".format(answer, licenses))
    return answer


def basic_namespace_pre_render(configurator):
    """License stuff."""
    configurator.variables.update({'year': date.today().year})
    if configurator.variables['pkg_license'].lower() == 'gpl':
        configurator.variables.update({'gpl': 'y'})
    else:
        configurator.variables.update({'gpl': 'n'})


def basic_namespace_post_render(configurator):
    """Nothing yet."""


# vim:set et sts=4 ts=4 tw=80: