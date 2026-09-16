# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- Repository reorganized: figures in `figures/` (was `photos_rapoort/`), subject, report, slides and talk script in `docs/`
- Report source fixed so that it compiles: graphics path, unbalanced brace on the title page, a duplicate of the whole body pasted after `\end{document}` removed, author name corrected
- Python sources linted with Ruff (unused import, f-strings without placeholder, import order)
- README rewritten in English: the model, the solvers, the scenarios, getting started, repository structure and quality checks

### Added

- CI: Ruff, the simulations run end to end with the empirical orders in the summary and the figures as artifact, report built with Tectonic, markdownlint and lychee and CodeQL (Python and workflows)
- Dependabot for the Python dependencies and the GitHub Actions
- MIT License, contributing guide, code of conduct, security policy, citation metadata, issue forms and pull request template
- Pinned dependencies in `requirements.txt` and `requirements-dev.txt`

## [1.0.0] - 2026-05-04

Version presented at the defence.

### Added

- Model of a trophic cascade with five populations (vegetation, elk and moose, deer, wolves, bears): five coupled nonlinear ODEs with Monod carrying capacities, Holling predation terms, a logarithmic numerical response of the wolves and seasonal hunting
- Four solvers with the same interface: explicit Euler, implicit Euler and Crank-Nicolson (Newton-Raphson with a finite-difference Jacobian), classical RK4
- Reference simulation over 50 years and comparison of the solvers, Yellowstone scenario (wolves reintroduced after 20 years), phase portraits, convergence study with the empirical orders
- Report, slides and talk script (French)

[Unreleased]: https://github.com/evrardlecureur/ProjetAN/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/evrardlecureur/ProjetAN/releases/tag/v1.0.0
