import sys
from os import getenv

from src.pipeline.crates import get_crates_packages
from src.pipeline.pkgx import get_pkgx_packages
from src.pipeline.utils.logger import Logger
from src.pipeline.utils.pg import DB

logger = Logger("main_pipeline")


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("usage: python main.py <package_manager>")

        if getenv("CHAI_DATABASE_URL") is None:
            raise ValueError("CHAI_DATABASE_URL is not set")

        # initialize the db and handoff everywhere
        db = DB()
        package_manager = sys.argv[1]

        # run the pipeline for the specified package manager
        if package_manager == "pkgx":
            get_pkgx_packages(db)
        elif package_manager == "crates":
            get_crates_packages(db)
        else:
            raise ValueError("invalid package manager")
    except Exception:
        logger.exception()
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
