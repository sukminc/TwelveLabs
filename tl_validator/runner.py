# tl_validator/runner.py
import os
import sys
import pathlib
import subprocess
import datetime as _dt
try:
    # Optional; only used in GUI mode
    import tkinter as _tk  # type: ignore
    from tkinter import filedialog as _fd  # type: ignore
    from tkinter import messagebox as _mb  # type: ignore
except Exception:  # pragma: no cover
    _tk = None
    _fd = None
    _mb = None

from tl_validator.core import extract_simple_failures, extract_progress_and_summary


def _discover_paths(arg: str | None, selected_files: list[str], selected_folder: str | None) -> list[pathlib.Path]:
    paths: list[pathlib.Path] = []
    if selected_folder:
        folder = pathlib.Path(selected_folder).expanduser().resolve()
        if folder.exists() and folder.is_dir():
            paths = sorted(p for p in folder.glob("*.json") if p.is_file())
    else:
        for f in selected_files:
            p = pathlib.Path(f).expanduser().resolve()
            if p.is_file() and p.suffix.lower() == ".json":
                paths.append(p)
    if not paths and arg:
        p = pathlib.Path(arg).expanduser().resolve()
        if p.is_dir():
            paths = sorted(x for x in p.glob("*.json") if x.is_file())
        elif p.is_file() and p.suffix.lower() == ".json":
            paths = [p]
    return paths


def _write_report(
    out_dir: pathlib.Path,
    cases_path: pathlib.Path,
    start: _dt.datetime,
    end: _dt.datetime,
    progress: str,
    summary: str,
    failures: list[str],
    proc: subprocess.CompletedProcess[str],
) -> pathlib.Path:
    ts = start.strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"{ts}_{cases_path.name}.txt"
    include_full = os.getenv("TL_INCLUDE_FULL_OUTPUT") == "1"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"Selected cases file: {cases_path}\n")
        f.write(f"Start:   {start.isoformat()}\n")
        f.write(f"End:     {end.isoformat()}\n")
        f.write(f"Elapsed: {str(end - start)}\n\n")
        f.write("=== SUMMARY ===\n")
        if progress:
            f.write(progress + "\n")
        if summary:
            f.write(summary + "\n")
        f.write("\n=== SIMPLE FAILURES ===\n")
        if failures:
            for msg in failures:
                f.write(f"- {msg}\n")
        else:
            f.write("None\n")
        f.write("\n")
        if include_full:
            f.write("=== PYTEST STDOUT ===\n")
            f.write(proc.stdout)
            f.write("\n=== PYTEST STDERR ===\n")
            f.write(proc.stderr)
        else:
            f.write("=== FULL OUTPUT OMITTED ===\n")
            f.write("Set TL_INCLUDE_FULL_OUTPUT=1 to include full pytest stdout/stderr.\n")
    return out_path


def main() -> None:
    # GUI selection (multi-file then folder), fallback to CLI arg
    selected_files: list[str] = []
    selected_folder: str | None = None

    if _tk and _fd:
        try:
            _root = _tk.Tk()
            _root.withdraw()

            # Ask the user which mode they want: Folder (Yes) or Files (No)
            choose_folder = _mb.askyesno(
                title="Select Mode",
                message=(
                    "Do you want to select a FOLDER containing JSON test cases?\n\n"
                    "Yes = Select a folder\nNo  = Select one or more JSON files"
                ),
                icon=_mb.QUESTION,
                parent=_root,
            )

            if choose_folder:
                selected_folder = _fd.askdirectory(
                    title="Select a folder containing JSON case files",
                    parent=_root,
                ) or None
            else:
                selected_files = list(
                    _fd.askopenfilenames(
                        title="Select one or more JSON case files",
                        filetypes=[
                            ("JSON files", "*.json"),
                            ("All files", "*.*"),
                        ],
                        parent=_root,
                    )
                )

            _root.destroy()
        except Exception:
            pass

    paths = _discover_paths(
        sys.argv[1] if len(sys.argv) > 1 else None,
        selected_files,
        selected_folder,
    )
    if not paths:
        print("No JSON files found. Provide a file or folder:\n"
              "  python -m tl_validator.runner /path/to/cases.json\n"
              "  python -m tl_validator.runner /path/to/folder_with_json")
        sys.exit(1)

    out_dir = pathlib.Path("validation_results")
    out_dir.mkdir(parents=True, exist_ok=True)

    reports: list[pathlib.Path] = []
    for cases_path in paths:
        os.environ["TL_CASES_FILE"] = str(cases_path)
        start = _dt.datetime.now()
        proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "--tb=short"], capture_output=True, text=True)
        all_out = (proc.stdout or "") + "\n" + (proc.stderr or "")
        failures = extract_simple_failures(all_out)
        progress, summary = extract_progress_and_summary(proc.stdout or "")
        end = _dt.datetime.now()

        # Echo compact lines to terminal
        if progress:
            print(progress)
        if summary:
            print(summary)

        out_path = _write_report(out_dir, cases_path, start, end, progress, summary, failures, proc)
        print(f"Saved results to {out_path}")
        reports.append(out_path)

    print("\nGenerated reports:")
    for rp in reports:
        print(f"- {rp}")


if __name__ == "__main__":
    main()
