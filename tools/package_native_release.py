"""Package explicitly built JNI/C libraries with source provenance and checksums for Maven downloads."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", required=True, choices=["windows-x86_64", "linux-x86_64"])
    parser.add_argument("--jni", type=Path, required=True)
    parser.add_argument("--ffi", type=Path, required=True)
    parser.add_argument("--validation", required=True, help="Describe native execution or cross-compilation checks")
    args = parser.parse_args()
    version = tomllib.loads((ROOT / "python/pyproject.toml").read_text())["project"]["version"]
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if subprocess.check_output(["git", "diff", "HEAD", "--name-only"], cwd=ROOT, text=True).strip():
        parser.error("Commit source changes before packaging a release")
    windows = args.platform.startswith("windows")
    expected = ["matsim_pt_router.dll", "multimodal_router.dll"] if windows else ["libmatsim_pt_router.so", "libmultimodal_router.so"]
    files = {}
    for path, name in zip([args.jni, args.ffi], expected):
        data = path.read_bytes()
        if path.name != name or not data.startswith(b"MZ" if windows else b"\x7fELF"):
            parser.error(f"Incorrect native binary for {args.platform}: {path}")
        files["native/" + name] = data
    files["LICENSE"] = (ROOT / "LICENSE").read_bytes()
    files["build-info.json"] = json.dumps(dict(version=version, revision=revision,
        platform=args.platform, validation=args.validation, numeric_jni_protocol=1,
        coordinate_policy_protocol=1), indent=2).encode()
    files["SHA256SUMS.txt"] = "".join(f"{hashlib.sha256(v).hexdigest()}  {k}\n" for k,v in files.items()).encode()
    name = f"mmrouter-native-{version}-{args.platform}"
    output = ROOT / "target/distributions"
    output.mkdir(parents=True, exist_ok=True)
    archive = output / (name + ".zip")
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
        for file, data in files.items():
            zipped.writestr(name + "/" + file, data)
    archive.with_suffix(".zip.sha256").write_text(f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n")
    print(archive)


if __name__ == "__main__":
    main()
