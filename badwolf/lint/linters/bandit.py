# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import io
import csv
import logging

from badwolf.lint import Problem
from badwolf.lint.linters import Linter
from badwolf.lint.utils import in_path, run_command


logger = logging.getLogger(__name__)


class BanditLinter(Linter):
    name = 'bandit'
    default_pattern = '*.py'

    def is_usable(self):
        return in_path('bandit')

    def lint_files(self, files):
        command = ['bandit', '-f', 'csv']
        command += files
        _, output = run_command(command, cwd=self.working_dir)
        if not output:
            raise StopIteration()

        reader = csv.DictReader(io.BytesIO(output))
        for row in reader:
            msg = '[{}] {}'.format(row['test_name'], row['issue_text'])
            yield Problem(
                row['filename'],
                int(row['line_number']),
                msg,
                self.name
            )
