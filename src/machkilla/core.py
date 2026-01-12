"""Core runtime pieces for Machkilla.

This module defines the engine and step primitives that other parts of the
project can build upon.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Iterable, List, Optional, Protocol


class Step(Protocol):
    """A single executable unit of work in the engine."""

    name: str

    def __call__(self) -> "StepResult":
        ...


@dataclass(frozen=True)
class StepResult:
    """Outcome of a step execution."""

    name: str
    started_at: datetime
    finished_at: datetime
    status: str
    details: Optional[str] = None


@dataclass
class Engine:
    """Coordinates and executes steps in order."""

    steps: List[Step] = field(default_factory=list)

    def register(self, step: Step) -> None:
        """Register a step for execution."""

        self.steps.append(step)

    def register_all(self, steps: Iterable[Step]) -> None:
        """Register multiple steps for execution."""

        self.steps.extend(steps)

    def run(self) -> List[StepResult]:
        """Run all registered steps sequentially."""

        results: List[StepResult] = []
        for step in self.steps:
            started_at = datetime.utcnow()
            result = step()
            finished_at = datetime.utcnow()
            results.append(
                StepResult(
                    name=result.name,
                    started_at=started_at,
                    finished_at=finished_at,
                    status=result.status,
                    details=result.details,
                )
            )
        return results


@dataclass(frozen=True)
class SimpleStep:
    """Convenience wrapper for simple callables."""

    name: str
    action: Callable[[], str]
    details: Optional[str] = None

    def __call__(self) -> StepResult:
        started_at = datetime.utcnow()
        status = self.action()
        finished_at = datetime.utcnow()
        return StepResult(
            name=self.name,
            started_at=started_at,
            finished_at=finished_at,
            status=status,
            details=self.details,
        )
