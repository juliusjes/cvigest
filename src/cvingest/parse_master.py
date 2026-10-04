import pydantic
import yaml

from cvingest.models import MasterCV, Personal, TailoredCV


def read_master(filename) -> MasterCV | None:
    try:
        with open(filename, "r") as f:
            raw = yaml.safe_load(f)
    except OSError as e:
        print(f"ERROR: {e!s}")
        return
    except yaml.YAMLError as e:
        print(f"ERROR: {e!s}")
        return

    return MasterCV.model_validate(raw)


def mask_personal(master: MasterCV, maskmap:dict) -> tuple[MasterCV, dict, Personal]:
    masked = {}

    personal = master.personal
    master.personal = None

    for edu in master.education:
        if edu.school in maskmap:
            masked[maskmap[edu.school]] = edu.school
            edu.school = maskmap[edu.school]

    for exp in master.experience:
        if exp.company in maskmap:
            masked[maskmap[exp.company]] = exp.company
            exp.company = maskmap[exp.company]

    return master, masked, personal


def unmask_personal(tailored: TailoredCV, mask: dict, personal: Personal) -> TailoredCV:

    tailored.personal = personal

    for edu in tailored.education:
        if edu.school in mask:
            edu.school = mask[edu.school]

    for exp in tailored.experience:
        if exp.company in mask:
            exp.company = mask[exp.company]

    return tailored


def parse_output(output: str) -> TailoredCV:
    output = output.strip("```yaml")
    output = output.strip("```")

    data = yaml.safe_load(output)
    try:
        tcv = TailoredCV.model_validate(data)
    except pydantic.ValidationError as e:
        print(f"ERROR: {e}")
        return

    return tcv


if __name__ == "__main__":
    with open("output.txt", "r") as f:
        output = f.read()

    parse_output(output)
