import os
from pathlib import Path
from string import Template

import yaml

from cvingest.models import MasterCV

dir = Path(os.path.dirname(os.path.abspath(__file__))) 


def build_prompt_from_template(
    template_name: str, description: str, master: MasterCV, output_schema: str
) -> str:
    template = Template((dir / f"prompts/{template_name}.txt").read_text())

    desc_path = (dir / f"descriptions/{description}")
    with open(desc_path, "r") as f:
        desc = f.read()
    
    assert master.personal == None

    prompt = template.substitute(
        job_description=desc,
        cv=yaml.dump(master.model_dump()),
        output_schema=output_schema,
    )

    return prompt
