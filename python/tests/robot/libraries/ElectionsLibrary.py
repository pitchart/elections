from ApprovalLibrary import verify_for_test
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn

from elections.elections import Elections

ELECTORS_BY_DISTRICT = {
    "District 1": ["Bob", "Anna", "Jess", "July"],
    "District 2": ["Jerry", "Simon"],
    "District 3": ["Johnny", "Matt", "Carole"],
}

ELECTION_MODES = {
    "without district": False,
    "with districts": True,
}


@library(scope="TEST", auto_keywords=False)
class ElectionsLibrary:
    def __init__(self) -> None:
        self._elections: Elections | None = None

    @keyword('An election "${mode}" with candidates "${candidates}"')
    def an_election_with_candidates(self, mode: str, candidates: str) -> None:
        self._elections = Elections(ELECTORS_BY_DISTRICT, ELECTION_MODES[mode])
        for candidate in candidates.split(","):
            self._elections.add_candidate(candidate.strip())

    @keyword('"${elector}" votes for "${candidate}" in "${district}"')
    def votes_for(self, elector: str, candidate: str, district: str) -> None:
        self._current_elections().vote_for(elector, candidate, district)

    @keyword("Results are verified")
    def results_are_verified(self) -> None:
        test_name = BuiltIn().get_variable_value("${TEST NAME}")
        verify_for_test(self._current_elections().results(), test_name)

    def _current_elections(self) -> Elections:
        if self._elections is None:
            raise AssertionError("No election has been set up")
        return self._elections
