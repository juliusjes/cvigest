from cvingest.models import EducationItem, ExperienceItem, TailoredCV


def construct_latex_source(tcv: TailoredCV) -> str:

    if tcv.personal is not None:
        name = tcv.personal.name
        email = tcv.personal.email
        phone = tcv.personal.phone
        linkedin = tcv.personal.linkedin
        github = tcv.personal.github 

    else:
        name = "placeholder"
        email = "placeholder"
        phone = "placeholder"
        city = "placeholder"
        country = "placeholder"

    experience = [construct_experience_block(expb) for expb in reversed(tcv.experience)]
    experience = "\n".join(experience)

    education = [construct_education_block(edub) for edub in reversed(tcv.education)]
    education = "\n".join(education)

    latex = rf"""
\documentclass[11pt]{{article}}
\usepackage{{graphicx}}
\setlength{{\parindent}}{{0pt}}
\usepackage{{hyperref}}
\usepackage{{enumitem}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{lipsum}}
\usepackage[left=1.06cm,top=1.7cm,right=1.06cm,bottom=0.49cm]{{geometry}}
\setlist[itemize]{{noitemsep}}
\begin{{document}}

\begin{{center}}
    \textbf{{{name}}}\\
    \hrulefill
\end{{center}}

\begin{{center}}
    {email} \textbullet\ {phone} \textbullet {linkedin} \textbullet {github}
\end{{center}}

\vspace{{0.5pt}}

\begin{{center}}
    \textbf{{Experience}}
\end{{center}}

{experience}

\begin{{center}}
    \textbf{{Education}}
\end{{center}}

{education}

\end{{document}}
        """
    return latex


def construct_description(description:str) -> str:

    if description is not None:
        splits = description.split("* ")
        if len(splits) != 0:

            description = ""

            description += rf"\begin{{itemize}}{"\n"}"

            for bullet in splits:
                if len(bullet) < 5:
                    continue
                description += rf"{"\t"}\item {bullet.strip("*")} {"\n"}"

            description += rf"\end{{itemize}}{"\n"}"
    else:
        description = ""

    return description



def construct_experience_block(experience: ExperienceItem) -> str:
    start, end = experience.span.as_tuple()
    title = experience.title
    company = experience.company
    description = construct_description(experience.description)

    latex = rf"""
        \textbf{{{company}}} \\
        \textbf{{{title}}} \hfill {start} – {end}

            {description}
    """
    return latex

def construct_education_block(education: EducationItem) -> str:
    start, end = education.span.as_tuple()
    program = education.program
    school = education.school
    major = education.major
    description = construct_description(education.description)

    latex = rf"""
         \textbf{{{school}}}{"\n"}
        {program} - {major} \hfill {start} – {end}

            {description}
    """
    return latex

def construct_skill_block():
    pass

def construct_personal_block():
    pass

def construct_projects_block():
    pass


if __name__ == "__main__":
    from parse_master import parse_output
    with open("output.txt", "r") as f:
        output = f.read()

    print("parsing model output")
    tailored_cv = parse_output(output)

    if tailored_cv is None:
        print("Could not produce valid TailoredCV object")

    source = construct_latex_source(tailored_cv)


    with open("main.tex", "w") as f:
        f.write(source)