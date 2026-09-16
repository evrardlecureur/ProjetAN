## Summary

<!-- What does this pull request change, and why? Link the related issue, for example "Closes #12". -->

## Type of change

- [ ] Bug fix
- [ ] New analysis, figure or section of the report
- [ ] Documentation
- [ ] CI, dependencies or tooling

## Checklist

- [ ] `ruff check .` passes
- [ ] `python main.py` (from `code/`) still runs and the figures of `figures/` are updated if the results changed
- [ ] `tectonic -X compile Rapport.tex` builds the report
- [ ] `npx markdownlint-cli2` and `lychee --offline --include-fragments .` pass (if Markdown files changed)
- [ ] `CHANGELOG.md` is updated under "Unreleased"
