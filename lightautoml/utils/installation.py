"""Tools for partial installation."""

import os


try:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import distribution
except ModuleNotFoundError:
    from importlib_metadata import PackageNotFoundError, distribution

import logging


logger = logging.getLogger(__name__)


def __validate_extra_deps(extra_section: str, error: bool = False) -> None:
    """Check if extra dependencies is installed.

    Args:
        extra_section: Name of extra dependencies
        error: How to process error

    """
    ignore_deps = os.environ.get("DOCUMENTATION_ENV", False)

    md = distribution("lightautoml").metadata
    extra_pattern = 'extra == "{}"'.format(extra_section)
    reqs_info = []
    for k, v in md.items():
        if k == "Requires-Dist" and extra_pattern in v:
            req = v.split(";")[0].split()[0]
            reqs_info.append(req)

    for req_info in reqs_info:
        lib_name: str = req_info.split()[0]
        try:
            distribution(lib_name)
        except PackageNotFoundError as e:
            # Print warning
            logger.warning(
                "'%s' extra dependency package '%s' isn't installed. "
                "Look at README.md in repo 'LightAutoML' for installation instructions.",
                extra_section,
                lib_name,
            )

            if not ignore_deps:
                if error:
                    raise e
