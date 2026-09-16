# Contributing

Thank you for your interest in this project. It is a student project of the
numerical analysis course at Polytech Nice Sophia (MAM3), written by four
students, and corrections, additional scenarios and pull requests are welcome.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to contribute

- **Report a bug** or **suggest an improvement** with the
  [issue forms](https://github.com/evrardlecureur/ProjetAN/issues/new/choose).
- **Report a security vulnerability** privately, as described in the
  [security policy](SECURITY.md). Please do not open a public issue for it.
- **Open a pull request** for a fix, an additional analysis, a figure or documentation.

For a larger change, for example a new section of the report, please open an
issue first so that we can agree on the approach.

## Development setup

Requires Python 3.12 and [Tectonic](https://tectonic-typesetting.github.io/) to build the report.

```bash
git clone https://github.com/evrardlecureur/ProjetAN.git
cd ProjetAN
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

ruff check .                       # lint
cd code && python main.py          # about 30 s, writes the five figures next to the scripts
tectonic -X compile Rapport.tex    # from the repository root, builds Rapport.pdf
```

To check the Markdown files like the CI does:

```bash
npx markdownlint-cli2
lychee --offline --include-fragments .
```

## Coding guidelines

The repository provides an [`.editorconfig`](.editorconfig) file: most editors
apply its indentation and whitespace settings automatically.

- The code must pass `ruff check`, configured in [`pyproject.toml`](pyproject.toml).
  The parameters are imported with `from params import *` on purpose, so that
  the equations of `model.py` read like the report.
- Keep the split of the modules: `params.py` (table of the subject), `model.py`
  (the five equations), `solvers.py` (one function per method, same signature),
  `main.py` (scenarios and figures).
- A new figure is saved by `main.py` and its committed copy goes to `figures/`
  with the name used by `Rapport.tex`.
- Pin new dependencies to an exact version in `requirements.txt` (or
  `requirements-dev.txt` for development tools) so that Dependabot can track them.
- The code comments, the report and the slides are in French, the repository documentation in English.

## Pull request process

1. Create a branch from `main` with a descriptive name, for example
   `fix/figure-labels` or `docs/results-table`.
2. Keep commits focused, with a short summary in the imperative mood
   (for example "Add the residual plot of dataset C").
3. Open a pull request against `main`, fill in the template and add a label
   (`bug`, `enhancement`, `documentation`...): labels sort the release notes.
4. The CI must pass (`python`, `pipeline`, `report`, `docs`) and another member of the team
   reviews the pull request before it is merged. The branch is not protected
   by GitHub (a setting reserved to the owner of the repository), so this is a
   team rule rather than an enforced one.
5. Update the README when the usage or the results change, and `CHANGELOG.md`
   under "Unreleased".

## Versioning and releases

The project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (`2.0.0`): incompatible change, for example a different layout of the repository;
- **MINOR** (`1.1.0`): new scenario, solver or figure;
- **PATCH** (`1.0.1`): backward-compatible bug fix or correction of the report.

Releases are published from `main` with a `vX.Y.Z` tag. GitHub generates their
notes from the merged pull requests, grouped by label as configured in
[`.github/release.yml`](.github/release.yml), and the `version` field of
[`CITATION.cff`](CITATION.cff) is updated at the same time.
