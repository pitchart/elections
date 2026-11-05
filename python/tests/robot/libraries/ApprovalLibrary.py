from pathlib import Path
from typing import Any

from approvaltests import Options, verify_as_json
from approvaltests.namer.namer_base import NamerBase

APPROVALS_DIRECTORY = Path(__file__).parent.parent / "approvals"


class RobotTestNamer(NamerBase):
    def __init__(self, test_name: str) -> None:
        super().__init__()
        self._test_name = test_name

    def get_file_name(self) -> str:
        return "elections." + self._test_name.lower().replace(" ", "_")

    def get_directory(self) -> str:
        return str(APPROVALS_DIRECTORY)

    def config_directory(self) -> str:
        return str(APPROVALS_DIRECTORY)


def verify_for_test(results: Any, test_name: str) -> None:
    options = Options().with_namer(RobotTestNamer(test_name))
    verify_as_json(results, options=options)
