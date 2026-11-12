from robocop.linter.rules import Rule, RuleSeverity, VisitorChecker
from robocop.linter.utils import misc as utils
from robot.api import Token
from robot.parsing.model.blocks import TestCase
from robot.parsing.model.statements import KeywordCall

PHASES = ("given", "when", "then")
CONTINUATIONS = ("and", "but")


class GherkinStructureRule(Rule):
    """
    Test case does not follow the Given / When / Then structure.

    A test must go through three phases in order: Given, When, Then.
    `And` and `But` continue the phase opened by the previous keyword.

    Correct code:

        *** Test Cases ***
        Test case
            Given An Election
            And Some Candidates
            When Someone Votes
            And Someone Else Votes
            Then Results Are Verified
            And Nothing Else Happened
    """

    name = "gherkin-structure"
    rule_id = "BDD01"
    message = "{error_msg}"
    severity = RuleSeverity.WARNING


class GherkinStructureChecker(VisitorChecker):
    gherkin_structure: GherkinStructureRule

    def visit_TestCase(self, node: TestCase) -> None:  # noqa: N802
        current_phase = -1
        seen_phases: set[str] = set()
        for step in node.body:
            if isinstance(step, KeywordCall):
                current_phase = self._check_step(step, current_phase, seen_phases)
        self._check_missing_phases(node, seen_phases)

    def _check_step(
        self, step: KeywordCall, current_phase: int, seen_phases: set[str]
    ) -> int:
        prefix = _prefix_of(step)
        if prefix in CONTINUATIONS:
            if current_phase < 0:
                self._report_step(step, f"'{prefix.title()}' used before any Given")
            return current_phase
        if prefix not in PHASES:
            self._report_step(
                step, "Step must start with Given, When, Then, And or But"
            )
            return current_phase
        phase = PHASES.index(prefix)
        if prefix in seen_phases:
            self._report_step(
                step, f"Repeated '{prefix.title()}': use And or But to continue it"
            )
        elif phase < current_phase:
            self._report_step(
                step,
                f"'{prefix.title()}' must come before "
                f"'{PHASES[current_phase].title()}'",
            )
        seen_phases.add(prefix)
        return max(phase, current_phase)

    def _check_missing_phases(self, node: TestCase, seen_phases: set[str]) -> None:
        for phase in PHASES:
            if phase not in seen_phases:
                col = utils.token_col(node.header, Token.TESTCASE_NAME)
                self.gherkin_structure.report(
                    error_msg=f"Test case '{node.name}' has no {phase.title()} step",
                    node=node.header,
                    col=col,
                    end_col=col + len(node.name),
                )

    def _report_step(self, step: KeywordCall, error_msg: str) -> None:
        col = utils.token_col(step, Token.KEYWORD)
        self.gherkin_structure.report(
            error_msg=error_msg,
            node=step,
            col=col,
            end_col=col + len(step.keyword or ""),
        )


def _prefix_of(step: KeywordCall) -> str:
    words = (step.keyword or "").split(maxsplit=1)
    return words[0].lower() if words else ""
