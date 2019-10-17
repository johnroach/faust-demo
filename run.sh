#!/bin/bash
set -x

export SIMPLE_SETTINGS=faustdemo.settings

poetry run faustdemo worker -l info --web-port=8088