__author__ = 'chris'
import os
import sys
from django.core.management.base import BaseCommand, CommandError
from ...backend.utils import add_djangui_script


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--group',
            dest='group',
            default='Djangui Scripts',
            help='The name of the group to create scripts under. Default: Djangui Scripts')
        parser.add_argument('script', type=str, help='A script or folder of scripts to add to Djangui.')

    def handle(self, *args, **options):
        script = options['script']
        if not script:
            raise CommandError('You must provide a script path or directory containing scripts.')
        if not os.path.exists(script):
            raise CommandError('{0} does not exist.'.format(script))
        group = options['group'] if options['group'] else 'Djangui Scripts'
        scripts = [os.path.join(script, i) for i in os.listdir(script)] if os.path.isdir(script) else [script]
        converted = 0
        for script in scripts:
            if script.endswith('.pyc') or '__init__' in script:
                continue
            if script.endswith('.py'):
                sys.stdout.write('Converting {}\n'.format(script))
                add_djangui_script(script=os.path.abspath(script), group=group)
                converted += 1
        sys.stdout.write('Converted {} scripts\n'.format(converted))