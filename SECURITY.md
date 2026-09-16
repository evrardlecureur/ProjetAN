# Security Policy

## Supported Versions

Only the `main` branch is maintained.

| Component | Path | Supported |
| --- | --- | --- |
| Model, solvers and simulations | `code/` | Yes |
| Report, subject, slides and talk script | `Rapport.tex, docs/` | Yes |
| GitHub Actions workflows and Dependabot configuration | `.github/` | Yes |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please do not disclose it publicly through a GitHub issue.

Report it privately by email to [romainben31@gmail.com](mailto:romainben31@gmail.com), or through GitHub's private vulnerability reporting if the owner of the repository has enabled it: [report a vulnerability](https://github.com/evrardlecureur/ProjetAN/security/advisories/new).

When reporting a vulnerability, please provide:

* A short description of the vulnerability
* The affected file or component
* The steps required to reproduce the issue
* Any relevant screenshots, logs, or code examples

## Scope

This policy applies to the source code and configuration contained in this repository, in particular:

* the Python code, which only depends on NumPy and Matplotlib and reads no external data;
* the LaTeX report and its figures;
* the GitHub Actions workflows and the Dependabot configuration.

As this is an educational project, security issues should be reported responsibly so they can be reviewed and addressed without unnecessarily exposing other users or contributors.

## Security Measures

* **CodeQL** code scanning (advanced setup, `.github/workflows/codeql.yml`) for every pull request, every push to `main` and once a week.
* **Dependabot** version updates for the GitHub Actions and the Python dependencies pinned in `requirements*.txt`, grouped by patch and minor updates.
* **Least privilege**: the workflows only get read access to the repository, plus the write access to security events that CodeQL needs to upload its results.

The settings that only the owner of the repository can change (branch protection, dependency graph and dependency review, Dependabot security updates, secret scanning, private vulnerability reporting) are not part of this policy.

## Response

Security reports will be reviewed as soon as reasonably possible.

Depending on the nature and severity of the issue, appropriate corrective actions may include:

* Fixing the vulnerability
* Updating dependencies
* Improving the code or configuration
* Documenting the issue and its resolution
