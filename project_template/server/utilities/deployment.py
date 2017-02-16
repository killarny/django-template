"""
Wrapper script for executing docker-compose commands within the correct
environment (staging|production).

Takes care of adding the plethora of '-f' options and the
'-p' label for each environment so that you don't need to worry about
accidentally forgetting them.

Also provides a few shortcut commands to simplify administration tasks.

Example:

### production
###  A script in your <repo-root>, perhaps - called simply 'production', with
###  this gist saved as <repo-root>/server/utilities/deployment.py

    $ cat production
    #!/usr/bin/env python3
    import sys

    from server.utilities.deployment import main

    # don't create pyc or __pycache__ files/directories
    sys.dont_write_bytecode = True


    if __name__ == '__main__':
        main('production')

    $ ./production update

    >> docker-compose -f docker-compose.yml -f production.yml -p myproject\
    > build --no-cache backend

    ...

    >> docker-compose -f docker-compose.yml -f production.yml -p myproject\
    > up -d

    ...

"""
import re
from argparse import ArgumentParser, REMAINDER
from os import getcwd
from os.path import split
from subprocess import CalledProcessError, Popen, TimeoutExpired
import unicodedata


class CommandNotImplemented(NotImplementedError):
    def __init__(self):
        super().__init__('Sorry, this command is not implemented yet.')


def run(*popenargs, check=False):
    """
    Partially backported subprocess.run method from Python 3.5 - latest
    version of Debian stable (which many containers run on) uses only
    Python 3.4, so we have to do this.

    Annoying, yes.

    Also, this is extremely simplified compared to the real method. It just
    needs to be Good Enough(tm) to do what we need, and be api compatible
    so the 3.5 method can be used when Debian stable allows for it.
    """
    with Popen(*popenargs) as process:
        try:
            stdout, stderr = process.communicate(None, timeout=None)
        except TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            raise TimeoutExpired(process.args, None, output=stdout,
                                 stderr=stderr)
        except:
            process.kill()
            process.wait()
            raise
        retcode = process.poll()
        if check and retcode:
            raise CalledProcessError(retcode, process.args,
                                     output=stdout, stderr=stderr)


def slugify(value):
    """
    Slightly modified version of Django's slugify method.

    Converts to lowercase, removes non-word characters (alphanumerics,
    underscores, and whitespace). Also strips leading and
    trailing whitespace.
    """
    value = (unicodedata.normalize('NFKD', value)
             .encode('ascii', 'ignore').decode('ascii'))
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '', value)


def __docker_compose(command, args=None, env=None, project=None,
                     dry_run=False):
    if not (env and project):
        # if the user provided no env and no project, then what's the
        # point of calling this method in the first place?
        raise ValueError("No 'env' or 'project' given.")
    compose_opts = [
        'docker-compose',
        '-f', 'docker-compose.yml',
        '-f', '{}.yml'.format(env),
        '-p', project,
        command,
    ] + args  # again, python 3.4 compat going on here
    # show the docker-compose command we're about to execute
    print('\n{highlight} {color}{cmdline}{endcolor}\n'.format(
        highlight='>>',
        color='\x1b[0;32m',
        endcolor='\x1b[0m',
        cmdline=' '.join(compose_opts),
    ))
    if dry_run:
        # only a dry-run, chaps! we don't need to really do anything, but
        # let's show some feedback to avoid confusion..
        print('{highlight} {color}dry run complete{endcolor}\n'.format(
            highlight='--',
            color='\x1b[0;30m',
            endcolor='\x1b[0m',
        ))
        return
    try:
        # delegate our command to docker-compose..
        run(compose_opts, check=True)
    except KeyboardInterrupt:
        # docker-compose has sufficient feedback when an interrupt occurs,
        # so we'll just exit
        exit()
    except CalledProcessError as e:
        # if something bad happened, we'll exit with the same return code
        # from the docker-compose process
        exit(e.returncode)


def docker_compose(opts):
    __docker_compose(opts.command, args=opts.args, dry_run=opts.dry_run,
                     env=opts.environment_name, project=opts.NAME)


def update(opts):
    build_args = ['--no-cache'] if not opts.use_cache else []
    # opts.container is a string if the default value was used, and a list
    # if different container(s) are specified
    if isinstance(opts.container, str):
        build_args.append(opts.container)
    else:
        build_args.extend(opts.container)
    __docker_compose('build', args=build_args, dry_run=opts.dry_run,
                     env=opts.environment_name, project=opts.NAME)
    __docker_compose('up', args=['-d'], dry_run=opts.dry_run,
                     env=opts.environment_name, project=opts.NAME)


def logs(opts):
    args = [
        '-f', '--tail=50',
    ]
    # opts.container is a string if the default value was used, and a list
    # if different container(s) are specified
    if isinstance(opts.container, str):
        args.append(opts.container)
    else:
        args.extend(opts.container)
    __docker_compose('logs', args=args, dry_run=opts.dry_run,
                     env=opts.environment_name, project=opts.NAME)


def main(environment_name):
    if environment_name not in ['staging', 'production']:
        raise ValueError("invalid environment: '{}'".format(environment_name))

    # construct the default project name using a similar pattern
    # as the default behavior of docker-compose
    _, project_name = split(getcwd())
    project_name = slugify(project_name)
    # append the environment name, if it's not 'production'
    if environment_name != 'production':
        project_name = '{prj}-{env}'.format(
            prj=project_name,
            env=environment_name,
        )

    # cmd line parsing
    parser = ArgumentParser(
        description="Deployment assistance utility for the '{}' "
                    "environment.".format(environment_name))
    parser.add_argument('-p', '--project-name', dest='NAME',
                        default=project_name,
                        help="specify an alternate project name "
                             "(default: '%(default)s')")
    parser.add_argument('--dry-run', action='store_true',
                        help="do not execute any actual commands")
    parser.add_argument('--debug', action='store_true',
                        help="debug this script")
    subparsers = parser.add_subparsers()

    # build (or rebuild) a container.. ignores the cache by default
    up = subparsers.add_parser('update',
                               help='re/build and deploy a container')
    up.add_argument('container', default='site', nargs='*',
                    help="container(s) to update (default: '%(default)s)'")
    up.add_argument('-c', '--use-cache', action='store_true',
                    help="use the docker cache when possible for build steps")
    up.set_defaults(func=update, environment_name=environment_name)

    # tail the interesting logs without seeing tons of scrollback -
    # defaults to simply showing the backend
    lg = subparsers.add_parser('logs',
                               help='tail the interesting logs, with some '
                                    'short scrollback')
    lg.add_argument('container', default='site', nargs='*',
                    help="container(s) to update (default: '%(default)s)'")
    lg.set_defaults(func=logs, environment_name=environment_name)

    # more-or-less direct commands to docker-compose
    dc = subparsers.add_parser('compose',
                               help='send a command to docker-compose, with '
                                    'the correct environment options prepended')
    dc.add_argument('command', help='command to send')
    dc.add_argument('args', nargs=REMAINDER, help='command arguments')
    dc.set_defaults(func=docker_compose, environment_name=environment_name)

    opts = parser.parse_args()
    try:
        opts.func(opts)
    except AttributeError:
        if opts.debug:
            raise
        parser.print_usage()
        exit(1)