import argparse
import json
import os
import subprocess
from pathlib import Path

import dotenv
import yaml

from cvingest.build_prompt import build_prompt_from_template
from cvingest.latex import construct_latex_source
from cvingest.model_api import send_prompt
from cvingest.models import TailoredCV
from cvingest.parse_master import (
    mask_personal,
    parse_output,
    read_master,
    unmask_personal,
)

CWD = Path.cwd()
env = CWD / ".env"
latex_build_dir = CWD / "latex_build"
temp_dir = CWD / "temp"

latex_build_dir.mkdir(exist_ok=True)
temp_dir.mkdir(exist_ok=True)

parser = argparse.ArgumentParser(prog="cv-ingest")

parser.add_argument("--master-cv", required=True)
parser.add_argument("--job-desc", required=True)
parser.add_argument("--prompt-template", default="tailor_cv")
parser.add_argument("--model", default="gemini-3.5-flash-lite")
parser.add_argument("--compile-only", action="store_true")
parser.add_argument("--build-to", default=latex_build_dir)
parser.add_argument("--env-file", default=env)
parser.add_argument("--mask-map", required=False)


def main(args):

    dotenv.load_dotenv(args.env_file)

    file = args.master_cv
    if not args.compile_only:
        print(f"Reading {file}")
        raw = read_master(file)

        if hasattr(args, "mask_map"):
            with open(args.mask_map, "r") as f:
                maskmap = json.load(f)
        else:
            maskmap = {}

        print("Masking personal information")
        masked, mask, personal = mask_personal(raw, maskmap)

        output_schema = yaml.safe_dump(
            TailoredCV.model_json_schema(),
            sort_keys=False,
        )
        description = args.job_desc

        print("Building prompt")
        prompt = build_prompt_from_template(
            args.prompt_template, description, masked, output_schema
        )

        with open(temp_dir / "sent_prompt.txt", "w") as f:
            wrote = f.write(prompt)
            print(f"Wrote {wrote}")

        print("sending prompt")
        output = send_prompt(prompt, args.model)

        with open(temp_dir / "model_output.txt", "w") as f:
            f.write(output)

        print("parsing model output")
        tailored_cv = parse_output(output)

        print("unmasking personal information")
        unmasked_tailored = unmask_personal(tailored_cv, mask, personal)

        print("Constructing latex source")
        latex = construct_latex_source(unmasked_tailored)

        with open(CWD / "main.tex", "w") as f:
            f.write(latex)

        print("Latex file in 'main.tex'")

    build_dir = Path(args.build_to)
    build_dir.mkdir(exist_ok=True)

    subprocess.run(
        [
            "pdflatex",
            "-interaction=nonstopmode",
            "-output-directory",
            str(build_dir),
            CWD / "main.tex",
        ],
        check=True,
        cwd=CWD
    )


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
