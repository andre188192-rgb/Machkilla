"""Entry point for running Machkilla core."""

from __future__ import annotations

from .core import Engine, SimpleStep


def build_engine() -> Engine:
    engine = Engine()
    engine.register(
        SimpleStep(
            name="bootstrap",
            action=lambda: "ok",
            details="Initial bootstrap step placeholder.",
        )
    )
    return engine


def main() -> None:
    engine = build_engine()
    results = engine.run()
    for result in results:
        print(f"{result.name}: {result.status}")


if __name__ == "__main__":
    main()
