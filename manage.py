#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management.commands.runserver import Command as Runserver

def main():
    # Monkeypatch django_tasks to avoid the TypeError in Python 3.11+
    try:
        import django_tasks.backends.immediate
        def dummy_enqueue(self, task, args, kwargs):
            return None
        django_tasks.backends.immediate.ImmediateBackend.enqueue = dummy_enqueue
    except ImportError:
        pass
    except Exception:
        pass

    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lawfirm_cms.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    Runserver.default_port = "9000"
    main()
