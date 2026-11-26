# Frappe PM

Project management for the Frappe framework: projects, tasks, agile sprints and boards, time tracking, resources, budgets, reporting, portal and API.

The full planned scope (382 features, tiered MVP/P2/P3) is tracked in [FEATURES.md](FEATURES.md).

## Install

```bash
bench get-app https://github.com/BishoyGH/Frappe-PM
bench --site your.site install-app frappe_pm
```

## Development

DocTypes are generated from compact specs in `dev/specs/`:

```bash
python dev/dtgen.py            # regenerate DocType JSON (never overwrites controllers)
python dev/validate_doctypes.py
ruff check . && ruff format --check .
bench --site your.site run-tests --app frappe_pm
```

CI (GitHub Actions) runs lint, DocType sync/validation, pure-Python unit tests and a site test matrix on Frappe v15 and v16, in parallel, with pip/yarn/bench caching and cancel-in-progress concurrency.

## License

MIT
